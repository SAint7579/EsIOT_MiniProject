import cv2
import numpy

background = None

def get_averageBackground(weight, capture):
	global background
	for i in range(60):
		ret,frame = capture.read()
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		if background is None:
			background = gray.copy().astype('float')
			return None
		cv2.accumulateWeighted(gray,background,weight)


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

def haarCascade_count(gray):
	'''
		counts entities using haar classifiers
	'''
	#Creating classifier objects
	car_cascade = cv2.CascadeClassifier(cars.xml)
	bike_cascade = cv2.CascadeClassifier(two_wheeler.xml)
	bus_cascade = cv2.CascadeClassifier(bus_front.xml)

	#Detecting objects
	cars = car_cascade.detectMultiScale(gray, 1.1, 2)
    	bike = bike_cascade.detectMultiScale(gray,1.01, 1)
	bus = bus_cascade.detectMultiScale(gray, 1.16, 1)

	boundings = list(cars) + list(bike) + list(bus)
	#Returns bounding rectangles and item_count
	return boundings,len(boundings)				
	
	
