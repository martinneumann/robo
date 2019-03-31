import cv2
import numpy as np
from matplotlib import pyplot as plt
import struct
import random as rng
import math


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
            # edged = cv2.fastNlMeansDenoisingColored(edged,None,10,10,7,21)

            # show edges
            # cv2.imshow('canny', edged)

            # find contours
            ret, thresh = cv2.threshold(edged, 200, 255, 0)
            thresh = cv2.dilate(thresh, None, iterations=1)
            thresh = cv2.erode(thresh, None, iterations=1)
            testimg, contours, h = cv2.findContours(thresh, 1, 2)

            o = 0
            i = 0
            print("Shapes found: " + str(len(contours)))
            for cnt in contours:
                approx = cv2.approxPolyDP(
                    cnt, 0.05*cv2.arcLength(cnt, True), True)
                if (len(approx) == 3) and cv2.contourArea(cnt) > 100 and cv2.contourArea(cnt) < 900:

                    # find center
                    M = cv2.moments(cnt)
                    if (len(M) > 4):
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        if (len(edge_buf) < 12):
                            cv2.drawContours(img, [cnt], 0, (0, 255, 255), -1)
                            cv2.putText(frame, str(cX) + ", " + str(cY), (cX - 20, cY - 20),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                            o = o + 1
                        board_edges[i] = [cX, cY]
                        i = i + 1

            o = o/2
            # if a == 1:
            # cons_edges = board_edges
            if o == 4:
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

            if (len(edge_buf) == 12):
                print("found edges: " + str(board_edges))
                av_edge = np.average(edge_buf, axis=0)
                print(av_edge)
                # print("Board edges are: \n" + str(np.average(edge_buf, axis=0)))
                for elem in av_edge:
                    cv2.circle(img, (int(elem[0]), int(
                        elem[1])), 7, (255, 0, 0), -1)
                    cv2.putText(img, (str(elem[0]) + ", " + str(elem[1])), (int(elem[0]) - 20, int(elem[1]) - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    cv2.imshow('robot view', img)
                if cv2.waitKey(50) & 0xFF == ord('q'):
                    break

                cap.release()
                cv2.destroyAllWindows()
                print str(av_edge[0])
                return av_edge

            # Display the resulting frame
            cv2.imshow('robot view', img)
            if cv2.waitKey(1000) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()


def getDistance(x1, y1, x2, y2):
    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))


def detectGesture():
    camera = cv2.VideoCapture(-1)
    # match = cv2.imread("data/000.png")
    # match = cv2.cvtColor(match, cv2.COLOR_BGR2GRAY)
    w = 640
    h = 480

    avg_points = []
    avg_point = [320, 240]

    lower = np.array([0, 48, 80], dtype="uint8")
    upper = np.array([20, 255, 255], dtype="uint8")
   # keep looping over the frames in the video
    while True:
            # grab the current frame
        (grabbed, frame) = camera.read()

        # if we are viewing a video and we did not grab a
        # frame, then we have reached the end of the video

        # resize the frame, convert it to the HSV color space,
        # and determine the HSV pixel intensities that fall into
        # the speicifed upper and lower boundaries
        converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        skinMask = cv2.inRange(converted, lower, upper)

        # apply a series of erosions and dilations to the mask
        # using an elliptical kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        skinMask = cv2.erode(skinMask, kernel, iterations=2)
        skinMask = cv2.dilate(skinMask, kernel, iterations=2)

        # blur the mask to help remove noise, then apply the
        # mask to the frame
        skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
        skin = cv2.bitwise_and(frame, frame, mask=skinMask)

        skin_new = cv2.Canny(skin, 100,  255)
        skin_new = cv2.dilate(skin_new, None, iterations=3)
        skin_new = cv2.erode(skin_new, None, iterations=3)
        _, contours, _ = cv2.findContours(
            skin_new, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # show the skin in the image along with the mask
        hull_list = []
        # for i in range(len(contours)):
        #    hull = cv2.convexHull(contours[i])
        #    hull_list.append(hull)
        # Draw contours + hull results

        # hull = cv2.convexHull(skin_new)
        # hull_list.append(hull)
        drawing = np.zeros(
            (skin_new.shape[0], skin_new.shape[1], 3), dtype=np.uint8)
        i = 0

        numberofpoints = 0
        for contour in contours:
            for point in contour:
                numberofpoints = numberofpoints + 1
        allcountours = np.zeros((numberofpoints, 1, 2), dtype=np.int32)

        count = 0
        for contour in contours:
            for point in contour:
                allcountours[count][0] = [point[0][0], point[0][1]]
                count = count + 1
        cnt = allcountours

        color = (rng.randint(0, 256), rng.randint(
            0, 256), rng.randint(0, 256))
        # cv2.drawContours(drawing, contours, i, color)
        # _, triangle = cv2.minEnclosingTriangle(cnt)
        # center, radius = cv2.minEnclosingCircle(cnt)
        hull = cv2.convexHull(cnt, returnPoints=False)

        # print("tri " + str(triangle[0][0]) +
        #      str(triangle[1][0]) + str(triangle[2][0]))
        # pt1 = (triangle[0][0][0], triangle[0][0][1])
        # pt2 = (triangle[1][0][0], triangle[1][0][1])
        # pt3 = (triangle[2][0][0], triangle[2][0][1])

        # cv2.line(skin_new, pt1, pt2, color)
        # cv2.line(skin_new, pt2, pt3, color)
        # cv2.line(skin_new, pt3, pt1, color)
        '''
        dist1 = getDistance(pt1[0], pt1[1], pt2[0], pt2[1])
        dist2 = getDistance(pt2[0], pt2[1], pt3[0], pt3[1])
        dist3 = getDistance(pt3[0], pt3[1], pt1[0], pt1[1])
        point = [0, 0]
        if (dist1 < dist2) and (dist1 < dist3):
            # dist 1 is smallest -> pt3
            point = pt3
        if (dist2 < dist1) and (dist2 < dist3):
            point = pt1
        if (dist3 < dist1) and (dist3 < dist2):
            point = pt2
        avg_points.append(point)
        '''
        # cv2.putText(skin_new, str(point), (point[0], point[1]),
        #            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        # print("distances: " + str(dist1) + ", " +
        #      str(dist2) + ", " + str(dist3))

        # cv2.line(skin_new, triangle[1], triangle[2], color)
        # cv2.line(skin_new, triangle[2], triangle[0], color)
        # cv2.circle(skin_new, (int(center[0]), int(
        #    center[1])), int(radius), color, 2)
        if hull is not None:
            defects = cv2.convexityDefects(cnt, hull)
            print("hull: " + str(hull))
            print("defects: " + str(defects))
            print(str(defects[2][0]))
            # cv2.putText(skin_new, str(defects[2][0]), (int(defects[2][0]), int(
            #    defects[2][1])),
            #    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            # cv2.drawContours(skin_new, hull, i, color)
            farthest_dist = 1
            farthest_point = ()
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                cv2.line(skin_new, start, end, color, 2)
                # cv2.circle(skin_new, far, 5, color, -1)

            ret, thresh = cv2.threshold(frame, 200, 255, 0)

            defectsarray = []
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                defectsarray.append([start[0], start[1]])
            print(str(defectsarray))

            max_dist = 0
            farthest_point = []
            M = cv2.moments(np.int32(defectsarray))

            # get centroid
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.putText(skin_new, "centroid", (cX - 25, cY - 25),
                        cv2.FONT_HERSHEY_PLAIN, 1, color)
            cv2.circle(skin_new, (cX, cY), 5, (255, 255, 255), 1)

            for point in defectsarray:
                # calculate farthesst point
                if (getDistance(cX, cY, point[0], point[1]) > max_dist) and (point[0] > 40) and (point[0] < 600) and (point[1] < 440) and (point[1] > 40):
                    max_dist = getDistance(cX, cY, point[0], point[1])
                    farthest_point = point
                    print("new farthest point: " + str(point) +
                          " with distance: " + str(max_dist))
                    cv2.circle(
                        skin_new, (farthest_point[0], farthest_point[1]), 20, (255, 255, 0), 1)
                    cv2.putText(skin_new, str(farthest_point), (farthest_point[0] + 10, farthest_point[1] + 10),
                                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))

            # rect = cv2.minAreaRect(cnt)

            # box = cv2.boxPoints(rect)
            # box = np.int0(box)
            # cv2.drawContours(skin_new, [box], 0, color, 2)
            '''
            ellipse = cv2.fitEllipse(cnt)

            skin_new = cv2.ellipse(skin_new, ellipse, (0, 255, 0), 2)

            rows, cols = skin_new.shape[:2]
            [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
            lefty = int((-x*vy/vx) + y)
            righty = int(((cols-x)*vy/vx)+y)
            print("line: " + str(vx) + ", " + str(vy) +
                    ", " + str(x) + ", " + str(y))
            if (vx > 0 and vy > 0 and x > 0 and y > 0):
                skin_new = cv2.line(skin_new, (cols-1, righty),
                                    (0, lefty), color, 2)
            
                                    '''
            if (farthest_point != None) and (len(farthest_point) > 0):
                avg_points.append(farthest_point)
            print("average points" + str(avg_points))
            i += 1
            # Show in a window
            total_x = 0
            avg_x = 0
            total_y = 0
            avg_y = 0
            if (len(avg_points) > 50):
                for pt in avg_points:
                    total_x += pt[0]
                    total_y += pt[1]
                avg_x = total_x / len(avg_points)
                avg_y = total_y / len(avg_points)
                print("found point: " + str(avg_x) + ", " + str(avg_y))
                return (avg_x, avg_y)
        cv2.imshow('Contours', skin_new)

        # if the 'q' key is pressed, stop the loop
        if cv2.waitKey(5000) & 0xFF == ord("q"):
            break

    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
