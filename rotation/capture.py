import time

import cv2
import mss
import numpy

with mss.mss() as sct:
    while 'Capturing':
        last_time = time.time()

        img = numpy.array(sct.grab(sct.monitors[2]))

        cv2.imshow('MSS test w/OpenCV', img)
        #cv2.calcOpticalFlowFarneback

        print('fps :{0}'.format(1.0/(time.time() - last_time)))

        # Quit with q
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
