from HFunctions import *
import cv2
import time

ACC_WT = 0.5
ALPHA = 1 #Reduction weight factor
try:
	while True:
		#GREEN ROUTINE
		time.sleep(5) #Waiting on green for 5 seconds

		#RED ROUTINE

		#FRAME_COUNT = 0
		RED_TIMER = 50
		UPD_CNT = 5
		cap = cv2.VideoCapture(0)
		try:
			get_averageBackground(ACC_WT,cap)
			while RED_TIMER > 0:
				ret,frame = cap.read()
				gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)		
				rect,count = static_FGEx_count(gray)
				cv2.putText(frame,str(RED_TIMER),(50,50),cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255) ,2)
				for (x,y,w,h) in rect:
					cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
				cv2.imshow("Live",frame)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break	
					
				if UPD_COUNT > 0:
					UPD_COUNT -= 1
					RED_TIMER -= 1
				else:
					UPD_COUNT = 5
					RED_TIMER = RED_TIMER - int(1 + ALPHA * count)
					
			cap.release()
			cv2.destroyAllWindows()	

		except:
			cap.release()
			cv2.destroyAllWindows()	

except KeyboardInterrupt:
	print("Terminated")
