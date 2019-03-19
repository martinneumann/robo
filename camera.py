import cv2
import numpy as np
from matplotlib import pyplot as plt
import struct


def calibrate():
    cap = cv2.VideoCapture(-1)
    ''' 1. CALIBRATE GESTURE AREA '''

    # four points that describe the edges of the board
    # indicated by circles that are detected
    board_edges = np.array([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [
                           0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]])
    cons_edges = np.array([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [
                          0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]])
    edge_buf = []

    # index for number of runs
    a = 1
    while(1):
        # Capture frame-by-frame
        _ret, frame = cap.read()

        if (not frame is None):

            # Our operations on the frame come here
            retval, img = cap.read(frame)

            # to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # edge detection (canny)
            edged = cv2.Canny(gray, 150, 200)

            # denoise
            #edged = cv2.fastNlMeansDenoisingColored(edged,None,10,10,7,21)

            # show edges
            # cv2.imshow('canny', edged)

            # find contours
            ret, thresh = cv2.threshold(edged, 127, 255, 0)
            _, contours, h = cv2.findContours(thresh, 1, 2)

            o = 0
            i = 0
            print("Shapes found: " + str(len(contours)))
            for cnt in contours:
                approx = cv2.approxPolyDP(
                    cnt, 0.01*cv2.arcLength(cnt, True), True)
                if len(approx) > 10:
                    if (cv2.contourArea(cnt) > 300 and cv2.contourArea(cnt) < 1800):
                        if (len(edge_buf) < 12):
                            cv2.drawContours(img, [cnt], 0, (0, 255, 255), -1)

                        # find center
                        M = cv2.moments(cnt)
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        if (len(edge_buf) < 9):
                            cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
                            cv2.putText(frame, str(cX) + ", " + str(cY), (cX - 20, cY - 20),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                            o = o + 1
                        if i < 12:
                            board_edges[i] = [cX, cY]
                            i = i + 1
                '''if len(approx) > 3 and len(approx) < 5:
                    if (cv2.contourArea(cnt) >300):
                        if (len(edge_buf) < 12):
                            cv2.drawContours(img,[cnt],0,(0,0,255),-1)
                            o = o + 1
                '''

            o = o/2
            # if a == 1:
            #cons_edges = board_edges
            if o == 6:
                for index, edge in enumerate(cons_edges):
                    if a == 0:
                        break
                    edge = [(edge[0] + board_edges[index][0])/2,
                            (edge[1] + board_edges[index][1])/2]
                    cons_edges[index] = edge
                edge_buf.append(board_edges)
                print("Valid runs: " + str(a))
                print("Valid shapes found: " + str(o))
                a = a+1
            else:
                print("Number of valid shapes found: " +
                      str(o) + ". Discarding results. \r")

            if (len(edge_buf) > 12):
                av_edge = np.average(edge_buf, axis=0)
                print(av_edge)
                #print("Board edges are: \n" + str(np.average(edge_buf, axis=0)))
                for elem in av_edge:
                    cv2.circle(img, (int(elem[0]), int(
                        elem[1])), 7, (255, 0, 0), -1)
                    cv2.putText(img, (str(elem[0]) + ", " + str(elem[1])), (int(elem[0]) - 20, int(elem[1]) - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    cv2.imshow('frame', img)
                if cv2.waitKey(50) & 0xFF == ord('q'):
                    break
                input_ = input(
                    "Is this calibration correct? Press Y/N to continue.")
                if (input_ == "y"):
                    cap.release()
                    cv2.destroyAllWindows()
                    break
                else:
                    edge_buf = []

            # Display the resulting frame
            cv2.imshow('frame', img)
            if cv2.waitKey(50) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()


def detectGesture():
    cap = cv2.VideoCapture(-1)
    match = cv2.imread("data/000.png")
    # match = cv2.cvtColor(match, cv2.COLOR_BGR2GRAY)
    w = 640
    h = 480
    while(1):
        _ret, frame = cap.read()
        if (not frame is None):

            # Our operations on the frame come here
            retval, img = cap.read(frame)

            # skin detection algorithm
            lower = np.array([0, 48, 80], dtype="uint8")
            upper = np.array([20, 255, 255], dtype="uint8")

            converted = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            skinMask = cv2.inRange(converted, lower, upper)

            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
            skinMask = cv2.erode(skinMask, kernel, iterations=2)
            skinMask = cv2.dilate(skinMask, kernel, iterations=2)

            skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
            skin = cv2.bitwise_and(frame, frame, mask=skinMask)
            # ret, thresh = cv2.threshold(edged, 127,255,0)
            # _, contours, h = cv2.findContours(skin, 1, 2)
            # print("found " + str(len(contours)))
            result_ = cv2.matchTemplate(skin, match,
                                        cv2.TM_SQDIFF)
            print(str(result_))
            loc = np.where(result_ >= 0.80)
            # _, maxVal, _, maxLoc = cv2.minMaxLoc(result_)
            print(str(np.ndim(loc)))
            print("max loc: " + str(loc[0]) + ", " + str(loc[1]))
            for pt in zip(*loc[::-1]):
                cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h),
                              (0, 255, 255), 2)

                cv2.imshow("images", np.hstack([frame, skin]))

            # if the 'q' key is pressed, stop the loop
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()

    return ("A1")
