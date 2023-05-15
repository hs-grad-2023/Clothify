import json
from os import path as osp

import numpy as np
from PIL import Image, ImageDraw
import torch
from torch.utils import data
from torchvision import transforms


class VITONDataset(data.Dataset):
    def __init__(self, opt):
        super(VITONDataset, self).__init__()
        self.load_height = opt.load_height
        self.load_width = opt.load_width
        self.semantic_nc = opt.semantic_nc
        self.data_path = osp.join(opt.dataset_dir, opt.dataset_mode)
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

        # load data list
        img_names = []
        c_names = []
        with open(osp.join(opt.dataset_dir, opt.dataset_mode, opt.dataset_list), 'r') as f:
            for line in f.readlines():
                img_name, c_name = line.strip().split()
                img_names.append(img_name)
                c_names.append(c_name)

        self.img_names = img_names
        self.c_names = dict()
        self.c_names['unpaired'] = c_names

    #get_parse_agnostic는 몸통, 목, 팔 부분이 흰색(255)으로 나타난 이진화된 마스크 return
    def get_parse_agnostic(self, parse, pose_data):
        parse_array = np.array(parse)
        parse_upper = ((parse_array == 5).astype(np.float32) + # upper clothes
                       (parse_array == 6).astype(np.float32) + # dress
                       (parse_array == 7).astype(np.float32)) # coat
        parse_neck = (parse_array == 10).astype(np.float32) # jumpsuit

        parse_lower = ((parse_array == 9).astype(np.float32) + # pants
                       (parse_array == 16).astype(np.float32) + # Left leg
                       (parse_array == 17).astype(np.float32)) # Right Leg
        parse_foot = ((parse_array == 18).astype(np.float32) + # Left Shoe
                     (parse_array == 19).astype(np.float32)) # Right Shoe

        r = 10
        agnostic = parse.copy()

        # mask arms
        for parse_id, pose_ids in [(14, [2, 5, 6, 7]), (15, [5, 2, 3, 4])]: # [('Left arm' ,['RShoulder', 'LShoulder', 'LElbow' LWrist']),('Right arm',['LShoulder','RShoulder','RElbow','RWrist'])]
            # parse_id -> 부위 /  pose_ids -> 관절 위치 / pose_data -> openpose json
            mask_arm = Image.new('L', (self.load_width, self.load_height), 'black')
            mask_arm_draw = ImageDraw.Draw(mask_arm)
            i_prev = pose_ids[0]
            for i in pose_ids[1:]:
                if (pose_data[i_prev, 0] == 0.0 and pose_data[i_prev, 1] == 0.0) or (pose_data[i, 0] == 0.0 and pose_data[i, 1] == 0.0):
                    continue 
                mask_arm_draw.line([tuple(pose_data[j]) for j in [i_prev, i]], 'white', width=r*10) # 각 관절을 잇는 선
                pointx, pointy = pose_data[i]
                radius = r*4 if i == pose_ids[-1] else r*15
                mask_arm_draw.ellipse((pointx-radius, pointy-radius, pointx+radius, pointy+radius), 'white', 'white') #팔을 덮는 원 생성
                i_prev = i
            parse_arm = (np.array(mask_arm) / 255) * (parse_array == parse_id).astype(np.float32)
            agnostic.paste(0, None, Image.fromarray(np.uint8(parse_arm * 255), 'L'))

        # mask torso & neck
        agnostic.paste(0, None, Image.fromarray(np.uint8(parse_upper * 255), 'L'))
        agnostic.paste(0, None, Image.fromarray(np.uint8(parse_neck * 255), 'L'))

        '''
            이 코드는 parse_neck 라는 2D 배열을 이미지로 변환하여 agnostic 이미지에 삽입하는 코드입니다. 
            parse_neck 배열은 특정 인물의 목 부분에 대한 이진 분할 정보를 담고 있으며, 값이 1인 픽셀은 해당 부분이 목인 것으로 간주됩니다.
            
            'L'은 이미지 모드 중 하나입니다. 이 모드는 8비트 흑백 이미지를 나타내며, 각 픽셀은 0~255 범위의 값으로 표현됩니다. 
            L은 "Luminance(밝기)"를 나타내는 말입니다. 따라서 이 모드의 이미지는 흑백 이미지이며, 각 픽셀의 값은 해당 위치의 밝기를 나타냅니다. 
            예를 들어, 0은 검은색, 255는 흰색을 나타냅니다.
        '''

        return agnostic


    '''
    get_img_agnostic는 원본 이미지에 목, 몸통, 팔 등을 gray로 마스크 처리하여 return
    '''

    def get_img_agnostic(self, img, parse, pose_data):
        ''' 
        img -> 모델 사진 / parse -> human parsing mask / pose_data -> openpose json 
        parse_head -> 머리, 목 이진 마스크 / parse_lower -> 허리 아래 이진 마스크
        '''
        parse_array = np.array(parse)
        parse_head = ((parse_array == 4).astype(np.float32) + #'Sunglasses'
                      (parse_array == 13).astype(np.float32)) #'Face'
        parse_lower = ((parse_array == 9).astype(np.float32) + #'Pants'             
                       (parse_array == 12).astype(np.float32) + #'Skirt'           
                       (parse_array == 16).astype(np.float32) + #'Left leg'
                       (parse_array == 17).astype(np.float32) + #'Right leg'
                       (parse_array == 18).astype(np.float32) + #'Left shoe'
                       (parse_array == 19).astype(np.float32)) #'Right shoe'
        '''
        astype(np.float32) 함수는 데이터 타입을 np.float32로 변환하는 함수이며,
        해당 배열에서 각 요소의 값이 1인 경우는 True로, 그렇지 않은 경우는 False로 변환됩니다. 
        이후 두 배열을 더하면 True가 1로 변환되어 값을 가지게 되며, 두 요소가 모두 False인 경우 0이 됩니다. 
        따라서 astype(np.float32) 함수 자체는 1을 반환하는 것이 아니라 1을 포함할 수 있는 데이터 타입으로 변환해주는 함수입니다.
        '''


        r = 20 #반지름
        agnostic = img.copy()
        agnostic_draw = ImageDraw.Draw(agnostic)

        length_a = np.linalg.norm(pose_data[5] - pose_data[2]) #LShoulder - RShoulder => 어깨의 너비
        length_b = np.linalg.norm(pose_data[12] - pose_data[9]) #LHip - RHip => 엉덩이의 너비
        '''
            위 코드에서는 왼쪽에서 오른쪽으로 뺐지만, 시작점에서 끝점을 뺀 것과 같습니다. 
            두 점을 연결하는 벡터의 방향과 크기는 끝점에서 시작점을 뺀 벡터와 같습니다. 
            예를 들어, pose_data[5]와 pose_data[2]를 연결하는 벡터의 방향과 크기는 pose_data[2]에서 pose_data[5]를 뺀 벡터와 같습니다.
        '''

        point = (pose_data[9] + pose_data[12]) / 2 # (LHip + RHip)/2 => 엉덩이 중앙
        pose_data[9] = point + (pose_data[9] - point) / length_b * length_a 
        #RHip = (엉덩이 중심) + (RHip - 엉덩이 중심) / 어깨의 너비 * 엉덩이의 너비
        pose_data[12] = point + (pose_data[12] - point) / length_b * length_a
        #LHip = (엉덩이 중심) + (LHip - 엉덩이 중심) / 어깨의 너비 * 엉덩이의 너비

        '''
        pose_data[9] - point는 엉덩이 위치와 인물 이미지 중심점 사이의 벡터를 계산합니다. 
        이 벡터를 length_b로 나눈 후 length_a를 곱해주면, 어깨 너비와 같은 길이의 벡터가 됩니다. 
        이렇게 계산된 벡터는 인물 이미지 중심점에서 시작하며, 어깨 너비만큼 오른쪽으로 떨어진 지점이 엉덩이 위치입니다.
        따라서 위 코드는, 인물 이미지의 중심점을 기준으로 엉덩이 위치를 재조정하여 어깨 너비에 맞추어 인물의 상체 비율을 보정하는 코드입니다.
        '''

        # mask arms
        agnostic_draw.line([tuple(pose_data[i]) for i in [2, 5]], 'gray', width=r*10) #RShoulder, LShoulder
        for i in [2, 5]: #RShoulder, LShoulder
            pointx, pointy = pose_data[i]
            agnostic_draw.ellipse((pointx-r*5, pointy-r*5, pointx+r*5, pointy+r*5), 'gray', 'gray')
        for i in [3, 4, 6, 7]: # RElbow, LElbow, RWrist, LWrist
            if (pose_data[i - 1, 0] == 0.0 and pose_data[i - 1, 1] == 0.0) or (pose_data[i, 0] == 0.0 and pose_data[i, 1] == 0.0):
                #각 관절의 위치 정보가 존재하지 않는 경우에는 해당 관절을 표시하지 않도록 설정
                continue
            agnostic_draw.line([tuple(pose_data[j]) for j in [i - 1, i]], 'gray', width=r*10)
            pointx, pointy = pose_data[i]
            agnostic_draw.ellipse((pointx-r*5, pointy-r*5, pointx+r*5, pointy+r*5), 'gray', 'gray')

        # mask torso
        for i in [9, 12]: # RHip, LHip
            pointx, pointy = pose_data[i]
            agnostic_draw.ellipse((pointx-r*3, pointy-r*6, pointx+r*3, pointy+r*6), 'gray', 'gray')
        agnostic_draw.line([tuple(pose_data[i]) for i in [2, 9]], 'gray', width=r*6) # RShoulder, RHip
        agnostic_draw.line([tuple(pose_data[i]) for i in [5, 12]], 'gray', width=r*6) # LShoulder, LHip
        agnostic_draw.line([tuple(pose_data[i]) for i in [9, 12]], 'gray', width=r*12) # RHip, LHip
        agnostic_draw.polygon([tuple(pose_data[i]) for i in [2, 5, 12, 9]], 'gray', 'gray') #어꺠와 엉덩이를 잇는 사각형 생성

        # mask neck
        pointx, pointy = pose_data[1]
        agnostic_draw.rectangle((pointx-r*7, pointy-r*7, pointx+r*7, pointy+r*7), 'gray', 'gray')
        agnostic.paste(img, None, Image.fromarray(np.uint8(parse_head * 255), 'L'))
        agnostic.paste(img, None, Image.fromarray(np.uint8(parse_lower * 255), 'L'))

        return agnostic



    '''
    클래스 객체가 인덱싱(인덱스 연산자 []를 사용하여 요소에 접근)이나 
    슬라이싱(슬라이스 연산자 :를 사용하여 범위를 지정하여 요소에 접근)이 될 때 호출되는 메서드
    이를 통해 객체의 요소를 가져오는 작업을 수행합니다. 
    '''
    def __getitem__(self, index): 
        img_name = self.img_names[index]
        c_name = {}
        c = {}
        cm = {}
        for key in self.c_names:
            c_name[key] = self.c_names[key][index]
            c[key] = Image.open(osp.join(self.data_path, 'cloth', c_name[key])).convert('RGB')
            c[key] = transforms.Resize((self.load_width,self.load_height), interpolation=2)(c[key])
            cm[key] = Image.open(osp.join(self.data_path, 'cloth-mask', c_name[key]))
            cm[key] = transforms.Resize((self.load_width,self.load_height), interpolation=0)(cm[key])
            '''
            interpolation은 이미지 크기를 조절할 때 사용되는 보간법(interpolation method)을 의미합니다. 
            이미지를 확대 또는 축소할 때 픽셀값이 결정되는 방법으로, 보간법에 따라 선명도나 변형 정도가 달라질 수 있습니다.

        `   여기서 interpolation=2는 이미지 크기 조절에 bilinear interpolation을 사용하겠다는 의미입니다. 
            Bilinear interpolation은 가장 인접한 4개의 픽셀 값을 이용해 새로운 픽셀 값을 생성하는 방법 중 하나로, 
            비교적 계산이 빠르고 자연스러운 결과를 얻을 수 있기 때문에 일반적으로 많이 사용됩니다.
            '''

            c[key] = self.transform(c[key])  # [-1,1]
            cm_array = np.array(cm[key])
            cm_array = (cm_array >= 128).astype(np.float32)
            cm[key] = torch.from_numpy(cm_array)  # [0,1]
            cm[key].unsqueeze_(0)

            '''
            먼저, `self.transform(c[key])`는 이미지를 `-1`과 `1` 사이의 값으로 Normalize합니다. 
            이는 이미지 분류나 생성과 같은 태스크에서 일반적으로 사용되는 방법 중 하나입니다.

            다음으로, `cm_array`는 입력 이미지와 크기가 동일한 색상 맵 데이터입니다. 
            색상 맵 데이터는 `cm`이라는 딕셔너리 변수에서 가져와서, 128보다 크거나 같은 값은 1, 작은 값은 0으로 이진화하여 
            `np.float32` 형식으로 저장됩니다.

            마지막으로, `cm[key]`는 이진화된 색상 맵 데이터를 PyTorch Tensor 형식으로 변환하고, 채널 차원을 추가합니다(`unsqueeze_(0)`). 
            이를 통해 `cm[key]`는 `[1, height, width]` 형태의 Tensor가 됩니다.
            '''

        # load pose image
        pose_name = img_name.replace('.jpg', '_rendered.png')
        pose_rgb = Image.open(osp.join(self.data_path, 'openpose-img', pose_name))
        pose_rgb = transforms.Resize(self.load_width, interpolation=2)(pose_rgb)
        pose_rgb = self.transform(pose_rgb)  # [-1,1]

        pose_name = img_name.replace('.jpg', '_keypoints.json')
        with open(osp.join(self.data_path, 'openpose-json', pose_name), 'r') as f:
            pose_label = json.load(f)
            pose_data = pose_label['people'][0]['pose_keypoints_2d']
            pose_data = np.array(pose_data)
            pose_data = pose_data.reshape((-1, 3))[:, :2]

        # load parsing image
        parse_name = img_name.replace('.jpg', '.png')
        parse = Image.open(osp.join(self.data_path, 'image-parse', parse_name))
        parse = transforms.Resize(self.load_width, interpolation=0)(parse)
        parse_agnostic = self.get_parse_agnostic(parse, pose_data)
        parse_agnostic = torch.from_numpy(np.array(parse_agnostic)[None]).long()

        labels = {
            0: ['background', [0, 10]],
            1: ['hair', [1, 2]],
            2: ['face', [4, 13]],
            3: ['upper', [5, 6, 7]],
            4: ['bottom', [9, 12]],
            5: ['left_arm', [14]],
            6: ['right_arm', [15]],
            7: ['left_leg', [16]],
            8: ['right_leg', [17]],
            9: ['left_shoe', [18]],
            10: ['right_shoe', [19]],
            11: ['socks', [8]],
            12: ['noise', [3, 11]]
        }
        parse_agnostic_map = torch.zeros(20, self.load_height, self.load_width, dtype=torch.float)
        parse_agnostic_map.scatter_(0, parse_agnostic, 1.0)
        new_parse_agnostic_map = torch.zeros(self.semantic_nc, self.load_height, self.load_width, dtype=torch.float)
        for i in range(len(labels)):
            for label in labels[i][1]:
                new_parse_agnostic_map[i] += parse_agnostic_map[label]

        # load person image
        img = Image.open(osp.join(self.data_path, 'image', img_name))
        img = transforms.Resize(self.load_width, interpolation=2)(img)
        img_agnostic = self.get_img_agnostic(img, parse, pose_data)
        img = self.transform(img)
        img_agnostic = self.transform(img_agnostic)  # [-1,1]

        result = {
            'img_name': img_name,
            'c_name': c_name,
            'img': img,
            'img_agnostic': img_agnostic,
            'parse_agnostic': new_parse_agnostic_map,
            'pose': pose_rgb,
            'cloth': c,
            'cloth_mask': cm,
        }
        return result

    def __len__(self):
        return len(self.img_names)


