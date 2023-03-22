import cv2
import pyzed.sl as sl
import numpy as np
from aruco_utils import get_aruco_image

camera = sl.Camera()
if camera.open() != sl.ERROR_CODE.SUCCESS:
    raise Exception("No camera")

camera_prameter = camera.get_camera_information().calibration_parameters.left_cam
fx = camera_prameter.fx
fy = camera_prameter.fy
cx = camera_prameter.cx
cy = camera_prameter.cy
dist_coeffs = camera_prameter.disto

K = np.float32([[fx, 0, cx],
                [0, fy, cy],
                [0, 0, 1]])
print(K)
image = sl.Mat()
markerlength = 0.05
obj_points = np.float32([[-1, 1, 0], 
                         [1, 1, 0], 
                         [1, -1, 0], 
                         [-1, -1, 0]]) * markerlength

R = np.eye(3, 3, dtype=np.float32)
rvec_, _ = cv2.Rodrigues(R)
flag = False
while True:
    if camera.grab() != sl.ERROR_CODE.SUCCESS:
        continue

    if camera.retrieve_image(image, sl.VIEW.LEFT) != sl.ERROR_CODE.SUCCESS:
        continue
    
    img = image.get_data()[:, :, :3]
    
    aruco_image, corners, ids, rej = get_aruco_image(img)
    #if ids is None: continue
    for corner in corners:
        ret, rvec, tvec = cv2.solvePnP(obj_points, corner, K, dist_coeffs)
        cv2.drawFrameAxes(aruco_image, K, dist_coeffs, rvec, tvec, 0.05)
        #print(tvec)
    if flag:
        R_, _ = cv2.Rodrigues(rvec)
        rvec_, _ = cv2.Rodrigues(R_)
        
    
    #aruco_image = cv2.putText(aruco_image, "Test", (100, 100), cv2.FONT_HERSHEY_COMPLEX, 10, (0, 0, 255), 3)
    cv2.putText(aruco_image, str(rvec_.ravel()), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.imshow("image", aruco_image)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('e'):
        flag = True
        
cv2.destroyAllWindows()
camera.close()
    
    