import io
#import picamera
import cv2
import numpy
import argparse
import cv2.cv as cv

#Create a memory stream so photos doesn't need to be saved in a file
stream = io.BytesIO()

#Get the picture (low resolution, so it should be quite fast)
#Here you can also specify other parameters (e.g.:rotate the image)
'''
with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.capture(stream, format='jpeg')
'''

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

if not args.get("video", False):
	camera = cv2.VideoCapture(1)
	#camera.resolution = (320, 240)
	#camera.capture(stream, format='jpeg')
while True:	
	ret, image = camera.read()

	#Convert the picture into a numpy array
	#buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

	#Now creates an OpenCV image
	#image = cv2.imdecode(buff, 1)

	#Load a cascade file for detecting faces
	face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')

	#Convert to grayscale
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

	#Look for faces in the image using the loaded cascade file
	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4, minSize=(20, 20), flags=cv.CV_HAAR_SCALE_IMAGE)

	print "Found "+str(len(faces))+" face(s)"

	#Draw a rectangle around every found face
	for (x,y,w,h) in faces:
	    cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)

	cv2.imshow('Faces', image)

	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

	#Save the result image
	#cv2.imwrite('result.jpg',image)