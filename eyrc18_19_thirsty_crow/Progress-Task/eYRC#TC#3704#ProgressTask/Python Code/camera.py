"SOME FUNCTIONS OF THIS FILE ARE USED IN PATH.PY SO KEEP IN SAME DIRECTORY"

import numpy as np
import cv2
import cv2.aruco as aruco
import math

"""
**************************************************************************
*                  E-Yantra Robotics Competition
*                  ================================
*  This software is intended to check version compatiability of open source software
*  Theme: Thirsty Crow
*  MODULE: Task1.1
*  Filename: detect.py
*  Version: 1.0.0
*  Date: October 31, 2018
*
*  Author: e-Yantra Project, Department of Computer Science
*  and Engineering, Indian Institute of Technology Bombay.
*
*  Software released under Creative Commons CC BY-NC-SA
*
*  For legal information refer to:
*        http://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
*
*
*  This software is made available on an “AS IS WHERE IS BASIS”.
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*  e-Yantra - An MHRD project under National Mission on Education using
*  ICT(NMEICT)
*
**************************************************************************
"""

####################### Define Utility Functions Here ##########################
"""
Function Name : getCameraMatrix()
Input: None
Output: camera_matrix, dist_coeff
Purpose: Loads the camera calibration file provided and returns the camera and
         distortion matrix saved in the calibration file.
"""


def getCameraMatrix():
    with np.load('Camera.npz') as X:
        camera_matrix, dist_coeff, _, _ = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]
    return camera_matrix, dist_coeff


"""
Function Name : sin()
Input: angle (in degrees)
Output: value of sine of angle specified
Purpose: Returns the sine of angle specified in degrees
"""


def sin(angle):
    value = math.sin(math.radians(angle))
    if value < 0.000001 and value > - 0.0000001:
        value =0.0
    return value


"""
Function Name : cos()
Input: angle (in degrees)
Output: value of cosine of angle specified
Purpose: Returns the cosine of angle specified in degrees
"""


def cos(angle):
    value =math.cos(math.radians(angle))
    if value < 0.000001 and value > - 0.0000001:
        value = 0.0
    return value




################################################################################


"""
Function Name : detect_markers()
Input: img (numpy array), camera_matrix, dist_coeff
Output: aruco list in the form [(aruco_id_1, centre_1, rvec_1, tvec_1),(aruco_id_2,
        centre_2, rvec_2, tvec_2), ()....]
Purpose: This function takes the image in form of a numpy array, camera_matrix and
         distortion matrix as input and detects ArUco markers in the image. For each
         ArUco marker detected in image, paramters such as ID, centre coord, rvec
         and tvec are calculated and stored in a list in a prescribed format. The list
         is returned as output for the function
"""


def detect_markers(img, camera_matrix, dist_coeff):
    markerLength = 100
    aruco_list = []
    #######################         INSERT CODE HERE        ########################

    gray = img
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    gray_detected = aruco.drawDetectedMarkers(gray, corners, ids, borderColor=(225, 0, 255))

    ##----------------------------------------------------------------------------------------------
    ##               ....finding aruco _ centers ....
    ##----------------------------------------------------------------------------------------------

    aruco_centers = np.zeros([len(ids), 2], float)

    for i in range(0, len(ids)):
        center_x = (float(corners[i][0][0][0]) + float(corners[i][0][2][0])) / 2
        center_y = (float(corners[i][0][0][1]) + float(corners[i][0][2][1])) / 2
        # print ("center_coordnates are = ", center_x,center_y)
        aruco_centers[i][0] = center_x
        aruco_centers[i][1] = center_y

    ##---------------------------------------------------------------------------------------------
    ##                 .....we got the aruco_centers .....
    ##---------------------------------------------------------------------------------------------

    with np.load('Camera.npz') as X:

        camera_matrix = X['mtx']
        dist_coeff = X['dist']
        CAMrot_vec = X['rvecs']
        CAMtrans_vec = X['tvecs']

    for n in range(0, len(ids)):
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners[n], markerLength, camera_matrix, dist_coeff)
        aruco_list.append(tuple((ids[n][0], tuple(aruco_centers[n]), rvec, tvec)))

    ##############################################################################
    return aruco_list


"""
Function Name : drawAxis()
Input: img (numpy array), aruco_list, aruco_id, camera_matrix, dist_coeff
Output: img (numpy array)
Purpose: This function takes the above specified outputs and draws 3 mutually
         perpendicular axes on the specified aruco marker in the image and
         returns the modified image.
"""


