import time

import cv2
import numpy as np
import pyautogui
import mss
import pygetwindow as gw

window_name = 'Albion Online Client'

window = gw.getWindowsWithTitle(window_name)[0]
window.activate()

template = cv2.imread('Image/Temporary1.png', cv2.IMREAD_GRAYSCALE)
pickTemp = cv2.imread('Image/PickUp.png', cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]

# PickUp x: 637
# Bite: 458:179

screen_position = {'top': window.top, 'left': window.left, 'width': window.width, 'height': window.height}
bite_position = {'top': 170, 'left': 450, 'width': 50, 'height': 50}
screen = mss.mss()


def process_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    processed_image = cv2.Canny(gray, 200, 300)
    return processed_image


def mouse_click(delay):
    pyautogui.mouseDown(button='left')
    time.sleep(delay)
    pyautogui.mouseUp(button='left')


def fishing_test():
    threshold = 0.8
    operation = 0

    while True:
        image = np.array(screen.grab(screen_position))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        operation += 1
        res = cv2.matchTemplate(image, pickTemp, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
            for p in image:
                #pts = (pt[0], pt[1])
                x = (pt[0])
                #y = (pt[1])
                print(x)
                if x < 635:
                    mouse_click(2)
                    x = 0
                    break
                elif x < 657:
                    mouse_click(1.5)
                    x = 0
                    break
                else:
                    #mouse_click(.1)
                    continue
            else:
                continue
            break
        print(operation)

        if operation >= 40:
            return


def waiting_bite():
    last_time = time.time()

    while True:
        image = np.array(screen.grab(bite_position))

        processed_image = process_image(image)
        mean = np.mean(processed_image)
        print('mean = ', mean)

        if mean <= float(1.8):
            return 1

        delta = time.time() - last_time
        if delta > 60:
            return 0


fish_repeat = 1500

while fish_repeat >= 0:
    pyautogui.moveTo(431, 175, 0.5)
    mouse_click(0.5)
    time.sleep(1.5)

    state = waiting_bite()
    if state == 1:
        mouse_click(1)
        fishing_test()

    pyautogui.keyDown('s')
    # time.sleep(0.2)
    pyautogui.keyUp('s')
    print(f'Осталось {fish_repeat} повторов')
    fish_repeat -= 1

    # if cv2.waitKey(25) & 0xFF == ord("z"):
    #     fish_repeat = -1
