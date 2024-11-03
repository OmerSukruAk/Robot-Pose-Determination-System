import cv2 as cv
import numpy as np
import os
import sys
import math

#Color Matrices
lower_blue = [50, 100, 100]
lower_red = [170, 100, 100]
lower_yellow = [20, 100, 100]
upper_blue = [170, 255, 255]
upper_red = [254, 255, 255]
upper_yellow = [50, 255, 255]

#Folder Paths
mainPath = (os.getcwd())
if("Codes" in mainPath):
    mainPath = os.path.dirname(os.getcwd())
    print(f"!new path:{mainPath}\n\n")
ImagesFolder = mainPath + "/Images"
VideosFolder =  mainPath + "/Videos"
TestVideosFolder = VideosFolder + "/Test_Videos"
TestImagesFolder = ImagesFolder + "/Test_Images"
DataFolder = mainPath + "/Data"

#------------------------------------------------------------------------------------------------------[Main funcs]
def generateDirectory():
    try:
        if not os.path.exists(ImagesFolder):
            os.makedirs(ImagesFolder)
        if not os.path.exists(VideosFolder):
            os.makedirs(VideosFolder)
        if not os.path.exists(DataFolder):
            os.makedirs(DataFolder)
        if not os.path.exists(TestImagesFolder):
            os.makedirs(TestImagesFolder)
        if not os.path.exists(TestVideosFolder):
            os.makedirs(TestVideosFolder)
    except OSError:
        print ('Error: Creating directory of data')

def video2Frame(videoPath = "v2f_example.mp4", dirName = "video.mp4"):
    videoName = dirName
    image_folder = ImagesFolder + f"/v2f_{videoName}"

    cap = cv.VideoCapture(videoPath)
    try:
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
    except OSError:
        print ('Error: Creating directory of data')
    currentFrame = 0
    while(True):
        try:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Saves image of the current frame in jpg file
            name = image_folder + "/frame" + str(currentFrame) + ".jpg"
            print ('Creating...' + name)
            cv.imwrite(name, frame)
            # To stop duplicate images
            currentFrame += 1
        except:
            print(">>> ended")
            break
    cap.release()
    cv.destroyAllWindows()
    return image_folder

