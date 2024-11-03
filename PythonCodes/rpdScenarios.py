import cv2 as cv, numpy as np, sys, os
import robotPoseDeterminer as rpd
import xlsxwriter
import datetime

def examineBot(Image, lower, upper, isImagePath = 1, returnName = "test.jpg", isShow  = 0, saveFolder = rpd.TestImagesFolder, isSave = 0):

    if isImagePath == 1: #is image is a path or a image variable
        imageName = returnName
        image = cv.imread(Image)
        if image is None:
            sys.exit("Could not read the image!")
    else:
        image = Image
        imageName = returnName

    masked = rpd.maskColor(Image, isImagePath, lower, upper)

    try:
        bigCirc , littleCirc = rpd.findCircles(masked, 0)
        Angle = round(rpd.calculateAngle(bigCirc, littleCirc), 2)
        Center = rpd.calculateCenter(bigCirc, littleCirc)
    except:
        Center = rpd.calculateCenter2(masked)
        Angle = "unknown"

    if(Center == None):
        return None

    if isShow == 1:
        cv.putText(image, f"Ang:{Angle}", (Center[0], Center[1]),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv.imshow(f"{imageName}",image)
        cv.waitKey(0)
    if isSave == 1:
        cv.imwrite(saveFolder+f"/{imageName}", image)

    return image, bigCirc, Angle

def examineBall(Image, lower, upper, isImagePath = 1, returnName = "test.jpg", isShow  = 0, saveFolder = rpd.TestImagesFolder, isSave = 0):
    if isImagePath == 1: #is image is a path or a image variable
        imageName = returnName
        image = cv.imread(Image)
        if image is None:
            sys.exit("Could not read the image!")
    else:
        image = Image
        imageName = returnName

    masked = rpd.maskColor(Image, isImagePath, lower, upper,0)

    try:
        Center = rpd.findCircles(masked, 0, 0)
    except:
        Center = rpd.calculateCenter2(masked, 0)

    if(Center == None):
        return None

    if isShow == 1:
        cv.putText(image, f"({Center[0]},{Center[1]})", (Center[0] - 50, Center[1] + 35),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv.imshow(f"{imageName}",image)
        cv.waitKey(0)
    if isSave == 1:
        cv.imwrite(saveFolder+f"/{imageName}", image)

    return image, Center

def examineFrame(Image = "", ImageName = "test.jpg", isImagePath = 1, isShow = 0, folderName = "folder1", isSave = 0):
    if(isImagePath == 1):
        image = cv.imread(Image)
    else:
        image = Image

    im1, ballCenter = examineBall(Image, rpd.lower_yellow, rpd.upper_yellow, isImagePath)
    im2, blueCenter,blueAngle = examineBot(im1, rpd.lower_blue, rpd.upper_blue, 0)
    im3, redCenter,redAngle = examineBot(im2, rpd.lower_red, rpd.upper_red, 0, ImageName, 0)

    cv.rectangle(image,(blueCenter[0] - 45, blueCenter[1] - 45),(blueCenter[0] + 45, blueCenter[1] + 45),(255, 255, 255),2)
    cv.rectangle(image,(ballCenter[0] - 15, ballCenter[1] - 15),(ballCenter[0] + 15, ballCenter[1] + 15),(255, 255, 255),2)
    cv.rectangle(image,(redCenter[0] - 45, redCenter[1] - 45),(redCenter[0] + 45, redCenter[1] + 45),(255, 255, 255),2)
    cv.putText(image, f"({blueCenter[0]},{blueCenter[1]})", (blueCenter[0], blueCenter[1]),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv.putText(image, f"({redCenter[0]},{redCenter[1]})", (redCenter[0], redCenter[1]),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv.putText(image, f"Ang:{blueAngle}", (blueCenter[0], blueCenter[1]+20),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv.putText(image, f"Ang:{redAngle}", (redCenter[0], redCenter[1]+20),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv.putText(image, f"({ballCenter[0]},{ballCenter[1]})", (ballCenter[0] - 50, ballCenter[1] + 35),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    if isShow == 1:
        cv.imshow(f"{ImageName}", image)
        cv.waitKey(0)
    if isSave == 1:
        ImageFolder = rpd.ImagesFolder + f"/{folderName}"
        try:
            if not os.path.exists(ImageFolder):
                os.makedirs(ImageFolder)
        except OSError:
            print('Error: Creating directory of data')
        
        cv.imwrite(ImageFolder+f"/{ImageName}", image)
    
    return Image, ImageName, ballCenter, blueCenter, blueAngle, redCenter, redAngle

def examineFrames(folderName, isShow = 0, saveName = "folder1", isSave = 0):
    imageLen = len(os.listdir(folderName))
    frame = (cv.imread(folderName + "/frame0.jpg"))
    height, width, layers = frame.shape

    if isSave == 1:
        path = rpd.ImagesFolder + f"/{saveName}"
        path2 = rpd.DataFolder + f"/{saveName}"
        workbook = xlsxwriter.Workbook( f"{path2}.xlsx" )
        worksheet = workbook.add_worksheet()
        worksheet.write(0,0 ,"FRAME")
        worksheet.write(0,1 ,"MS")
        worksheet.write(0,2 ,"BALL(x,y)")
        worksheet.write(0,3 ,"BOT[B](x,y)")
        worksheet.write(0,4 ,"BOT[B]°")
        worksheet.write(0,5 ,"BOT[R](x,y)")
        worksheet.write(0,6 ,"BOT[R]°")

        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            print('Error: Creating directory of data')

    for i in range(imageLen):
        img = cv.imread(folderName + f"/frame{i}.jpg")
        try:
            start = datetime.datetime.now()
            img2, ImageName, ballCenter, blueCenter, blueAngle, redCenter, redAngle = examineFrame(img, f"/frame{i}.jpg", 0)
            stop = datetime.datetime.now()
            workTime = stop - start
            milis = int(workTime.total_seconds() * 1000)

            if isShow == 1:
                cv.imshow(f"/frame{i}.jpg", img2)
                cv.waitKey(0)
            if isSave == 1:
                cv.imwrite(path + f"/frame{i}.jpg", img2)
                worksheet.write(i+2,0 , f"frame{i}")
                worksheet.write(i+2,1 , f"[{milis}]")
                worksheet.write(i+2,2 , f"({ballCenter[0]},{ballCenter[1]})")
                worksheet.write(i+2,3 , f"({blueCenter[0]},{blueCenter[1]})")
                worksheet.write(i+2,4 , f"{blueAngle}°")
                worksheet.write(i+2,5 , f"({redCenter[0]},{redCenter[1]})")
                worksheet.write(i+2,6 , f"{redAngle}°")
        except:
            print(f"frame{i}.jpg can not readed")

    if(isSave == 1):
        rpd.frame2Video(path, f"{saveName}.mp4", 1)
        workbook.close()

def examineVideo(videoName, isShow = 0, saveName = "folder1", isSave = 0):
    img_fold = rpd.video2Frame(videoName,saveName)
    examineFrames(img_fold, 0, saveName, 1)

