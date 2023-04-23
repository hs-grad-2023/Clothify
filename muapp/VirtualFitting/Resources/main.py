import cvzone
import cv2
from cvzone.PoseModule import PoseDetector
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import datetime, time, pygame

pygame.mixer.init()
shutter_sound = pygame.mixer.Sound("shutter.mp3")
shutter_sound.set_volume(0.5)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
detector = PoseDetector()

shirtsFolderPath = "Shirts"
pantsFolderPath = "Pants"

listShirts = os.listdir(shirtsFolderPath)
listPants = os.listdir(pantsFolderPath)

fixedRatio = 320 / 190 #셔츠의 넓이 262 / lm11에서 12의 사이 넓이
shirtsRatioHeight = 500 / 440 #이미지 사이즈 비율 581/440

fixedRatio2 = 270 / 140 #셔츠의 넓이 262 / lm11에서 12의 사이 넓이
pantsRatioHeight = 1000 / 440 #이미지 사이즈 비율 581/440

imageNumber = 0
imageNumber2 = 0
cameraButton = cv2.imread("camera.png", cv2.IMREAD_UNCHANGED)
imgButtonRight = cv2.imread("button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
counterRight2 = 0
counterLeft2 = 0
counterLeft3 = 0
selectionSpeed = 10
distance_threshold = 673
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findPose(img, draw=False)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    if bboxInfo:
        # center = bboxInfo["center"]
        # cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]

        lm23 = lmList[23][1:3]
        lm24 = lmList[24][1:3]

        distance = lmList[24][2]
        

        
        # else:
        #     cv2.putText(img, f"Distance: {distance}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        imgShirt = cv2.imread(os.path.join(shirtsFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)

        imgPant = cv2.imread(os.path.join(pantsFolderPath, listPants[imageNumber2]), cv2.IMREAD_UNCHANGED)

        widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
        widthOfShirt = max(widthOfShirt, 1)#가장 큰값을 반환. wos가 1보다 작아지면 1반환.
        imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtsRatioHeight)))

        widthOfPant = int((lm23[0] - lm24[0]) * fixedRatio2)
        widthOfPant = max(widthOfPant, 1)#가장 큰값을 반환. wos가 1보다 작아지면 1반환.
        imgPant = cv2.resize(imgPant, (widthOfPant, int(widthOfPant * pantsRatioHeight)))

        currentScale = (lm11[0] - lm12[0]) / 150 #옷 위치 190
        offset = int(52 * currentScale), int(48 * currentScale) #좌우 44, 48 *30/48

        currentScale2 = (lm23[0] - lm24[0]) / 150 #옷 위치 190
        offset2 = int(75 * currentScale2), int(80 * currentScale2) #좌우 44, 48 *30/48 x, y



        try:
            #  img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
            img_height, img_width, _ = img.shape#웹캠 영상의 높이와 너비를 가져옵니다.
            sh_height, sh_width, _ = imgShirt.shape#셔츠 이미지의 높이와 너비를 가져옵니다.

            x_position = max(0, lm12[0] - offset[0])# 셔츠 이미지의 x 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 왼쪽 경계를 벗어나지 않습니다.
            y_position = max(0, lm12[1] - offset[1])#셔츠 이미지의 y 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 위쪽 경계를 벗어나지 않습니다.

            pa_height, pa_width, _ = imgPant.shape#셔츠 이미지의 높이와 너비를 가져옵니다.

            x_position2 = max(0, lm24[0] - offset2[0])# 셔츠 이미지의 x 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 왼쪽 경계를 벗어나지 않습니다.
            y_position2 = max(0, lm24[1] - offset2[1])#셔츠 이미지의 y 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 위쪽 경계를 벗어나지 않습니다.

            # 셔츠 이미지가 웹캠 영역을 벗어난 경우, 잘라내기
            if x_position2 + pa_width <= img_width and y_position2 + pa_height <= img_height:
                img = cvzone.overlayPNG(img, imgPant, (x_position2, y_position2))

            if x_position2 + pa_width > img_width or y_position2 + pa_height > img_height:
                cropped_width2 = min(pa_width, img_width - x_position2)#잘라낼 셔츠 이미지의 너비를 계산합니다. 웹캠 영상의 너비에서 이미지의 x 위치를 뺀 값과 셔츠 이미지의 원래 너비 중 작은 값을 사용합니다.
                cropped_height2 = min(pa_height, img_height - y_position2)#잘라낼 셔츠 이미지의 높이를 계산합니다. 웹캠 영상의 높이에서 이미지의 y 위치를 뺀 값과 셔츠 이미지의 원래 높이 중 작은 값을 사용합니다.
                imgPant_cropped = imgPant[:cropped_height2, :cropped_width2]#셔츠 이미지에서 웹캠 영역 안에 있는 부분만 잘라냅니다.
                img = cvzone.overlayPNG(img, imgPant_cropped, (x_position2, y_position2))#잘라낸 셔츠 이미지를 웹캠 영상에 붙입니다.
            
            if x_position + sh_width <= img_width and y_position + sh_height <= img_height:
                img = cvzone.overlayPNG(img, imgShirt, (x_position, y_position))

            if x_position + sh_width > img_width or y_position + sh_height > img_height:
                cropped_width = min(sh_width, img_width - x_position)
                cropped_height = min(sh_height, img_height - y_position)#
                imgShirt_cropped = imgShirt[:cropped_height, :cropped_width]
                img = cvzone.overlayPNG(img, imgShirt_cropped, (x_position, y_position))
                    
            
        except:
            pass
        
        if lmList[15][1] > 1050 and lmList[15][1] < 1200 and lmList[15][2] < 200 and lmList[15][2] > 100:
            counterLeft3 += 1
            cv2.ellipse(img, (1138, 160), (66, 66), 0, 0, 
                        counterLeft3 * selectionSpeed, (0, 255, 0), 20)
            if counterLeft3 * selectionSpeed > 360:
                counterLeft3 = 0
                start_time = time.time()
                countdown = 3

                while countdown >= 0:
                    _, img = cap.read()
                    img = cv2.flip(img, 1)
                    img = cv2.resize(img, (1280, 720))
                    img = detector.findPose(img, draw=False)
                    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
                    if bboxInfo:
                        # center = bboxInfo["center"]
                        # cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

                        lm11 = lmList[11][1:3]
                        lm12 = lmList[12][1:3]

                        lm23 = lmList[23][1:3]
                        lm24 = lmList[24][1:3]

                        distance = lmList[24][2]          
      
                        # else:
                        #     cv2.putText(img, f"Distance: {distance}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        imgShirt = cv2.imread(os.path.join(shirtsFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)

                        imgPant = cv2.imread(os.path.join(pantsFolderPath, listPants[imageNumber2]), cv2.IMREAD_UNCHANGED)

                        widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
                        widthOfShirt = max(widthOfShirt, 1)#가장 큰값을 반환. wos가 1보다 작아지면 1반환.
                        imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtsRatioHeight)))

                        widthOfPant = int((lm23[0] - lm24[0]) * fixedRatio2)
                        widthOfPant = max(widthOfPant, 1)#가장 큰값을 반환. wos가 1보다 작아지면 1반환.
                        imgPant = cv2.resize(imgPant, (widthOfPant, int(widthOfPant * pantsRatioHeight)))

                        currentScale = (lm11[0] - lm12[0]) / 150 #옷 위치 190
                        offset = int(52 * currentScale), int(48 * currentScale) #좌우 44, 48 *30/48

                        currentScale2 = (lm23[0] - lm24[0]) / 150 #옷 위치 190
                        offset2 = int(75 * currentScale2), int(80 * currentScale2) #좌우 44, 48 *30/48 x, y



                    # 이 부분에 이미지 처리 코드를 삽입하세요.
                    try:
                        #  img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
                        img_height, img_width, _ = img.shape#웹캠 영상의 높이와 너비를 가져옵니다.
                        sh_height, sh_width, _ = imgShirt.shape#셔츠 이미지의 높이와 너비를 가져옵니다.

                        x_position = max(0, lm12[0] - offset[0])# 셔츠 이미지의 x 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 왼쪽 경계를 벗어나지 않습니다.
                        y_position = max(0, lm12[1] - offset[1])#셔츠 이미지의 y 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 위쪽 경계를 벗어나지 않습니다.

                        pa_height, pa_width, _ = imgPant.shape#셔츠 이미지의 높이와 너비를 가져옵니다.

                        x_position2 = max(0, lm24[0] - offset2[0])# 셔츠 이미지의 x 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 왼쪽 경계를 벗어나지 않습니다.
                        y_position2 = max(0, lm24[1] - offset2[1])#셔츠 이미지의 y 위치를 계산하되, 0보다 작으면 0으로 설정합니다. 이렇게 하면 이미지가 위쪽 경계를 벗어나지 않습니다.

                        # 셔츠 이미지가 웹캠 영역을 벗어난 경우, 잘라내기
                        if x_position2 + pa_width <= img_width and y_position2 + pa_height <= img_height:
                            img = cvzone.overlayPNG(img, imgPant, (x_position2, y_position2))

                        if x_position2 + pa_width > img_width or y_position2 + pa_height > img_height:
                            cropped_width2 = min(pa_width, img_width - x_position2)#잘라낼 셔츠 이미지의 너비를 계산합니다. 웹캠 영상의 너비에서 이미지의 x 위치를 뺀 값과 셔츠 이미지의 원래 너비 중 작은 값을 사용합니다.
                            cropped_height2 = min(pa_height, img_height - y_position2)#잘라낼 셔츠 이미지의 높이를 계산합니다. 웹캠 영상의 높이에서 이미지의 y 위치를 뺀 값과 셔츠 이미지의 원래 높이 중 작은 값을 사용합니다.
                            imgPant_cropped = imgPant[:cropped_height2, :cropped_width2]#셔츠 이미지에서 웹캠 영역 안에 있는 부분만 잘라냅니다.
                            img = cvzone.overlayPNG(img, imgPant_cropped, (x_position2, y_position2))#잘라낸 셔츠 이미지를 웹캠 영상에 붙입니다.
                        
                        if x_position + sh_width <= img_width and y_position + sh_height <= img_height:
                            img = cvzone.overlayPNG(img, imgShirt, (x_position, y_position))

                        if x_position + sh_width > img_width or y_position + sh_height > img_height:
                            cropped_width = min(sh_width, img_width - x_position)
                            cropped_height = min(sh_height, img_height - y_position)#
                            imgShirt_cropped = imgShirt[:cropped_height, :cropped_width]
                            img = cvzone.overlayPNG(img, imgShirt_cropped, (x_position, y_position))      
                        
                    except:
                        pass

                    elapsed_time = time.time() - start_time
                    if elapsed_time >= 1:
                        countdown -= 1
                        start_time = time.time()

                    if countdown != -1:
                        img_pil = Image.fromarray(img)
                        draw = ImageDraw.Draw(img_pil)
                        font = ImageFont.truetype("GmarketSansTTF\GmarketSansTTFBold.ttf", 80)
                        draw.text((580, 10), f"{countdown}", font=font, fill=(0, 255, 0, 0))
                        img = np.array(img_pil)

                    cv2.imshow("Virtual Fitting", img)
                    cv2.waitKey(1)

                shutter_sound.play()
                white_img = np.full(img.shape, 255, dtype=np.uint8)
                cv2.imshow("Virtual Fitting", white_img)
                cv2.waitKey(200)
                timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                cv2.imwrite(f'Picture\capture_{timestamp}.png', img)
                print("Capture saved")

        else:
            counterLeft3 = 0


        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        font = ImageFont.truetype("GmarketSansTTF\GmarketSansTTFBold.ttf", 30)  # 한글 폰트 파일을 사용합니다. 시스템에 따라 경로를 변경해야 할 수도 있습니다.
        draw.text((580, 10), "좌우 버튼을 눌러서 가상피팅을 해보세요!(나가기-Q)", font=font, fill=(0, 255, 0, 0))
        img = np.array(img_pil)

        if distance > distance_threshold:
            img_pil = Image.fromarray(img)
            draw = ImageDraw.Draw(img_pil)
            font = ImageFont.truetype("GmarketSansTTF\GmarketSansTTFBold.ttf", 30)  # 한글 폰트 파일을 사용합니다. 시스템에 따라 경로를 변경해야 할 수도 있습니다.
            draw.text((10, 10), "너무 가깝습니다.", font=font, fill=(0, 0, 255, 0))
            img = np.array(img_pil)

        img = cvzone.overlayPNG(img, cameraButton, (1074, 93))

        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 493))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 493))

        if lmList[16][1] < 200 and lmList[16][1] > 100 and lmList[16][2] < 400 and lmList[16][2] > 300:
            counterRight += 1
            cv2.ellipse(img, (139, 360), (66, 66), 0, 0, 
                        counterRight * selectionSpeed, (0, 255, 0), 20)
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber < len(listShirts)-1:
                    imageNumber += 1
                else:
                    imageNumber = 0

        elif lmList[15][1] > 1050 and lmList[15][1] < 1200 and lmList[15][2] < 400 and lmList[15][2] > 300:
            counterLeft += 1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0, 
                        counterLeft * selectionSpeed, (0, 255, 0), 20)
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1
                else:
                    imageNumber = len(listShirts)-1

        elif lmList[16][1] < 200 and lmList[16][1] > 100 and lmList[16][2] < 600 and lmList[16][2] > 500:
            counterRight2 += 1
            cv2.ellipse(img, (139, 560), (66, 66), 0, 0, 
                        counterRight2 * selectionSpeed, (0, 255, 0), 20)
            if counterRight2 * selectionSpeed > 360:
                counterRight2 = 0
                if imageNumber2 < len(listPants)-1:
                    imageNumber2 += 1
                else:
                    imageNumber2 = 0

        elif lmList[15][1] > 1050 and lmList[15][1] < 1200 and lmList[15][2] < 600 and lmList[15][2] > 500:
            counterLeft2 += 1
            cv2.ellipse(img, (1138, 560), (66, 66), 0, 0, 
                        counterLeft2 * selectionSpeed, (0, 255, 0), 20)
            if counterLeft2 * selectionSpeed > 360:
                counterLeft2 = 0
                if imageNumber2 > 0:
                    imageNumber2 -= 1
                else:
                    imageNumber2 = len(listPants)-1
        else:
            counterRight = 0
            counterLeft = 0

            counterRight2 = 0
            counterLeft2 = 0

        

    cv2.imshow("Virtual Fitting", img)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()