import cv2
import numpy as np
import pdb
import datetime



background = None
background_jump = None
road_mask = cv2.imread('mask_count.jpg',cv2.IMREAD_GRAYSCALE)
cross_mask = cv2.imread('mask_jumppoint.jpg',cv2.IMREAD_GRAYSCALE)


def showimg(img):
	cv2.imshow("asked",img)
	cv2.waitKey()
	cv2.destroyAllWindows()

def get_countBackground(weight, capture, flip = False):
	'''
		Gets the averaged background for the waiting area
	'''
	global background
	#Averaging for 60 frames

	for i in range(60):
		ret,frame = capture.read()
		#If the image is inverted
		if flip is True:
			frame = cv2.flip(frame,0)
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		#Getting the ROI from mask
		if road_mask is not None:
			gray = cv2.bitwise_and(gray,road_mask)
		if background is None:
			background = gray.copy().astype('float')
			return None
		#Computing the average
		cv2.accumulateWeighted(gray,background,weight)

def get_jumpBackground(weight, capture, flip = False):
	'''
		Gets the background for the restricted area
	'''
	global background_jump
	#Averaging for 60 frames

	for i in range(60):
		ret,frame = capture.read()
		#If the image is inverted
		if flip is True:
			frame = cv2.flip(frame,0)
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		#Getting the roi form the frame
		if cross_mask is not None:
			gray = cv2.bitwise_and(gray,cross_mask)
		if background_jump is None:
			background_jump = gray.copy().astype('float')
			return None
		#Computing the average
		cv2.accumulateWeighted(gray,background_jump,weight)



def segment(gray, threshold_min = 25):
	'''
		Finds thresholds and contours for the grayscale segment
	'''
	if road_mask is not None:
		gray = cv2.bitwise_and(gray,road_mask)
	#Getting the thresholded area
	diff = cv2.absdiff(background.astype('uint8'),gray)
	ret,thresholded = cv2.threshold(diff,threshold_min,255,cv2.THRESH_BINARY)
	#Getting the contours
	cont,_ = cv2.findContours(thresholded.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	if len(cont) is None:
		return None
	else:
		segment = cont
		return (thresholded,segment)


def capture_jumpers(frame, gray, threshold_min = 25):
	'''
		Uses background subtractions to capture images of the jumper
	'''
	if cross_mask is not None:
		gray = cv2.bitwise_and(gray,cross_mask)
	#Getting the threshoded area
	diff = cv2.absdiff(background_jump.astype('uint8'),gray)
	ret,thresholded = cv2.threshold(diff,threshold_min,255,cv2.THRESH_BINARY)
	#Getting the contours
	cont,_ = cv2.findContours(thresholded.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	if len(cont) is None:
		return None
	else:
		for c in cont:
			#Finding the relevant areas
			if cv2.contourArea(c) > 2000:
				x,y,w,h = cv2.boundingRect(c)
				cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),3)
				jumper = frame[y:y+h,x:x+w]
				#Saving the images
				cv2.imwrite('./jumpers/'+str(datetime.datetime.now())+'.jpg',jumper)


def static_FGEx_count(gray):
	'''
		counts entities with static background reduction
	'''
	boundings = []
	ret = segment(gray)
	if ret is not None:
		th,cnt = ret
		for c in cnt:
			#Getting the relevant contours
			if cv2.contourArea(c) > 1000:
				boundings.append(cv2.boundingRect(c))
	#Returns bounding rectangles and item_count
	return boundings,len(boundings)

def haarCascade_count(gray):
	'''
		counts entities using haar classifiers
	'''
	#Creating classifier objects
	car_cascade = cv2.CascadeClassifier("cars.xml")
#	bike_cascade = cv2.CascadeClassifier("two_wheeler.xml")
#	bus_cascade = cv2.CascadeClassifier("bus_front.xml")

	#Detecting objects
	cars = car_cascade.detectMultiScale(gray, 1.1, 2)
	boundings = list(cars)
	#Returns bounding rectangles and item_count
	return boundings,len(boundings)				
	
	
