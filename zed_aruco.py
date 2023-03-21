import cv2
import pyzed.sl as sl
from aruco_utils import get_aruco_image

camera = sl.Camera()
image = sl.Mat()

camera.open()

while True:
    ret = camera.grab()
    if not ret: raise
    
    ret = camera.retrieve_image(image, sl.VIEW.LEFT)
    if not ret: continue
    
    img = image.get_data()[:, :, :3]
    aruco_image, corners, ids, rej = get_aruco_image(img)
    
    cv2.imshow('aruco_image', aruco_image)
    if cv2.waitKey(1) == ord('q'): break
    
cv2.destroyAllWindows()
camera.close()