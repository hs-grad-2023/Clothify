'''
1. 콘솔창에서 해당 파일이 위치한 디렉토리로 이동한 후에, python manage.py shell을 입력하여 장고 쉘을 실행합니다.
2. 장고 쉘에서 다음과 같이 코드를 입력하여 데이터를 업로드합니다.
    exec(open('upload_data.py').read())
이렇게 하면 upload_data.py 파일에 작성한 코드가 실행되어 데이터를 업로드할 수 있습니다.
'''

from django.core.files.uploadedfile import SimpleUploadedFile
from muapp.models import viton_upload_model, viton_upload_cloth
import os

cloth_dir = "C:/hs-grad-2023/VITON-HD/datasets/zalando-hd-resized/test/cloth"
model_dir = "C:/hs-grad-2023/VITON-HD/datasets/zalando-hd-resized/test/image"

for root, dirs, files in os.walk(cloth_dir):
    for cloth_file in files:
        # 이미지 파일 경로 생성
        cloth_path = os.path.join(root, cloth_file)
        model_path = os.path.join(model_dir, cloth_file)

        with open(cloth_path, 'rb') as f:
            cfile = SimpleUploadedFile(f.name, f.read())
        with open(model_path, 'rb') as f:
            mfile = SimpleUploadedFile(f.name, f.read())

        # 모델 인스턴스 생성 및 저장
        cloth = viton_upload_cloth(clothes_name=cloth_file, clothes_image=cfile)
        cloth.save()

        model = viton_upload_model(model_name=cloth_file, model_image=mfile)
        model.save()