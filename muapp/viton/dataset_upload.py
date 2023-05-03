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

from django.core.files.uploadedfile import SimpleUploadedFile
from muapp.models import viton_upload_model, viton_upload_cloth, viton_upload_result
import os

# cloth_dir = "C:/hs-grad-2023/VITON-HD/datasets/zalando-hd-resized/test/cloth"
# model_dir = "C:/hs-grad-2023/VITON-HD/datasets/zalando-hd-resized/test/image"
# result_dir = "C:/hs-grad-2023/VITON-HD/results/vitondataset_result"

# i = 1
# for root, dirs, files in os.walk(cloth_dir):
#     for cloth_file in files:
#         i+=1
#         # 이미지 파일 경로 생성
#         cloth_path = os.path.join(root, cloth_file)
#         model_path = os.path.join(model_dir, cloth_file)

#         with open(cloth_path, 'rb') as f:
#             cfile = SimpleUploadedFile(f.name, f.read())
#         with open(model_path, 'rb') as f:
#             mfile = SimpleUploadedFile(f.name, f.read())

#         # 모델 인스턴스 생성 및 저장
#         cloth = viton_upload_cloth(name=cloth_file, image=cfile, uploadUser="sample")
#         cloth.save()

#         model = viton_upload_model(name=cloth_file, image=mfile, uploadUser="sample")
#         model.save()
#         if(i>50): break

# # 파일 이름 리스트를 저장할 txt 파일 경로 및 이름 지정
# file_list_file = 'C:/hs-grad-2023/VITON-HD/datasets/zalando-hd-resized/test/custom_pairs.txt'

# model_all = viton_upload_model.objects.all()
# cloth_all = viton_upload_cloth.objects.all()

# with open(file_list_file, 'w') as f:
#     for model in model_all:
#         for cloth in cloth_all:
#             result_name = model.name + ' ' + cloth.name
#             f.write(result_name + '\n')

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
        result = viton_upload_result(name=result, image=file, model_id = (values[0]+'_00.'+values[3]), cloth_id = (values[1]+'_00.'+values[3]))
        result.save()






