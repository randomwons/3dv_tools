import cv2
import numpy as np


def get_aruco_image(image : np.array,
            dictionary=cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)):
    
    imagecopy = image.copy()
    corners, ids, rej = cv2.aruco.detectMarkers(image, dictionary)
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(imagecopy, corners, ids)
    
    return imagecopy, corners, ids, rej
    