import cv2

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

video = cv2.VideoCapture(0)

while True:
    ret, image = video.read()
    if not ret:
        break
    imagecopy = image.copy()
    corners, ids, _ = cv2.aruco.detectMarkers(image, dictionary)
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(imagecopy, corners, ids)
    cv2.imshow("image", imagecopy)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()
