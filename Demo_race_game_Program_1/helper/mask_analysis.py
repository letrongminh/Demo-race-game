import cv2
import numpy as np


class BinaryMaskAnalyser:
    """This class analyses binary masks, like the ones returned by the color detection classes.

    The class implements function for finding the contour with the largest area and its properties
    (centre, surrounding rectangle).
    There are also functions for noise removal.
    """

    def returnNumberOfContours(self, mask):
        """it returns the total number of contours present on the mask this method must be used during video analysis
        to check if the frame contains at least one contour before calling the other function below. @parameter mask
        the binary image to use in the function @return get the number of contours
        """
        if mask is None:
            return None
        mask = np.copy(mask)  # doing a copy otherwise findContours modify the original
        if len(mask.shape) == 3:
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(mask, 1, 2)
        if hierarchy is None:
            return 0
        else:
            return len(hierarchy)

    def returnMaxAreaCenter(self, mask):
        """it returns the centre of the contour with largest area.
 
        This method could be useful to find the center of a face when a skin detector filter is used.
        @parameter mask the binary image to use in the function
        @return get the x and y center coords of the contour whit the largest area.
            In case of error it returns a tuple (None, None)"""
        if mask is None:
            return None, None
        mask = np.copy(mask)
        if len(mask.shape) == 3:
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(mask, 1, 2)
        area_array = np.zeros(len(contours))  # contains the area of the contours
        counter = 0
        for cnt in contours:
            area_array[counter] = cv2.contourArea(cnt)
            counter += 1
        if area_array.size == 0:
            return None, None  # the array is empty
        max_area_index = np.argmax(area_array)  # return the index of the max_area element

        cnt = contours[max_area_index]
        # calculate at the moments
        moments = cv2.moments(cnt)
        if moments['m00'] == 0:
            return None, None
        cx = int(moments['m10'] / moments['m00'])  # get the center from the moments
        cy = int(moments['m01'] / moments['m00'])
        return cx, cy  # return the center coords

    def returnMaxAreaContour(self, mask):
        """it returns the contour with largest area.
        This method could be useful to find a face when a skin detector filter is used.
        @parameter mask the binary image to use in the function
        @return get the x and y center coords of the contour whit the largest area 
        """
        if mask is None:
            return None
        mask = np.copy(mask)
        if len(mask.shape) == 3:
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(mask, 1, 2)
        area_array = np.zeros(len(contours))  # contains the area of the contours
        counter = 0
        for cnt in contours:
            area_array[counter] = cv2.contourArea(cnt)
            counter += 1
        if area_array.size == 0:
            return None  # the array is empty
        max_area_index = np.argmax(area_array)  # return the index of the max_area element
        cnt = contours[max_area_index]
        return cnt  # return the max are contour

    def drawMaxAreaContour(self, frame, mask, color=None, thickness=3):
        """it draws the contour with largest area.
 
        @parameter frame the image to use as canvas
        @parameter mask the binary image to use in the function
        @parameter color the color of the contour
        @parameter thickness of the contour
        """
        if color is None:
            color = [0, 255, 0]
        cnt = self.returnMaxAreaContour(mask)
        cv2.drawContours(frame, cnt, -1, color, thickness)

    def matchMaxAreaWithShape(self, mask, shape):
        """it returns a value which identify the similarity between the largest area contour and a shape.
 
        The lower the result, the better match it is. It is calculated based on the hu-moment values.
        For example if we have three shapes:
        A=star, B=rotated dilated star, C=square
        Matching Image A with itself = 0.0
        Matching Image A with Image B = 0.001946
        Matching Image A with Image C = 0.326911
        @parameter mask the binary image to use in the function
        @parameter shape the contour to compare
        """
        cnt = self.returnMaxAreaContour(mask)
        return cv2.matchShapes(cnt, shape, 1, 0.0)

    def returnMaxAreaConvexHull(self, mask):
        """it returns the convex hull surrounding the contour with the largest area.
 
        @parameter mask the binary image to use in the function
        @return get the coords of the convex hull
        """
        cnt = self.returnMaxAreaContour(mask)
        return cv2.convexHull(cnt)

    def drawMaxAreaConvexHull(self, frame, mask, color=None, thickness=3):
        """it draws the convex hull for the contour with largest area.
 
        @parameter frame the image to use as canvas
        @parameter mask the binary image to use in the function
        @parameter color the color of the convex hull
        @parameter thickness of the convex hull
        """
        if color is None:
            color = [0, 255, 0]
        cnt = self.returnMaxAreaContour(mask)
        hull = cv2.convexHull(cnt)
        cv2.drawContours(frame, hull, -1, color, thickness)

    def returnMaxAreaRectangle(self, mask):
        """it returns the rectangle surrounding the contour with the largest area.
 
        This method could be useful to find a face when a skin detector filter is used.
        @parameter mask the binary image to use in the function
        @return get the coords of the upper corner of the rectangle (x, y) and the rectangle size (width, height)
            In case of error it returns a tuple (None, None, None, None) 
        """
        if mask is None:
            return None, None, None, None
        mask = np.copy(mask)
        if len(mask.shape) == 3:
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(mask, 1, 2)
        area_array = np.zeros(len(contours))  # contains the area of the contours
        counter = 0
        for cnt in contours:
            area_array[counter] = cv2.contourArea(cnt)
            counter += 1
        if area_array.size == 0:
            return None, None, None, None  # the array is empty
        max_area_index = np.argmax(area_array)  # return the index of the max_area element
        cnt = contours[max_area_index]
        (x, y, w, h) = cv2.boundingRect(cnt)
        return x, y, w, h

    def drawMaxAreaRectangle(self, frame, mask, color=None, thickness=3):
        """it draws the rectangle with largest area.
 
        @parameter frame the image to use as canvas
        @parameter mask the binary image to use in the function
        @parameter color the color of the rectangle
        @parameter thickness of the rectangle
        """
        if color is None:
            color = [0, 255, 0]
        x, y, w, h = self.returnMaxAreaRectangle(mask)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

    def returnMaxAreaCircle(self, mask):
        """it returns the circle surrounding the contour with the largest area.
 
        @parameter mask the binary image to use in the function
        @return get the center (x, y) and the radius of the circle
        """
        if mask is None:
            return None, None, None
        mask = np.copy(mask)
        if len(mask.shape) == 3:
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(mask, 1, 2)
        area_array = np.zeros(len(contours))  # contains the area of the contours
        counter = 0
        for cnt in contours:
            area_array[counter] = cv2.contourArea(cnt)
            counter += 1
        if area_array.size == 0:
            return None, None, None  # the array is empty
        max_area_index = np.argmax(area_array)  # return the index of the max_area element
        cnt = contours[max_area_index]
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        return int(x), int(y), int(radius)

    def drawMaxAreaCircle(self, frame, mask, color=None, thickness=3):
        """it draws the circle with largest area.
 
        @parameter frame the image to use as canvas
        @parameter mask the binary image to use in the function
        @parameter color the color of the circle
        @parameter thickness of the circle
        """
        if color is None:
            color = [0, 255, 0]
        x, y, r = self.returnMaxAreaCircle(mask)
        cv2.circle(frame, (x, y), r, color, thickness)
