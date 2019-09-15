from HFunctions import *
import cv2
import time
import pdb
import numpy as np
from cloud_upload import cloud_upload 

ACC_WT = 0.5
ALPHA = 3 #Reduction weight factor

try:
	cap = cv2.VideoCapture(0)
	get_countBackground(ACC_WT,cap,flip = False)
	get_jumpBackground(ACC_WT,cap, flip = False)
	cap.release()
	while True:

		#GREEN ROUTINE
		print("SIGNAL STATUS : GREEN")
		if cloud_upload() !=1:
			print("Upload failed!")
		time.sleep(5) #Waiting on green for 5 seconds
		
		#RED ROUTINE
		print("SIGNAL STATUS : RED")
		FRAME_COUNT = 0
		RED_TIMER = 50
		UPD_COUNT = 5
		cap = cv2.VideoCapture(0)
		try:

			while RED_TIMER > 0:
				ret,frame = cap.read()
				#frame = cv2.flip(frame, 0)
				pts = np.array([[490,0], [150,0] ,[60,300], [580,300]], np.int32)
				jump_pnts = np.array([[60,310],[0,480], [640,480], [580,310] ], np.int32)
				gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)


				#rect,count = haarCascade_count(gray)	#Alternative	
				rect,count = static_FGEx_count(gray)
				capture_jumpers(frame, gray)
				#Displaying the results
				cv2.putText(frame,str(RED_TIMER),(50,50),cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255) ,2)
				#Drawing the ROI
				cv2.polylines(frame, [pts], True,(0,255,0),3)
				cv2.polylines(frame, [jump_pnts], True,(0,0,255),3)
				for (x,y,w,h) in rect:
					cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)

				#Timer update logic
				if FRAME_COUNT % 25 == 0:
					if UPD_COUNT > 0:
						UPD_COUNT -= 1
						RED_TIMER -= 1
					else:
						UPD_COUNT = 5
						RED_TIMER = RED_TIMER - int(1 + ALPHA * count)

				#Showing the live frame
				cv2.imshow("Live",frame)
				FRAME_COUNT += 1
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break	

					
			cap.release()
			cv2.destroyAllWindows()	

		except:
			#Closing the windows
			cap.release()
			cv2.destroyAllWindows()


except KeyboardInterrupt:
	print("Terminated")
