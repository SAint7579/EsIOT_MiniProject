from HFunctions import *
import cv2

ACC_WT = 0.5
FRAME_COUNT = 0


cap = cv2.VideoCapture(0)
try:
	while True:
		ret,frame = cap.read()
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		if FRAME_COUNT <= 60:
			get_average(gray,ACC_WT)		
		else:
			rect,count = static_FGEx_count(gray)
			cv2.putText(frame,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255) ,2)
			for (x,y,w,h) in rect:
				cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
		cv2.imshow("Live",frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break	
			
		FRAME_COUNT += 1
	cap.release()
	cv2.destroyAllWindows()	

except:
	cap.release()
	cv2.destroyAllWindows()	

