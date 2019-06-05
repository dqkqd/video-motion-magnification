import cv2
import numpy as np

def combine(video1, video2, video_output):
    capture1 = cv2.VideoCapture(video1)
    capture2 = cv2.VideoCapture(video2)

    frame_count1 = int(capture1.get(cv2.CAP_PROP_FRAME_COUNT))
    width1 = int(capture1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height1 = int(capture1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps1 = int(capture1.get(cv2.CAP_PROP_FPS))

    frame_count2 = int(capture2.get(cv2.CAP_PROP_FRAME_COUNT))
    width2 = int(capture2.get(cv2.CAP_PROP_FRAME_WIDTH))
    height2 = int(capture2.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps2 = int(capture2.get(cv2.CAP_PROP_FPS))

    # setup output
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    writer = cv2.VideoWriter(video_output, fourcc, fps1, (2 * width1, height1), 1)

    i = 0
    print('\nCombining: %s' %video_output)
    while capture1.isOpened() and capture2.isOpened():
        ret1, frame1 = capture1.read()
        ret2, frame2 = capture2.read()
        
        if not ret1 or not ret2:
            break

        new_frame = np.concatenate((frame1, frame2), axis=1)
        writer.write(new_frame)
        i = i + 1
        print('%d' %i, end = ' * ')

    print('\nCompleted')