class VITONDataLoader:
    def __init__(self, opt, dataset):
        super(VITONDataLoader, self).__init__()

        if opt.shuffle:
            train_sampler = data.sampler.RandomSampler(dataset)
        else:
            train_sampler = None

        self.data_loader = data.DataLoader(
                dataset, batch_size=opt.batch_size, shuffle=(train_sampler is None),
                num_workers=opt.workers, pin_memory=True, drop_last=True, sampler=train_sampler
        )
        self.dataset = dataset
        self.data_iter = self.data_loader.__iter__()

    def next_batch(self):
        try:
            batch = self.data_iter.__next__()
        except StopIteration:
            self.data_iter = self.data_loader.__iter__()
            batch = self.data_iter.__next__()

        return batch

        ''' 
        # openpose json Return value
            "version": 버전 정보
            "people": 사람들의 리스트
                "pose_keypoints_2d": 인체 부위의 x, y 좌표 및 신뢰도 값 (각 점들의 신뢰도 값이 함께 반환됨)
                "face_keypoints_2d": 얼굴 부위의 x, y 좌표 및 신뢰도 값 (얼굴 부위를 감지하면 반환됨)
                "hand_left_keypoints_2d": 왼손 부위의 x, y 좌표 및 신뢰도 값 (왼손 부위를 감지하면 반환됨)
                "hand_right_keypoints_2d": 오른손 부위의 x, y 좌표 및 신뢰도 값 (오른손 부위를 감지하면 반환됨)

        # default keypoint order
            0 - Nose        | 5 - LShoulder | 10 - RKnee     | 15 - REye
            1 - Neck        | 6 - LElbow    | 11 - RAnkle    | 16 - LEye
            2 - RShoulder   | 7 - LWrist    | 12 - LHip      | 17 - REar
            3 - RElbow      | 8 - MidHip    | 13 - LKnee     | 18 - LEar
            4 - RWrist      | 9 - RHip      | 14 - LAnkle

        # CHIP datasets label(image-parse)
            0. 'Background'        5. 'Upper clothes'     10. 'Jumpsuits'       15. 'Right arm'
            1. 'Hat'               6. 'Dress'             11. 'Scarf'           16. 'Left leg'
            2. 'Hair'              7. 'Coat'              12. 'Skirt'           17. 'Right leg'
            3. 'Glove'            8. 'Socks'             13. 'Face'            18. 'Left shoe'
            4. 'Sunglasses'      9. 'Pants'             14. 'Left arm'        19. 'Right shoe'

        
        '''