import cv2
import numpy

background = None

def get_average(frame, weight):
	global background
	if background is None:
		background = frame.copy().astype('float')
		return None
	cv2.accumulateWeighted(frame,background,weight)


def segment(gray,threshold_min = 25):
	'''
		Finds thresholds and contours for the grayscale segment
	'''
	diff = cv2.absdiff(background.astype('uint8'),gray)
	ret,thresholded = cv2.threshold(diff,threshold_min,255,cv2.THRESH_BINARY)
	cont,_ = cv2.findContours(thresholded.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	if len(cont) is None:
		return None
	else:
		segment = cont
		return (thresholded,segment)



def static_FGEx_count(gray):
	'''
		counts entities with static background reduction
	'''
	boundings = []
	ret = segment(gray)
	if ret is not None:
		th,cnt = ret
		for c in cnt:
			if cv2.contourArea(c) > 1000:
				boundings.append(cv2.boundingRect(c))
	#Returns bounding rectangles and item_count
	return boundings,len(boundings)
				
	
	