def frame2Video(imageFolderName,videoName,isFrameName = 0):
    imageLen = len(os.listdir(imageFolderName))
    frame = (cv.imread(imageFolderName + "/frame0.jpg"))
    height, width, layers = frame.shape

    video = cv.VideoWriter((VideosFolder + f"/{videoName}"), 0, 1, (width,height))

    for i in range(imageLen):
        img = cv.imread(imageFolderName + f"/frame{i}.jpg")
        if(isFrameName == 1):
            cv.putText(img, f"frame{i}", (25,25), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        video.write(img)

    cv.destroyAllWindows()
    video.release()

def maskColor(image, isImagePath = 1, lowerArray = [50, 100, 100], upperAray = [170, 255, 255], isShow = 0, isSave = 0, saveName = (TestImagesFolder+"/maskedColor.jpg")):
    
    if isImagePath: #is image is a path or a image variable
        im = cv.imread(image, cv.IMREAD_COLOR)
        if im is None:
            sys.exit("Could not read the image!")
    else:
        im = image

    params = cv.SimpleBlobDetector_Params()
    params.minThreshold = 100;
    params.maxThreshold = 200;
    params.filterByArea = True
    params.minArea = 200
    params.maxArea = 20000
    params.filterByCircularity = True
    params.minCircularity = 0.1
    params.filterByConvexity = True
    params.minConvexity = 0.1
    params.filterByInertia = True
    params.minInertiaRatio = 0.1

    Lower = np.array(lowerArray) 
    Upper = np.array(upperAray)
    frame = im
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, Lower, Upper)
    mask = cv.erode(mask, None, iterations=0)
    mask = cv.dilate(mask, None, iterations=0)
    frame = cv.bitwise_and(frame,frame,mask = mask)
    detector = cv.SimpleBlobDetector_create(params)
    keypoints = detector.detect(mask)

    im_with_keypoints = cv.drawKeypoints(mask, keypoints, np.array([]), (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    frame = cv.bitwise_and(frame,im_with_keypoints,mask = mask)

    if isShow == 1:
        cv.imshow('Masked Color',frame)
        cv.waitKey(0)
    if isSave == 1:
        cv.imwrite(saveName, frame)
    
    return frame #masked color

def findCircles(Image, isImagePath = 1, isShow = 0, isSave = 0, saveName = (TestImagesFolder + "/circles.jpg")):
    circles = {}
    if isImagePath: #is image is a path or a image variable
        im = cv.imread(Image, cv.IMREAD_COLOR)
        if im is None:
            sys.exit("Could not read the image!")
    else:
        im = Image

    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    # Blur using 3 * 3 kernel.
    gray_blurred = cv.blur(gray, (3, 3))

    # Apply Hough transform on the blurred image.
    detected_circles = cv.HoughCircles(gray_blurred, cv.HOUGH_GRADIENT, 1, 20, param1 = 50, param2 =15, minRadius = 1, maxRadius = 40)

    # Draw circles that are detected.
    if detected_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            circles[r] = [a,b]
            if isShow == 1:
                cv.circle(im, (a, b), r, (0, 255, 0), 2) #circumference
                cv.circle(im, (a, b), 1, (0, 255, 0), 1) #center
        
        if isShow == 1:
            cv.imshow("Detected Circle", im)
            cv.waitKey(0)
        if isSave == 1:
            cv.imwrite(saveName, im)
        
        if(len(circles.keys()) == 1):
            for i in circles.keys():
                r1 = i
            return circles.get(r1)
        elif(len(circles.keys()) < 1):
            print("Photo is blurred")
            return None
        else:
            r1,r2 = circles.keys()

        if(r1 > r2):
            return circles.get(r1),circles.get(r2)
        else:
            return circles.get(r2),circles.get(r1)

def calculateAngle(bigCord = [0,0], littleCord = [0,0]):
    x1, y1, x2, y2 = bigCord[0], bigCord[1], littleCord[0], littleCord[1]
    Angle = 0

    if(x2 > x1):
        edgeX = abs(x2-x1)
    else:
        edgeX = abs(x1-x2)
    if(y2 > y1):
        edgeY = abs(y2-y1)
    else:
        edgeY = abs(y1-y2)

    sinA = ((edgeX)/(edgeY))
    cosA = ((edgeY)/(edgeX))

    if (y1 == y2): # 0 or 180  
        if(x1 > x2):
            Angle = 180
        else: #(x1 < x2)
            Angle = 0
    elif (y1 < y2): # between 180-360 
        if(x1 == x2):
            Angle = 270
        elif(x1 > x2):
            Angle = 270 - math.degrees(math.asin(sinA))
        else: #(x1 < x2)
            Angle = 360 - math.degrees(math.acos(cosA))
    else: #(y1 < y2) between 0-180
        if(x1 == x2):
            Angle = 90
        elif(x1 > x2):
            Angle = 90 + math.degrees(math.asin(sinA))
        else: #(x1 < x2)
            Angle = 90 - math.degrees(math.acos(cosA))

    return Angle

def calculateCenter(bigCord = [0,0], littleCord = [0,0]): #find with circles
    x1, y1, x2, y2 = bigCord[0], bigCord[1], littleCord[0], littleCord[1]

    if(x2 > x1):
        edgeX = abs(x2-x1)
        centerX = x1 + int(edgeX/2)
    else:
        edgeX = abs(x1-x2)
        centerX = x2 + int(edgeX/2)
    if(y2 > y1):
        edgeY = abs(y2-y1)
        centerY = y1 + int(edgeX/2)
    else:
        edgeY = abs(y1-y2)
        centerY = y2 + int(edgeX/2)

    return centerX, centerY

def calculateCenter2(maskedImage, isShow = 0, isSave = 0, saveName = (TestImagesFolder + "/blobCenter.jpg")): #find with blob
    img = maskedImage
    # convert the image to grayscale
    gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # convert the grayscale image to binary image
    ret,thresh = cv.threshold(gray_image,127,255,0)	 
    # calculate moments for each contour
    M = cv.moments(thresh)
    # calculate x,y coordinate of center
    try:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    except:
        return None
    
    if isShow == 1:
        cv.circle(img, (cX, cY), 1, (255, 255, 255), -1)
        cv.putText(img, "center", (cX - 25, cY - 25),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv.imshow('Blob',img)
        cv.waitKey(0)
    if isSave == 1:
        cv.imwrite(saveName, img)

    return cX, cY

#------------------------------------------------------------------------------------------------------[Scenarios]




