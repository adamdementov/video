# Purpose
This program tracks a relatively large object with a pattern of yellow, blue, and yellow, stuck closely together.

The program displays visually the tracked object, and outputs
 to the terminal the center of the object as perceived. (Printing currently only implemented in python)

The visual display can be easily disabled.

# Important: this code is only tested for linux environments

Both make use of the opencv library, so be sure that is installed and over version 3.0.

The camera used will be the default one, and if you wish to change that, on the line:

# C++
VideoCapture cap(0);

# Python
cam = cv2.VideoCapture(0)

Change the (0) to another number, and the code will use a camera of lower priority or order.

To compile, run g++ with the following tags and example filenames:

g++ blobber.cpp `pkg-config --libs opencv` -o runnable

Where runnable will be the name of an executable created. This can then be run with:

./runnable

which will start the code and open a viewing window that will show the object tracking.

To disable the visual display, comment out:

# C++
imshow("frame", im_with_keypoints);

# Python
cv2.imshow('frame',im_with_keypoints)

and

cv2.destroyAllWindows()

In the python version,
The code outputs currently only the horizontal axis position from 0 to the video pixel width (currently set to 640)
The vertical axis information is easily available in the code next to the horizontal, but deemed not as important for motion to an object.