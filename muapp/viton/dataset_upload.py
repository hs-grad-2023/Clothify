'''
1. 콘솔창에서 해당 파일이 위치한 디렉토리로 이동한 후에, python manage.py shell을 입력하여 장고 쉘을 실행합니다.
2. 장고 쉘에서 다음과 같이 코드를 입력하여 데이터를 업로드합니다.
python manage.py shell
cd "C:/hs-grad-2023/django/muapp/viton"

import os
os.chdir('C:/hs-grad-2023/django/muapp/viton')


exec(open('C:/hs-grad-2023/django/muapp/viton/dataset_upload.py', encoding='utf-8').read())
이렇게 하면 upload_data.py 파일에 작성한 코드가 실행되어 데이터를 업로드할 수 있습니다.
'''

'''
from muapp.models import viton_upload_model, viton_upload_cloth, viton_upload_result

viton_upload_model.objects.all().delete()
viton_upload_cloth.objects.all().delete()
viton_upload_result.objects.all().delete()
'''
from muapp.models import viton_upload_model, viton_upload_cloth, viton_upload_result
import os
from django.core.files import File

cm_dir = "C:\hs-grad-2023\VITON-HD\datasets\zalando-hd-resized\\test\cloth-mask"
ip_dir = "C:\hs-grad-2023\VITON-HD\datasets\zalando-hd-resized\\test\image-parse"
oi_dir = "C:\hs-grad-2023\VITON-HD\datasets\zalando-hd-resized\\test\openpose-img"
oj_dir = "C:\hs-grad-2023\VITON-HD\datasets\zalando-hd-resized\\test\openpose-json"
'''
# 데이터베이스를 순회합니다.
for obj in viton_upload_model.objects.all():
    # 파일명을 가져옵니다.
    filename = obj.name.split('.')[0]
    # 파일이 존재하는지 확인합니다.
    if os.path.exists(os.path.join(ip_dir,filename+'.png')) and os.path.exists(os.path.join(oi_dir,filename+'_rendered.png')) and os.path.exists(os.path.join(oj_dir,filename+'_keypoints.json')):
        # 파일을 엽니다.
        with open(os.path.join(ip_dir,filename+'.png'), "rb") as f:
            # 파일 객체를 Django의 File 객체로 변환합니다.
            django_file = File(f)
            # 모델의 image 필드에 할당합니다.
            obj.maskmodel.save(filename+'.png', django_file, save=True)
        with open(os.path.join(oi_dir,filename+'_rendered.png'), "rb") as f:
            # 파일 객체를 Django의 File 객체로 변환합니다.
            django_file = File(f)
            # 모델의 image 필드에 할당합니다.
            obj.openposeImage.save(filename+'_rendered.png', django_file, save=True)
        with open(os.path.join(oj_dir,filename+'_keypoints.json'), "rb") as f:
            # 파일 객체를 Django의 File 객체로 변환합니다.
            django_file = File(f)
            # 모델의 image 필드에 할당합니다.
            obj.openposeJson.save(filename+'_keypoints.json', django_file, save=True)
'''
for obj in viton_upload_cloth.objects.all():
    # 파일명을 가져옵니다.
    filename = obj.name.split('.')[0]
    # 파일이 존재하는지 확인합니다.
    if os.path.exists(os.path.join(cm_dir,filename+'.jpg')):
        # 파일을 엽니다.
        with open(os.path.join(cm_dir,filename+'.jpg'), "rb") as f:
            # 파일 객체를 Django의 File 객체로 변환합니다.
            django_file = File(f)
            # 모델의 image 필드에 할당합니다.
            obj.maskimage.save(filename+'.jpg', django_file, save=True)
    

'''
from django.core.files.uploadedfile import SimpleUploadedFile
from muapp.models import viton_upload_model, viton_upload_cloth, viton_upload_result
import os


cloth_dir = "C:/hs-grad-2023/VITON-HD/datasets/zalando-hd-resized/test/cloth"
model_dir = "C:/hs-grad-2023/VITON-HD/datasets/zalando-hd-resized/test/image"
result_dir = "C:/hs-grad-2023/VITON-HD/results/vitondataset_result"
cm_dir = "C:/hs-grad-2023/VITON-HD/datasets/zalando-hd-resized/test/cloth-mask"
ip_dir = "C:/hs-grad-2023/VITON-HD/datasets/zalando-hd-resized/test/image-parse"
oi_dir = "C:/hs-grad-2023/VITON-HD/datasets/zalando-hd-resized/test/openpose-img"
oj_dir = "C:/hs-grad-2023/VITON-HD/datasets/zalando-hd-resized/test/openpose-json"


i = 1
for root, dirs, files in viton_upload_cloth.objects.all():
    for cloth_file in files:
        i+=1
        # 이미지 파일 경로 생성
        cloth_path = os.path.join(root, cloth_file)
        model_path = os.path.join(model_dir, cloth_file)

        with open(cloth_path, 'rb') as f:
            cfile = SimpleUploadedFile(f.name, f.read())
        with open(model_path, 'rb') as f:
            mfile = SimpleUploadedFile(f.name, f.read())

        # 모델 인스턴스 생성 및 저장
        cloth = viton_upload_cloth(clothesname=cloth_file ,name=cloth_file, image=cfile, uploadUser="sample")
        cloth.save()

        model = viton_upload_model(clothesname=cloth_file, name=cloth_file, image=mfile, uploadUser="sample")
        model.save()
        if(i>50): break

# 파일 이름 리스트를 저장할 txt 파일 경로 및 이름 지정
file_list_file = 'C:/hs-grad-2023/VITON-HD/datasets/zalando-hd-resized/test/custom_pairs.txt'

model_all = viton_upload_model.objects.all()
cloth_all = viton_upload_cloth.objects.all()

with open(file_list_file, 'w') as f:
    for model in model_all:
        for cloth in cloth_all:
            result_name = model.name + ' ' + cloth.name
            f.write(result_name + '\n')
'''
'''
import re
result_dir = "C:/hs-grad-2023/VITON-HD/results/vitondataset_result"
for root, dirs, files in os.walk(result_dir):
    for result in files:
       # 이미지 파일 경로 생성
        result_path = os.path.join(root, result)

        with open(result_path, 'rb') as f:
            file = SimpleUploadedFile(f.name, f.read())

        # 모델 인스턴스 생성 및 저장
        values = re.split('[_|.]',result)
        print(values)
        modelid = viton_upload_model.objects.get(name=(values[0]+'_00.'+values[3]))
        clothid = viton_upload_cloth.objects.get(name=(values[1]+'_00.'+values[3]))

        result = viton_upload_result(name=result, image=file, model_id = modelid.ID, cloth_id = clothid.ID)
        result.save()

'''




