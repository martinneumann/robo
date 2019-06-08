import cv2
import numpy as np
from matplotlib import pyplot as plt
import struct
import random as rng
import math
import operator


def draw_positions(position, calibratedPosition, img):
    # position = "000A10C10E10G10B20D20F20H20A30C30E30G30B80D80F80H80A70C70E70G70B60D60F60H6000"
    # calibratedPosition is board_fields
    # img is the cv2 image where drawing takes place



    letter = ["A", "B", "C", "D", "E", "F", "G", "H", "X"]

    white_pos = position[2:38]      # values for white pieces   
    black_pos = position[38:74]     # values for black pieces

    for x in range(12):
        xx = 3 * x
        peace_w = white_pos[xx:xx+3]
        peace_b = black_pos[xx:xx+3]
        if peace_w != "000":
            # loop over position, draw circle if not zero
            pos = calibratedPosition[peace_w[1:3]]
            print("point for drawing: " + str(pos))
            cv2.circle(img, (pos[0], pos[1]),
                       11, (220, 220, 220), -1)
            cv2.circle(img, (pos[0], pos[1]),
                       12, (150, 100, 200), 1)
        if peace_b != "000":
            pos = calibratedPosition[peace_b[1:3]]
            print("point for drawing: " + str(pos))
            cv2.circle(img, (pos[0], pos[1]),
                       12, (0, 0, 0), -1)
            cv2.circle(img, (pos[0], pos[1]),
                       12, (150, 100, 200), 1)
    # cv2.imshow("displayWindow", img)
                # matrix_list[y_cor_b][x_cor_b] = symbole_b




def draw_hand_rect(self, frame):
    rows, cols, _ = frame.shape

    self.hand_row_nw = np.array([6*rows/20, 6*rows/20, 6*rows/20, 10 *
                                 rows/20, 10*rows/20, 10*rows/20, 14*rows/20, 14*rows/20, 14*rows/20])

    self.hand_col_nw = np.array([9*cols/20, 10*cols/20, 11*cols/20, 9 *
                                 cols/20, 10*cols/20, 11*cols/20, 9*cols/20, 10*cols/20, 11*cols/20])

    self.hand_row_se = self.hand_row_nw + 10
    self.hand_col_se = self.hand_col_nw + 10

    size = self.hand_row_nw.size
    for i in xrange(size):
        cv2.rectangle(frame, (self.hand_col_nw[i], self.hand_row_nw[i]), (
            self.hand_col_se[i], self.hand_row_se[i]), (0, 255, 0), 1)
        black = np.zeros(frame.shape, dtype=frame.dtype)
        frame_final = np.vstack([black, frame])
        return frame_final


