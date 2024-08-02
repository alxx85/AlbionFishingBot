import cv2
import numpy as np
import pyautogui
import mss
import pygetwindow as gw

delay = True
window_name = 'Albion Online Client'

window = gw.getWindowsWithTitle(window_name)[0]
window.activate()

template = cv2.imread('Image/Temporary2.png', cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]

# PickUp x: 637

screen_position = {'top': window.top, 'left': window.left, 'width': window.width, 'height': window.height}
screen = mss.mss()

def process_image(image):
    processed_image = cv2.Canny(image, threshold1=100, threshold2=300)
    return processed_image


while delay:
    frame = np.array(screen.grab(screen_position))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.68
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
        for p in frame:
            pts = (pt[0], pt[1])
            x = (pt[0])
            y = (pt[1])
            print(x)
            cv2.putText(frame, "%d-%d" % (x, y), (x + 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 2)
            break
#        delay = False
        break

    processed_image = process_image(frame)
    mean = np.mean(processed_image)
    print('mean = ', mean)
    if mean <= float(7): # усреднение картинки...
        delay = False

cv2.imshow('screenshot', processed_image)
if cv2.waitKey(0):
    cv2.destroyAllWindows()
