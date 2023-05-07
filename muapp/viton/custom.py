'''
cd C:\hs-grad-2023\VITON-HD
python custom.py --name test2 --dataset_mode custom 


cd C:\hs-grad-2023
python Self-Correction-Human-Parsing/simple_extractor.py --dataset 'lip' --model-restore '/VITON-HD/checkpoints/human_parsing_final.pth' --input-dir '/VITON-HD/datasets/custom/image' --output-dir '/VITON-HD/datasets/custom/image-parse'
'''

'''
- 모든 사진의 사이즈는 768*1024로 맞추기
custom_pair -> img_name(jpg), c_name(jpg)
image(model) -> jpg, 데이터 받아서 resize(768 * 1024)
image-parse -> {image_name}.png, 데이터 받아서 resize(768 * 1024)
                Self-Correction-Human-Parsing(colab) -> https://colab.research.google.com/drive/1JOwOPaChoc9GzyBi5FUEYTSaP2qxJl10?usp=sharing#scrollTo=qB3uv4ksWjry

openpose-img -> {image_name}_rendered.png
openpose-json -> {image_name}_keypoints.json

'''


import argparse
import os

import torch
from torch import nn
from torch.nn import functional as F
import torchgeometry as tgm

from datasets import VITONDataset, VITONDataLoader
from network import SegGenerator, GMM, ALIASGenerator
from utils import gen_noise, load_checkpoint, save_images


def get_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True)

    parser.add_argument('-b', '--batch_size', type=int, default=1)
    parser.add_argument('-j', '--workers', type=int, default=1)
    parser.add_argument('--load_height', type=int, default=1024)
    parser.add_argument('--load_width', type=int, default=768)
    parser.add_argument('--shuffle', action='store_true')

    parser.add_argument('--dataset_dir', type=str, default='./data')
    parser.add_argument('--dataset_mode', type=str, default='custom') #dataset 내부 폴더 이름
    parser.add_argument('--dataset_list', type=str, default='custom_pairs.txt')
    parser.add_argument('--checkpoint_dir', type=str, default='./checkpoints/')
    parser.add_argument('--save_dir', type=str, default='./results/')

    parser.add_argument('--display_freq', type=int, default=1)

    parser.add_argument('--seg_checkpoint', type=str, default='seg_final.pth')
    parser.add_argument('--gmm_checkpoint', type=str, default='gmm_final.pth')
    parser.add_argument('--alias_checkpoint', type=str, default='alias_final.pth')

    # common
    parser.add_argument('--semantic_nc', type=int, default=13, help='# of human-parsing map classes')
    parser.add_argument('--init_type', choices=['normal', 'xavier', 'xavier_uniform', 'kaiming', 'orthogonal', 'none'], default='xavier')
    parser.add_argument('--init_variance', type=float, default=0.02, help='variance of the initialization distribution')

    # for GMM
    parser.add_argument('--grid_size', type=int, default=5)

    # for ALIASGenerator
    parser.add_argument('--norm_G', type=str, default='spectralaliasinstance')
    parser.add_argument('--ngf', type=int, default=64, help='# of generator filters in the first conv layer')
    parser.add_argument('--num_upsampling_layers', choices=['normal', 'more', 'most'], default='most',
                        help='If \'more\', add upsampling layer between the two middle resnet blocks. '
                             'If \'most\', also add one more (upsampling + resnet) layer at the end of the generator.')

    opt = parser.parse_args()
    return opt