def set_hand_hist(self, frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    roi = np.zeros([90, 10, 3], dtype=hsv.dtype)

    size = self.hand_row_nw.size
    for i in xrange(size):
        roi[i*10:i*10+10, 0:10] = hsv[self.hand_row_nw[i]
            :self.hand_row_nw[i]+10, self.hand_col_nw[i]:self.hand_col_nw[i]+10]

    self.hand_hist = cv2.calcHist(
        [roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
    cv2.normalize(self.hand_hist, self.hand_hist, 0, 255, cv2.NORM_MINMAX)


def apply_hist_mask(frame, hist):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)

    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    cv2.filter2D(dst, -1, disc, dst)

    ret, thresh = cv2.threshold(dst, 100, 255, 0)
    thresh = cv2.merge((thresh, thresh, thresh))

    cv2.GaussianBlur(dst, (3, 3), 0, dst)

    res = cv2.bitwise_and(frame, thresh)
    return res


def draw_final(self, frame, hand_detection):
    hand_masked = image_analysis.apply_hist_mask(
        frame, hand_detection.hand_hist)

    contours = image_analysis.contours(hand_masked)
    if contours is not None and len(contours) > 0:
        max_contour = image_analysis.max_contour(contours)
        hull = image_analysis.hull(max_contour)
        centroid = image_analysis.centroid(max_contour)
        defects = image_analysis.defects(max_contour)

        if centroid is not None and defects is not None and len(defects) > 0:
            farthest_point = image_analysis.farthest_point(
                defects, max_contour, centroid)

            if farthest_point is not None:
                self.plot_farthest_point(frame, farthest_point)


def calibrate():
    cap = cv2.VideoCapture(-1)
    ''' 1. CALIBRATE GESTURE AREA '''

    # four points that describe the edges of the board
    # indicated by circles that are detected

    cons_edges = np.array([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [
                          0, 0], [0, 0]])
    edge_buf = []

    board_fields = {}

    # index for number of runs
    a = 1
    while(1):
        board_edges = np.array([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [
                               0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]])
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
            contours, h = cv2.findContours(thresh, 1, 2)

            o = 0  # valid shapes in this run
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
                        print("found point: " + str(cX) + "," + str(cY))
                        if (len(edge_buf) < 12):
                            cv2.drawContours(img, [cnt], 0, (0, 255, 255), -1)
                            cv2.putText(frame, str(cX) + ", " + str(cY), (cX - 20, cY - 20),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                            o = o + 1
                        board_edges[i] = [cX, cY]
                        i = i + 1

            print("board_edges: " + str(board_edges))

            print("after cleaning: " + str(board_edges))
            if (len(board_edges) < 4):
                print("too few edges found, continuing")
                continue
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
                board_edges = [board_edges[0], board_edges[2],
                               board_edges[4], board_edges[6]]
                edge_buf.append(board_edges)
                print("Valid runs: " + str(a))
                print("Valid shapes found: " + str(edge_buf))
                a = a+1
            else:
                print("Number of valid shapes found: " +
                      str(o) + ". Discarding results. \r")

            if (len(edge_buf) == 12):
                print("found edges: " + str(board_edges))
                av_edge = np.average(edge_buf, axis=0)
                # print(av_edge)
                # print("Board edges are: \n" + str(np.average(edge_buf, axis=0)))
                for elem in av_edge:
                    cv2.circle(img, (int(elem[0]), int(
                        elem[1])), 7, (255, 0, 0), -1)
                    cv2.putText(img, (str(elem[0]) + ", " + str(elem[1])), (int(elem[0]) - 20, int(elem[1]) - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    cv2.imshow('displayWindow', img)

                # put board
                edges = []
                edges = av_edge

                # print(str(edges))

                edges = sorted(edges, key=lambda x: x[0])

                # print("edegs: " + str(edges))

                print("successfully calibrated.")
                print("board edges are: " +
                      str(edges[0]) + ", " + str(edges[1]) + ", " + str(edges[2]) + ", " + str(edges[3]))
                print("sorting edges...")

                # sort points
                # 1. sort by x value
                sorted_edges = []
                lowest_x = [800, 800]
                k = 0
                for point in edges:
                    if (len(sorted_edges) > 0):
                        for pt in sorted_edges:
                            if point[0] < pt[0]:
                                sorted_edges.insert(k, point)
                                k += 1
                                break
                            if (k == len(sorted_edges)):
                                sorted_edges.append(point)
                                k += 1
                                break
                    else:
                        sorted_edges.append(point)
                        k += 1
                print("after sorting: " + str(sorted_edges))
                if (sorted_edges[0][1] > sorted_edges[1][1]):
                    # change positions if y of 1 is larger than y of 0
                    tmp_edge = sorted_edges[0]
                    sorted_edges[0] = sorted_edges[1]
                    sorted_edges[1] = tmp_edge

                if (sorted_edges[2][1] > sorted_edges[3][1]):
                    tmp_edge = sorted_edges[2]
                    sorted_edges[2] = sorted_edges[3]
                    sorted_edges[3] = tmp_edge

                print("After swapping: " + str(sorted_edges))
                edges = sorted_edges

                print("calculating fields...")

                dx = (edges[2][0] - edges[0][0]) / 10
                dx2 = (edges[3][0] - edges[1][0]) / 10
                dy = (edges[2][1] - edges[3][1]) / 10
                dy2 = (edges[0][1] - edges[1][1]) / 10

                # print("distorsion: " + str(dx1) + ", " +
                #      str(dx2) + "; " + str(dy1) + ", " + str(dy2))
                x_dist = (edges[3][0] - edges[2][0])/10
                print("x dist: " + str(x_dist))
                y_dist = (edges[3][1] - edges[2][1])/10
                print("y dist: " + str(y_dist))

                letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
                y_val = edges[2][1]   # first y value
                x_val = edges[2][0]   # first x value

                # first row
                # top_row
                print("x val: " + str(x_val) + ", y val: " + str(y_val))
                field_edges = []

                # top row
                top_row = getEightPointsBetween(img,
                                                edges[2][0], edges[2][1], edges[0][0], edges[0][1])

                for element in top_row:
                    element = [int(element[0]), int(element[1])]
                    print(str(element))
                print("top row: " + str(top_row))

                bottom_row = getEightPointsBetween(img,
                                                   edges[3][0], edges[3][1], edges[1][0], edges[1][1])

                # bottom row
                for element in bottom_row:
                    element = [int(element[0]), int(element[1])]
                    print(str(element))
                print("bottom row: " + str(bottom_row))

                fields = []
                # fields in between
                for i in range(len(top_row)):
                    # get circles between rows
                    tmplist = getEightPointsBetween(img,
                                                    top_row[i][0], top_row[i][1], bottom_row[i][0], bottom_row[i][1])

                    # convert circles to fields with key
                    for x in range(len(tmplist)):
                        tmp = str(letters[i] + numbers[x])
                        board_fields[tmp] = tmplist[x]

                print("board fields are: " + str(board_fields))

                if cv2.waitKey(50) & 0xFF == ord('q'):
                    break

                cap.release()
                # cv2.destroyAllWindows()
                # print str(av_edge[0])
                return board_fields, img

            # Display the resulting frame
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            cv2.imshow('displayWindow', img)

    cap.release()
    # cv2.destroyAllWindows()


def getEightPointsBetween(img, x1, y1, x2, y2):
    print("getting points between: " + str(x1) + "," +
          str(y1) + " and " + str(x2) + "," + str(y2))
    x_dist = (x2 - x1) / 9
    y_dist = (y2 - y1) / 9
    x = x1 + x_dist
    y = y1 + y_dist
    points = []
    for i in range(8):
        x = int(x)
        y = int(y)
        points.append((x, y))
        cv2.circle(img, (x, y),
                   5, (255, 255, 0))
        x += x_dist
        y += y_dist

    return points


def addPoint(x1, y1, x2, y2):
    return [x1 + x2, y1 + y2]


def subtractPoint(x1, y1, x2, y2):
    return [x2 - x1, y2 - y1]


def getDistance(x1, y1, x2, y2):
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))


def detectGesture(position, board_fields):
    camera = cv2.VideoCapture(-1)
    # match = cv2.imread("data/000.png")
    # match = cv2.cvtColor(match, cv2.COLOR_BGR2GRAY)
    w = 640
    h = 480

    average_x = 0
    average_y = 0
    variance_x = 1000
    variance_y = 1000

    avg_points = []
    avg_point = [320, 240]

    lower = np.array([0, 20, 10], dtype="uint8")
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
        # skinMask = cv2.erode(skinMask, kernel, iterations=2)
        # skinMask = cv2.dilate(skinMask, kernel, iterations=1)
        skinMask = cv2.morphologyEx(skinMask, cv2.MORPH_OPEN, kernel)

        # blur the mask to help remove noise, then apply the
        # mask to the frame
        skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
        skin = cv2.bitwise_and(frame, frame, mask=skinMask)
        draw_positions(position, board_fields, frame)
        cv2.imshow("displayWindow", frame)
        skin_new = cv2.Canny(skin, 100,  255)
        skin_new = cv2.dilate(skin_new, None, iterations=1)
        # skin_new = cv2.erode(skin_new, None, iterations=1)
        contours, _ = cv2.findContours(
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

        if hull is not None:
            defects = cv2.convexityDefects(cnt, hull)
            # print("hull: " + str(hull))
            # print("defects: " + str(defects))
            # print(str(defects[2][0]))
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
            # print(str(defectsarray))

            max_dist = 0
            farthest_point = []
            M = cv2.moments(np.int32(defectsarray))

            # get centroid
            if (M["m00"] != 0):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX = 0
                cY = 0  # @TODO: check
            cv2.putText(skin_new, "centroid", (cX - 25, cY - 25),
                        cv2.FONT_HERSHEY_PLAIN, 1, color)
            cv2.circle(skin_new, (cX, cY), 5, (100, 255, 255), 1)

            for point in defectsarray:
                # calculate farthesst point
                if (getDistance(cX, cY, point[0], point[1]) > max_dist) and (point[0] > 40) and (point[0] < 600) and (point[1] < 440) and (point[1] > 40):
                    max_dist = getDistance(cX, cY, point[0], point[1])
                    farthest_point = point
                    # print("new farthest point: " + str(point) +
                    #      " with distance: " + str(max_dist))
                    cv2.circle(
                        skin_new, (farthest_point[0], farthest_point[1]), 20, (255, 255, 0), 1)
                    cv2.putText(skin_new, "farthest point: " + str(farthest_point), (farthest_point[0] + 10, farthest_point[1] + 10),
                                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))

            if (farthest_point != None) and (len(farthest_point) > 0):
                avg_points.append(farthest_point)
            # print("average points" + str(avg_points))
            # raw_input()
            i += 1

            if (len(avg_points) > 40):
                avg_points.pop(0)
                print("Length of avg_points is: " +
                      str(len(avg_points)) + ", removing first element...")

            total_x = 0
            avg_x = 0
            total_y = 0
            avg_y = 0

            if (len(avg_points) > 1):
                print("Calculating running average and variance...")
                sum_x = 0
                sum_y = 0
                for point in avg_points:
                    sum_x += point[0]
                    sum_y += point[1]
                # calculated average of all found points
                average_x = sum_x / len(avg_points)
                average_y = sum_y / len(avg_points)
                print("Average is: " + str(average_x) + ", " + str(average_y))
                # now: find variance

                variance_sum_x = 0
                variance_sum_y = 0
                for point in avg_points:
                    variance_sum_x += math.pow(point[0] - average_x, 2)
                    variance_sum_y += math.pow(point[1] - average_y, 2)

                variance_x = variance_sum_x / len(avg_points)
                variance_y = variance_sum_y / len(avg_points)

                print("Variance is: " + str(variance_x) + ", " + str(variance_y))
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            if (variance_x < 15 and variance_y < 15):
                print("Variance is smaller than 2, accepting result.")
                return(average_x, average_y), frame

        # cv2.imshow('Contours', skin_new)

        # if the 'q' key is pressed, stop the loop
        # if cv2.waitKey(5000) & 0xFF == ord("q"):
        #    break

    # cleanup the camera and close any open windows
    camera.release()


'''
            if (len(avg_points) == 5):
                for pt in avg_points:
                    total_x += pt[0]
                    total_y += pt[1]
                avg_x = total_x / len(avg_points)
                avg_y = total_y / len(avg_points)
                print("found point: " + str(avg_x) + ", " + str(avg_y))
                return (avg_x, avg_y)
'''
