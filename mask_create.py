import cv2
import numpy as np

image = np.zeros((480,640), dtype = np.uint8)
points = np.array([[60,310],[0,480], [640,480], [580,310] ], np.int32)

points = points.reshape((-1,1,2))
cv2.fillPoly(image,[points],255)
#cv2.polylines(image, [points] , True, (255,255,255),-1)
#image = cv2.flip(image,0)
cv2.imwrite("mask_jumppoint.jpg",image)
cv2.imshow("temp",image)
cv2.waitKey()
cv2.destroyAllWindows()

