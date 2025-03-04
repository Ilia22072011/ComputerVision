import cv2
import numpy as np
if __name__ == '__main__':
    def nothing(*arg):
        pass
cv2.namedWindow( "result" ) # создаем главное окно
cv2.namedWindow( "settings" ) # создаем окно настроек
cap = int()
while True:
    video_capture = int(input('Whitch video use?(1/2): '))
    if video_capture == 1:
        cap = cv2.VideoCapture(0)
        break
    if video_capture == 2:
        cap = cv2.VideoCapture("http://192.168.4.1:81/stream")
        break
    else:
        print('Eroor try again\n')
        continue
cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)
crange = [0,0,0, 0,0,0]
while True:
    flag, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
# считываем значения бегунков
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')
# формируем начальный и конечный цвет фильтра
    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)
# накладываем фильтр на кадр в модели HSV
    thresh = cv2.inRange(hsv, h_min, h_max)
    cv2.imshow('result', thresh)
    if cv2.waitKey(1) == ord('q'):
        break
print(h1, s1, v1, h2, s2, v2)
cap.release()
cv2.destroyAllWindows()