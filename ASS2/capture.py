#This code is written by Utkarsh Goel for MSU CSCI 442 Computer Vision
import cv2 as cv
import numpy as np
import os

def capture_webcam():
    camera = cv.VideoCapture(0)
    ret_val, tempImg = camera.read()
    tempImg = cv.resize(tempImg, (320,240))
    imgAcw = np.zeros((tempImg.shape), np.float32)
    while True:
        ret_val, img = camera.read()
        if ret_val:
            img = cv.flip(img, 1)
            cv.namedWindow('regular', cv.WINDOW_NORMAL)
            cv.resizeWindow('regular', 320,240)
            cv.moveWindow('regular', 0, 0)
            img = cv.resize(img, (320,240))
            cv.imshow('regular', img)
            imgBlank = img.copy()

            cv.namedWindow('grayscale', cv.WINDOW_NORMAL)
            cv.resizeWindow('grayscale', 320,240)
            cv.moveWindow('grayscale', 320, 0)
            grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            cv.imshow('grayscale', grayImg)

            cv.namedWindow('capture clone - image 1', cv.WINDOW_NORMAL)
            cv.resizeWindow('capture clone - image 1', 320,240)
            cv.moveWindow('capture clone - image 1', 0, 265)
            

            #brightening the image
            img_yuv = cv.cvtColor(img, cv.COLOR_BGR2YUV)
            img_yuv[:,:,0] = cv.equalizeHist(img_yuv[:,:,0])
            img_output = cv.cvtColor(img_yuv, cv.COLOR_YUV2BGR)
            cv.imshow('capture clone - image 1', img_output)
            blur = cv.GaussianBlur(img_output, (5,5),0)

            cv.accumulateWeighted(blur, imgAcw, 0.32)
            cv.convertScaleAbs(imgAcw, imgBlank, 1.0, 0.0)
            diff = cv.absdiff(blur, imgBlank)
            diffGray =cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
            
            ret,thresh = cv.threshold(diffGray,2,255,0)
            blur1 = cv.GaussianBlur(thresh, (5,5), 1.5)
            ret,thresh1 = cv.threshold(blur1,250,255,0)
            im2, contours, hierarchy = cv.findContours(thresh1,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
            
            cv.drawContours(thresh1, contours, -1, (0,255,0), 2)
            
            cv.namedWindow('new frame', cv.WINDOW_NORMAL)
            cv.resizeWindow('new frame', 320,240)
            cv.moveWindow('new frame', 320, 265)
            cv.imshow('new frame', thresh1)

        if cv.waitKey(1) == 27:
            break
        
    cv.destroyAllWindows()
    os._exit(0)

def main():
    capture_webcam()

if __name__ == '__main__':
    main()
