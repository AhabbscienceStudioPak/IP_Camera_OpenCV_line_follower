import cv2
import pyautogui
import numpy as np
import requests

#video_capture = cv2.VideoCapture(0)

url = "type your webcam ip address here"
#video_capture = cv2.VideoCapture(0)

#video_capture.set(3, 160)

#video_capture.set(4, 120)

while (True):
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    # Capture the frames

    ret = img

    # Crop the image

    crop_img = img[60:420, 0:660]


    # Convert to grayscale

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Gaussian blur

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Color thresholding

    ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

    # Find the contours of the frame

    contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)


    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        cv2.line(crop_img, (cx, 0), (cx, 720), (255, 0, 0), 1)
        cv2.line(crop_img, (0, cy), (1280, cy), (255, 0, 0), 1)

        cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 1)

        if cx >= 180:
            print("Turn Right!")
            #pyautogui.press('d')
        if cx < 180 and cx > 50:
            print("On Track!")
            #pyautogui.press('w')
        if cx <= 50:
            print("Turn Left")
            #pyautogui.press('a')
    else:
            print("I don't see the line")

    cv2.imshow('frame',crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