# 
def test(opt, seg, gmm, alias):
    up = nn.Upsample(size=(opt.load_height, opt.load_width), mode='bilinear')
    gauss = tgm.image.GaussianBlur((15, 15), (3, 3))
    gauss.cuda()

    custom_dataset = VITONDataset(opt)
    custom_loader = VITONDataLoader(opt, custom_dataset)

    with torch.no_grad():
        for i, inputs in enumerate(custom_loader.data_loader):
            img_names = inputs['img_name']
            c_names = inputs['c_name']['unpaired']

            img_agnostic = inputs['img_agnostic'].cuda()
            parse_agnostic = inputs['parse_agnostic'].cuda()
            pose = inputs['pose'].cuda()
            c = inputs['cloth']['unpaired'].cuda()
            cm = inputs['cloth_mask']['unpaired'].cuda()

            # Part 1. Segmentation generation
            parse_agnostic_down = F.interpolate(parse_agnostic, size=(256, 192), mode='bilinear')
            pose_down = F.interpolate(pose, size=(256, 192), mode='bilinear')
            c_masked_down = F.interpolate(c * cm, size=(256, 192), mode='bilinear')
            cm_down = F.interpolate(cm, size=(256, 192), mode='bilinear')
            seg_input = torch.cat((cm_down, c_masked_down, parse_agnostic_down, pose_down, gen_noise(cm_down.size()).cuda()), dim=1)

            parse_pred_down = seg(seg_input)
            parse_pred = gauss(up(parse_pred_down))
            parse_pred = parse_pred.argmax(dim=1)[:, None]

            parse_old = torch.zeros(parse_pred.size(0), 13, opt.load_height, opt.load_width, dtype=torch.float).cuda()
            parse_old.scatter_(1, parse_pred, 1.0)

            labels = {
                0:  ['background',  [0]],
                1:  ['paste',       [2, 4, 7, 8, 9, 10, 11]],
                2:  ['upper',       [3]],
                3:  ['hair',        [1]],
                4:  ['left_arm',    [5]],
                5:  ['right_arm',   [6]],
                6:  ['noise',       [12]]
            }
            parse = torch.zeros(parse_pred.size(0), 7, opt.load_height, opt.load_width, dtype=torch.float).cuda()
            '''
            torch.zeros(*size, out=None, dtype=None, layout=torch.strided, device=None, requires_grad=False)

            이때 parse_pred.size(0)는 parse_pred 텐서의 첫 번째 차원의 크기를 의미합니다. 
            이 코드는 parse_pred와 같은 개수의 이미지에 대해 parse를 만듭니다.
            parse의 두 번째 차원은 분할된 이미지의 채널 수를 의미하며, 각 채널은 분할된 이미지의 특정 클래스를 나타냅니다. 
            이 코드에서는 7개의 채널을 가진 parse를 만들기 때문에 분할된 이미지는 7개의 클래스로 나누어집니다.
            '''
            for j in range(len(labels)):
                for label in labels[j][1]:
                    parse[:, j] += parse_old[:, label]

            # Part 2. Clothes Deformation
            agnostic_gmm = F.interpolate(img_agnostic, size=(256, 192), mode='nearest')
            parse_cloth_gmm = F.interpolate(parse[:, 2:3], size=(256, 192), mode='nearest')
            pose_gmm = F.interpolate(pose, size=(256, 192), mode='nearest')
            c_gmm = F.interpolate(c, size=(256, 192), mode='nearest')
            gmm_input = torch.cat((parse_cloth_gmm, pose_gmm, agnostic_gmm), dim=1)

            _, warped_grid = gmm(gmm_input, c_gmm)
            warped_c = F.grid_sample(c, warped_grid, padding_mode='border')
            warped_cm = F.grid_sample(cm, warped_grid, padding_mode='border')

            # Part 3. Try-on synthesis
            misalign_mask = parse[:, 2:3] - warped_cm #parse[:, 2:3] -> upper~hair
            misalign_mask[misalign_mask < 0.0] = 0.0
            parse_div = torch.cat((parse, misalign_mask), dim=1) #마스크와 위치좌표가 있는 parse 결합
            parse_div[:, 2:3] -= misalign_mask

            output = alias(torch.cat((img_agnostic, pose, warped_c), dim=1), parse, parse_div, misalign_mask)

            '''
            alias = ALIASGenerator(opt, input_nc=9)
            def __init__(self, opt, input_nc):
            '''

            unpaired_names = []
            for img_name, c_name in zip(img_names, c_names):
                unpaired_names.append('{}_{}'.format(img_name.split('_')[0], c_name))

            save_images(output, unpaired_names, os.path.join(opt.save_dir, opt.name))

            if (i + 1) % opt.display_freq == 0:
                print("step: {}".format(i + 1))


def main():
    opt = get_opt()
    print(opt)

    if not os.path.exists(os.path.join(opt.save_dir, opt.name)):
        os.makedirs(os.path.join(opt.save_dir, opt.name))

    seg = SegGenerator(opt, input_nc=opt.semantic_nc + 8, output_nc=opt.semantic_nc)
    gmm = GMM(opt, inputA_nc=7, inputB_nc=3)
    opt.semantic_nc = 7
    alias = ALIASGenerator(opt, input_nc=9)
    opt.semantic_nc = 13

    load_checkpoint(seg, os.path.join(opt.checkpoint_dir, opt.seg_checkpoint))
    load_checkpoint(gmm, os.path.join(opt.checkpoint_dir, opt.gmm_checkpoint))
    load_checkpoint(alias, os.path.join(opt.checkpoint_dir, opt.alias_checkpoint))

    seg.cuda().eval()
    gmm.cuda().eval()
    alias.cuda().eval()
    test(opt, seg, gmm, alias)


if __name__ == '__main__':
    main()