def drawAxis(img, aruco_list, aruco_id, camera_matrix, dist_coeff):
    for x in aruco_list:
        if aruco_id == x[0]:
            rvec, tvec = x[2], x[3]
    markerLength = 100
    m = markerLength / 2
    pts = np.float32([[-m, m, 0], [m, m, 0], [-m, -m, 0], [-m, m, m]])
    pt_dict = {}
    imgpts, _ = cv2.projectPoints(pts, rvec, tvec, camera_matrix, dist_coeff)
    for i in range(len(pts)):
        pt_dict[tuple(pts[i])] = tuple(imgpts[i].ravel())
    src = pt_dict[tuple(pts[0])];
    dst1 = pt_dict[tuple(pts[1])];
    dst2 = pt_dict[tuple(pts[2])];
    dst3 = pt_dict[tuple(pts[3])];

    img = cv2.line(img, src, dst1, (0, 255, 0), 4)
    img = cv2.line(img, src, dst2, (255, 0, 0), 4)
    img = cv2.line(img, src, dst3, (0, 0, 255), 4)
    return img


"""
Function Name : drawCube()
Input: img (numpy array), aruco_list, aruco_id, camera_matrix, dist_coeff
Output: img (numpy array)
Purpose: This function takes the above specified outputs and draws a cube
         on the specified aruco marker in the image and returns the modified
         image.
"""


def drawCube(img, ar_list, ar_id, camera_matrix, dist_coeff):
    for x in ar_list:
        if ar_id == x[0]:
            rvec, tvec = x[2], x[3]
    markerLength = 100
    m = markerLength / 2;
    ######################## INSERT CODE HERE ########################
    pts = np.float32([[-m, m, 0], [m, -m, m], [-m, -m, m], [m, m, m], [m, -m, 0], [-m, m, m], [-m, -m, 0], [m, m, 0]])
    pt_dict = {};
    imgpts, _ = cv2.projectPoints(pts, rvec, tvec, camera_matrix, dist_coeff)
    for i in range(len(pts)):
        pt_dict[tuple(pts[i])] = tuple(imgpts[i].ravel())
    # fix source point ....

    src1 = pt_dict[tuple(pts[0])]
    src2 = pt_dict[tuple(pts[1])]
    src3 = pt_dict[tuple(pts[2])]
    src4 = pt_dict[tuple(pts[3])]
    src5 = pt_dict[tuple(pts[4])]

    # setting up destination point ....
    dst1 = pt_dict[tuple(pts[5])]
    dst2 = pt_dict[tuple(pts[6])]
    dst3 = pt_dict[tuple(pts[7])]

    img = cv2.line(img, dst2, src3, (255, 0, 0), 4)
    img = cv2.line(img, src5, src2, (255, 0, 0), 4)
    img = cv2.line(img, src1, dst1, (255, 0, 0), 4)
    img = cv2.line(img, dst3, src4, (255, 0, 0), 4)

    img = cv2.line(img, src1, dst2, (0, 255, 0), 4)
    img = cv2.line(img, src1, dst3, (0, 255, 0), 4)
    img = cv2.line(img, src5, dst2, (0, 255, 0), 4)
    img = cv2.line(img, src5, dst3, (0, 255, 0), 4)

    img = cv2.line(img, dst1, src4, (0, 0, 255), 4)
    img = cv2.line(img, dst1, src3, (0, 0, 255), 4)
    img = cv2.line(img, src2, src4, (0, 0, 255), 4)
    img = cv2.line(img, src2, src3, (0, 0, 255), 4)

    ##################################################################
    return img


"""
Function Name : drawCylinder()
Input: img (numpy array), aruco_list, aruco_id, camera_matrix, dist_coeff
Output: img (numpy array)
Purpose: This function takes the above specified outputs and draws a cylinder
         on the specified aruco marker in the image and returns the modified
         image.
"""


