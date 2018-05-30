import cv2
import numpy as np;

cam = cv2.VideoCapture(0)


# Set up the detector with default parameters.
params = cv2.SimpleBlobDetector_Params()

params.filterByArea = True
params.minArea = 1000
params.filterByCircularity = True
params.minCircularity = 0
params.maxCircularity = 1
params.filterByConvexity = False
params.filterByInertia = True
params.minInertiaRatio = 0.1
params.minDistBetweenBlobs = 10
params.filterByColor = False
params.maxArea = 20000
centerValue_inner = 110
centerValue_outer = 30
detector = cv2.SimpleBlobDetector_create(params)

while(True):
	# Capture frame-by-frame
	ret, frame = cam.read()
	frame = cv2.resize(frame,(640,480))
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# define range of blue color in HSV
	#KEEP IN MIND HUE IS 0-180
	lower_inner = np.array([centerValue_inner-10,65,0])
	upper_inner = np.array([centerValue_inner+10,255,255])
	lower_outer = np.array([centerValue_outer-10,80,0])
	upper_outer = np.array([centerValue_outer+10,255,255])

	# Threshold the HSV image to get only blue colors
	mask_inner = cv2.inRange(hsv, lower_inner, upper_inner)
	mask_outer = cv2.inRange(hsv, lower_outer, upper_outer)

	# Bitwise-AND mask and original image
	res_inner = cv2.bitwise_and(frame,frame, mask= mask_inner)
	res_outer = cv2.bitwise_and(frame,frame, mask= mask_outer)	

	keypoints_inner = detector.detect(res_inner)
	if(len(keypoints_inner) > 0):
		keypoints_inner = [max(keypoints_inner, key=(lambda circ : circ.size))]
	keypoints_outer = detector.detect(res_outer)
	if(len(keypoints_outer) > 1):
		outer_a = max(keypoints_outer, key=(lambda circ : circ.size))
		keypoints_outer.remove(outer_a)
		outer_b = max(keypoints_outer, key=(lambda circ : circ.size))
		keypoints_outer = [outer_a,outer_b]

	average = 0
	if(len(keypoints_outer) == 0):
		keypoints_inner = None
		keypoints_outer = None
		average = -1
	else:
		
		count = len(keypoints_outer) + len(keypoints_inner)
		if(len(keypoints_outer) != 0):
			for circ in keypoints_outer:
				average += circ.pt[0]
		if(len(keypoints_inner) != 0):
			average += keypoints_inner[0].pt[0]
		average /= count;
	print average
	# Display the resulting frame
	im_with_keypoints = cv2.drawKeypoints(frame, keypoints_inner, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	im_with_keypoints = cv2.drawKeypoints(im_with_keypoints, keypoints_outer, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imshow('frame',im_with_keypoints)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
