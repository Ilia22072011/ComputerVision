from time import sleep
import cv2
import numpy as np
if __name__ == '__main__':
    def callback(*arg):
        print (arg)
cv2.namedWindow( "result" )

#cap = cv2.VideoCapture("http://192.168.4.1:81/stream")
cap = cv2.VideoCapture(0)

g_h1, g_s1, g_v1, g_h2, g_s2, g_v2 = input().split(sep=' ')
r_h1, r_s1, r_v1, r_h2, r_s2, r_v2 = input().split(sep=' ')
# HSV фильтр для зеленых объектов из прошлого
ghsv_min = np.array((int(g_h1), int(g_s1), int(g_v1)), np.uint8)
ghsv_max = np.array((int(g_h2), int(g_s2), int(g_v2)), np.uint8)

rhsv_min = np.array((r_h1, r_s1, r_v1), np.uint8)
rhsv_max = np.array((r_h2, r_s2, r_v2), np.uint8)
while True:
    sleep(0.01)
    xr = None
    yr = None
    xg = None
    yg = None
    x = None
    y = None
    ret, img = cap.read()
    print(img.shape())
    # преобразуем RGB картинку в HSV модель
    ghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
    rhsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )

    # применяем цветовой фильтр
    gthresh = cv2.inRange(ghsv, ghsv_min, ghsv_max)
    rthresh = cv2.inRange(rhsv, rhsv_min, rhsv_max)

    # вычисляем моменты изображения
    gmoments = cv2.moments(gthresh, 1)
    gdM01 = gmoments['m01']
    gdM10 = gmoments['m10']
    gdArea = gmoments['m00']
    # будем реагировать только на те моменты,
    # которые содержать больше 100 пикселей
    if gdArea > 100:
        xg = int(gdM10 / gdArea)
        yg = int(gdM01 / gdArea)
        
        #cv2.circle(img, (xg, yg), 10, (0,0,255), -1)

    rmoments = cv2.moments(rthresh, 1)
    rdM01 = rmoments['m01']
    rdM10 = rmoments['m10']
    rdArea = rmoments['m00']
    # будем реагировать только на те моменты,
    # которые содержать больше 100 пикселей
    if rdArea > 100:
        xr = int(rdM10 / rdArea)
        yr = int(rdM01 / rdArea)
        #cv2.circle(img, (xr, yr), 10, (0,255, 0), -1)

    if cv2.waitKey(1) == ord('q'):
        break
    #sleep(0.05)
    if xr == None or yr == None or xg == None or yg == None:
        cv2.imshow('result', img)
        continue
    else:
        x = int((xr + xg)/2)
        y = int((yr + yg)/2)
        
        cv2.circle(img, (x, y), 10, (0,255, 0), -1)
        print(x, y)
        cv2.imshow('result', img)
cap.release()
cv2.destroyAllWindows()