def drawCylinder(img, ar_list, ar_id, camera_matrix, dist_coeff):
    for x in ar_list:
        if ar_id == x[0]:
            rvec, tvec = x[2], x[3]
    markerLength = 100
    m = int(markerLength / 2)
    radius = int(markerLength / 2);
    height = int(markerLength * 1.5)

    ######################## INSERT CODE HERE ########################

    # --------------------------------------------------------------------------------------------
    # finding required points ....
    # --------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------
    # above function GENERATES ALL POINTS ON CYLINDER [CENTER , CIRCUMFERENCE_Z(clockwise-manner)
    # --------------------------------------------------------------------------------------------

    def pl_points(z):
        points = np.zeros([13, 3], np.float32)
        # points of centre at given plane --
        points[0][0] = 0
        points[0][1] = 0
        points[0][2] = z
        # rest of the points on the circumference --
        for i in range(1, 13):
            points[i][0] = radius * sin(i * 30)
            points[i][1] = radius * cos(i * 30)
            points[i][2] = z
        return points

    # -----------------------------------------------------------------------------------------------------------
    #       SINCE PROJECTING A POINT IS'NT ENOUGH SO WE'RE DRAWING AN APPROX CIRCLE THAT'S PROJECTABLE ON ARUCO-PLANE
    # -----------------------------------------------------------------------------------------------------------

    def draw_ProCircle(img, z, h):
        # h -- is angle difference( ...in order to tune accuracy )
        pts = np.zeros([360, 3], np.float32)

        # rest of the points on the circumference --
        for i in range(0, 360):
            pts[i][0] = radius * sin(i * h)
            pts[i][1] = radius * cos(i * h)
            pts[i][2] = z

        pt_dict = {};
        imgpts, _ = cv2.projectPoints(pts, rvec, tvec, camera_matrix, dist_coeff)
        for i in range(len(pts)):
            pt_dict[tuple(pts[i])] = tuple(imgpts[i].ravel())

        for i in range(0, 360):
            img = cv2.line(img, pt_dict[tuple(pts[i])], pt_dict[tuple(pts[i])], (0, 0, 255), 2)

        return img

    # --------------------------------------------------------------------------------------------
    #       DRAWING STARTS HERE ....
    # --------------------------------------------------------------------------------------------
    def drawcircle(z, img):
        pts = pl_points(z)
        pt_dict = {};
        imgpts, _ = cv2.projectPoints(pts, rvec, tvec, camera_matrix, dist_coeff)
        for i in range(len(pts)):
            pt_dict[tuple(pts[i])] = tuple(imgpts[i].ravel())
        # --------------------------------------------------------------------------------------------
        # first we draw the circle with center at  (0,0,0) and (0,0,height)  --

        draw_ProCircle(img, 0, 1)
        draw_ProCircle(img, height, 1)
        # --------------------------------------------------------------------------------------------

        for i in range(1, 7):
            img = cv2.line(img, pt_dict[tuple(pts[i])], pt_dict[tuple(pts[i + 6])], (0, 0, 255), 2)

        return img

    def join_pts(img):

        pts_0 = pl_points(0)
        pts_z = pl_points(height)
        pt_dict_0 = {};
        pt_dict_z = {};
        imgpts_0, _ = cv2.projectPoints(pts_0, rvec, tvec, camera_matrix, dist_coeff)
        imgpts_z, _ = cv2.projectPoints(pts_z, rvec, tvec, camera_matrix, dist_coeff)
        for i in range(len(pts_0)):
            pt_dict_0[tuple(pts_0[i])] = tuple(imgpts_0[i].ravel())
            pt_dict_z[tuple(pts_z[i])] = tuple(imgpts_z[i].ravel())

        for i in range(0, 13):
            img = cv2.line(img, pt_dict_0[tuple(pts_0[i])], pt_dict_z[tuple(pts_z[i])], (0, 0, 255), 2)

        return img

    drawcircle(0, img)
    drawcircle(height, img)
    join_pts(img)
    # --------------------------------------------------------------------------------------------
    #       IT RETURNS A COMPLETE DIAGRAM FOR A GIVEN PLANE(Z)
    # --------------------------------------------------------------------------------------------

    ##################################################################
    return img


"""
MAIN CODE
This main code reads images from the test cases folder and converts them into
numpy array format using cv2.imread. Then it draws axis, cubes or cylinders on
the ArUco markers detected in the images.
"""

if __name__ == "__main__":
    cam, dist = getCameraMatrix()
    img = cv2.imread("..\\TestCases\\image_1.jpg")
    # img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    aruco_list = detect_markers(img, cam, dist)
    for i in aruco_list:
        img = drawAxis(img, aruco_list, i[0], cam, dist)
        img = drawCube(img, aruco_list, i[0], cam, dist)
        img = drawCylinder(img, aruco_list, i[0], cam, dist)
        cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
