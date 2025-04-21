import cv2
from time import time
import statistics
import numpy as np  # Импортируем NumPy

cap = cv2.VideoCapture(0)
cv2.namedWindow("result")  # Даём название окну 
while True:
    ret, img = cap.read()
    if not ret:  # Проверяем, удалось ли захватить изображение
        print("Не удалось захватить изображение")
        break
    if cv2.waitKey(1) == ord('q'):
        break
    
    res = []
    height = img.shape[0]
    width = img.shape[1]
    start = time()
    
    for y in range(0, height, 8):
        was = False
        last = np.sum(img[y][0], dtype=np.int32) / 3  # Используем np.sum с типом int32
        for x in range(0, width, 4):
            ava = np.sum(img[y][x], dtype=np.int32) / 3  # Используем np.sum с типом int32
            if not was and abs(last - ava) > 60:
                res.append(x)
                was = True  # Исправлено на присваивание True
                last = ava
                
    if len(res) != 0:
        ans = int(statistics.median(res))
        data = -1*( int(180 / width * ans) - 90)
        cv2.circle(img, (ans, 100), 10, (0, 255, 0), -1)
        cv2.imshow('result', img)
        print(data, '\t', time() - start)
    else:
        continue

cap.release()  # Освобождаем ресурс видеозахвата
cv2.destroyAllWindows()  # Закрываем все окна OpenCV
