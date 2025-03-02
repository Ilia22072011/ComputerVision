#Импортитуем модули
from time import sleep
import cv2
import numpy as np
if __name__ == '__main__':
    def callback(*arg):
        print (arg)

turn_angle = 180  #Инициализируем переменную угла пворота мотора

cv2.namedWindow( "result" ) #Даём название окну 

cap = int()  #Инициализируем переменную для видеопотока
#Выбираем источник видеопотока
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

g_h1, g_s1, g_v1, g_h2, g_s2, g_v2 = input().split(sep=' ')  #Вводим настройки для 1го цвета
r_h1, r_s1, r_v1, r_h2, r_s2, r_v2 = input().split(sep=' ')  #Вводим настройки для 2го цвета

#Создаём HSV модель 1го цвета
ghsv_min = np.array((int(g_h1), int(g_s1), int(g_v1)), np.uint8)
ghsv_max = np.array((int(g_h2), int(g_s2), int(g_v2)), np.uint8)

#Создаём HSV модель 2го цвета
rhsv_min = np.array((r_h1, r_s1, r_v1), np.uint8)
rhsv_max = np.array((r_h2, r_s2, r_v2), np.uint8)

#Создаём основной цикл программы
while True:
    sleep(0.01)  #Задержка для ограничения fps

    xr, xg = int(), int() #Обнуляем переменные координат

    ret, img = cap.read()  #Читаем изображение

    #Создаём HSV модели
    ghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
    rhsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )

    gthresh = cv2.inRange(ghsv, ghsv_min, ghsv_max)
    rthresh = cv2.inRange(rhsv, rhsv_min, rhsv_max)

    #Высчитываем моменты
    gmoments = cv2.moments(gthresh, 1)
    gdM01 = gmoments['m01']
    gdM10 = gmoments['m10']
    gdArea = gmoments['m00']

    rmoments = cv2.moments(rthresh, 1)
    rdM01 = rmoments['m01']
    rdM10 = rmoments['m10']
    rdArea = rmoments['m00']

    #Выставляем минимальную планку, чтобы исключить ошибки
    if gdArea > 100:    
        xg = int(gdM10 / gdArea)    

    if rdArea > 100:
        xr = int(rdM10 / rdArea) 

    #Проыеряяем нажание клавиши для завершения программы
    if cv2.waitKey(1) == ord('q'):
        break

    #Настройка П-регулятора
    if xr == 0 or xg == 0:
        cv2.imshow('result', img)
        data_to_send = 777
        continue
    else:
        w_img = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        x = int((xr + xg)/2)
        data_to_send = int((x - w_img / 2) * (turn_angle/w_img))
        cv2.circle(img, (x, 100), 10, (0,255, 0), -1)
        print(data_to_send)
        cv2.imshow('result', img)

cap.release()
cv2.destroyAllWindows()