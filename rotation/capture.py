import time

import cv2
import mss
import numpy

import pyautogui
import os

from mouse import mousemove
from skimage.measure import compare_ssim, compare_mse, compare_psnr

#monitor = {'top': 14, 'left': 0, 'width': 800, 'height': 600}
# time.sleep(2)
# #pyautogui.moveRel(xOffset=1050, yOffset=0, duration=10)
# matrix = None
# with mss.mss() as sct:
#     NewImg = None
#     while 'Capturing':
#         last_time = time.time()

#         OldImg = NewImg
#         #Move the mouse, might need a sleep after
#         mousemove(x=0,y=10,duration=0)
#         #NewImg = numpy.array(sct.grab(sct.monitors[1]))
#         NewImg = numpy.array(sct.grab(monitor))

#         cv2.imshow('MSS test w/OpenCV', NewImg)
#         # if OldImg is not None:
#         #     matrix = cv2.estimateRigidTransform(OldImg, NewImg, fullAffine=False)
#         #     print(matrix)
#         #     if matrix is not None:
#         #         print(1 - matrix[0][0])
#         #cv2.calcOpticalFlowFarneback

#         #print('fps :{0}'.format(1.0/(time.time() - last_time)))

#         # Quit with q
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             cv2.destroyAllWindows()
#             break
#         #time.sleep(2)


def buildVertPanorama(step=375, delay=10):
    time.sleep(delay)
    with mss.mss() as capture:
        monitor = capture.monitors[1]
        imgArray = [numpy.array(capture.grab(monitor))]

        for _ in range(20):
            mousemove(movex=step, movey=0, delay=0)
            imgArray.append(numpy.array(capture.grab(monitor)))
    
    # stitcher = cv2.createStitcher(False)
    # result = stitcher.stitch(imgArray)

    # cv2.imshow('Verticle Stitch test', result)
    # if cv2.waitKey(25) & 0xFF == ord('q'):
    #         cv2.destroyAllWindows()
    orig = imgArray[0]
    for i in imgArray:
        print("MSE: ", compare_mse(orig, i))
        print("ssim: ", compare_ssim(orig, i, multichannel=True))
        print("psnr: ", compare_psnr(orig, i))
        # cv2.imshow('Verticle Stitch test', i)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    return imgArray

#def mean_square_error()