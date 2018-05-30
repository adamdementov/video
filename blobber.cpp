#include <iostream>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

int main(){

	int centerValue_inner = 110;
	int centerValue_outer = 30;

	VideoCapture cap(0);

	if(!cap.isOpened())  // check if we succeeded
	        return -1;

	SimpleBlobDetector::Params params;

	params.filterByArea = true;
	params.minArea = 1000;
	params.filterByCircularity = true;
	params.minCircularity = 0;
	params.maxCircularity = 1;
	params.filterByConvexity = false;
	params.filterByInertia = true;
	params.minInertiaRatio = 0.1;
	params.minDistBetweenBlobs = 10;
	params.filterByColor = false;
	params.maxArea = 20000;
	Ptr<cv::SimpleBlobDetector> detector = SimpleBlobDetector::create(params);
	

	while(true)
	{
		Mat frame;
		Mat hsv;
		Mat inner_mask;
		Mat outer_mask;
		Mat im_with_keypoints;

		cap.read(frame); // get a new frame from camera

		resize(frame, frame,Size(640,480));
		cvtColor(frame, hsv, COLOR_BGR2HSV);//prepare input frame
		inRange(hsv, Scalar(centerValue_inner-10,65,0), Scalar(centerValue_inner+10,255,255), inner_mask);//filter inner
		inRange(hsv, Scalar(centerValue_outer-10,80,0), Scalar(centerValue_outer+10,255,255), outer_mask);//filter outer

		
		std::vector<KeyPoint> keypoints_outer;
		std::vector<KeyPoint> keypoints_inner;
		detector->detect( inner_mask, keypoints_inner);
		detector->detect( outer_mask, keypoints_outer);
	

		drawKeypoints(frame, keypoints_inner,im_with_keypoints, Scalar(0,0,255), 4);
		drawKeypoints(im_with_keypoints, keypoints_outer,im_with_keypoints, Scalar(0,0,255), 4);

		imshow("frame", im_with_keypoints);
		if(waitKey(30) >= 0) break;
	}
	// the camera will be deinitialized automatically in VideoCapture destructor
	return 0;
}
