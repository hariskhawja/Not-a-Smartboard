from dotenv import load_dotenv
import cv2
import time

load_dotenv()

def init_cam():
    cam_port = -1
    while cam_port <= 10:
        cam = cv2.VideoCapture(cam_port)
        if cam.isOpened():
            return cam
        else:
            cam.release()
            cam_port+=1
            time.sleep(1)


def capture_picture(image_paths):
    cam = init_cam()
    if not (cam.isOpened()):
        print("Not open")

    res, img = cam.read()

    if res:
        for image_path in image_paths:
            cv2.imwrite(image_path, img)

#capture_picture(["./img.png", "./dsa.png"])
