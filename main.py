from filterbank import *
import os
import sys
import cv2
    
import sys
import numpy as np

from pyr2arr import Pyramid2arr
from temporal_filters import IdealFilterWindowed, ButterBandpassFilter

from image_converter import rgb2ycc, ycc2rgb, scale_range
from combine_video import combine

def phaseBasedMagnify(vidFname, maxFrames, windowSize, factor, fpsForBandPass, lowFreq, highFreq, threshold, filter_type):

    # initialize the steerable complex pyramid
    steer = Steerable(5)
    pyArr = Pyramid2arr(steer)

    print ("Reading:", vidFname, end = '')

    # get vid properties
    vidReader = cv2.VideoCapture(vidFname)
        
    vidFrames = int(vidReader.get(cv2.CAP_PROP_FRAME_COUNT))    
    width = int(vidReader.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidReader.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(vidReader.get(cv2.CAP_PROP_FPS))
    func_fourcc = cv2.VideoWriter_fourcc

    if np.isnan(fps):
        fps = 30

    print (' %d frames' % vidFrames, end = '')
    print (' (%d x %d)' % (width, height), end = '')
    print (' FPS:%d' % fps)

    

    # how many frames
    nrFrames = min(vidFrames, maxFrames)

    # read video
    #print steer.height, steer.nbands

    # setup temporal filter
    if filter_type == 0:
        filter_ = IdealFilterWindowed(windowSize, lowFreq, highFreq, fps=fpsForBandPass, outfun=lambda x: x[0])
        # output video filename
        vidFnameOut = vidFname + '-MagIdeal-fac%d-fps%d-lo%.2f-hi%.2f.avi' % (factor, fpsForBandPass, lowFreq, highFreq)

    else:
        filter_ = ButterBandpassFilter(1, lowFreq, highFreq, fps=fpsForBandPass)
        # output
        vidFnameOut = vidFname + '-MagButter-fac%d-fps%d-lo%.2f-hi%.2f.avi' % (factor, fpsForBandPass, lowFreq, highFreq)

    # combined video name
    vidCombined = vidFnameOut + '-Combined.avi'

    # video Writer
    fourcc = func_fourcc('M', 'J', 'P', 'G')
    vidWriter = cv2.VideoWriter(vidFnameOut, fourcc, int(fps), (width,height), 1)
    print ('Writing:', vidFnameOut)

    scale = scale_range(width, height, threshold)
    print('Scaled %d' %scale)
    print ('FrameNr:', end = ' ')
    for frameNr in range( nrFrames + windowSize ):
        print (frameNr, end = ' ')
        sys.stdout.flush() 

        if frameNr < nrFrames:
            # read frame
            _, im = vidReader.read()
               
            if im is None:
                # if unexpected, quit
                break

            if scale != 1:
                im = cv2.resize(im, (width // scale, height // scale))
            
            grayIm, cr, cb = rgb2ycc(im)

            # get coeffs for pyramid
            coeff = steer.buildSCFpyr(grayIm)

            
            # add image pyramid to video array
            # NOTE: on first frame, this will init rotating array to store the pyramid coeffs                 
            arr = pyArr.p2a(coeff)
            
            phases = np.angle(arr)
            
            # add to temporal filter
            filter_.update([phases])

            # try to get filtered output to continue            
            try:
                filteredPhases = filter_.next()
            except StopIteration:
                continue

            print('*', end = ' ')
            
            # motion magnification
            magnifiedPhases = (phases - filteredPhases) + filteredPhases*factor
            
            # create new array
            newArr = np.abs(arr) * np.exp(magnifiedPhases * 1j)

            # create pyramid coeffs     
            newCoeff = pyArr.a2p(newArr)
            
            # reconstruct pyramid
            out = steer.reconSCFpyr(newCoeff)

            # clip values out of range
            out[out>255] = 255
            out[out<0] = 0
            
            # make a RGB image
            rgbIm = ycc2rgb(out, cr, cb)

            if scale != 1:
                h,w,c = rgbIm.shape
                rgbIm = cv2.resize(rgbIm, (w * scale, h * scale))
            
            #write to disk
            res = cv2.convertScaleAbs(rgbIm)
            vidWriter.write(res)

    # free the video reader/writer
    vidReader.release()
    vidWriter.release()   


    # combine two video
    combine(vidFname, vidFnameOut, vidCombined)

################# main script
maxFrames=60000
windowSize=30
threshold=150000

if __name__ == "__main__":

    _, video_name, factor, lowfreq, highfreq = sys.argv

    print('Video name: %s, factor = %s, lowfreq = %s, highfreq = %s' %(video_name, factor, lowfreq, highfreq))
    phaseBasedMagnify(video_name, maxFrames, windowSize,
                      factor = int(factor) , fpsForBandPass = 1,
                      lowFreq = float(lowfreq), highFreq = float(highfreq),
                      threshold = threshold, filter_type = 1)
    

