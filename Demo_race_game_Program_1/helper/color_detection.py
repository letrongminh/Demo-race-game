import cv2
import numpy as np


class BackProjectionColorDetector:

    def __init__(self):
        self.template_hsv = None

    def setTemplate(self, frame):
        """Set the BGR image used as template during the pixel selection

        The template can be a specific region of interest of the main frame or a representative color scheme to identify
        the template is internally stored as an HSV image."""

        self.template_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    def getTemplate(self):
        """Get the BGR image used as template during the pixel selection
        The template can be a specific region of interest of the main frame or a representative color scheme to identify
        """
        if self.template_hsv is None:
            return None
        else:
            return cv2.cvtColor(self.template_hsv, cv2.COLOR_HSV2BGR)

    def returnFiltered(self, frame, morph_opening=True, blur=True, kernel_size=5, iterations=1):
        """Given an input frame in BGR return the filtered version.

        @param frame the original frame (color)
        @param morph_opening it is a erosion followed by dilatation to remove noise
        @param blur to smooth the image it is possible to apply Gaussian Blur
        @param kernel_size is the kernel dimension used for morph and blur
        """
        if self.template_hsv is None:
            return None

        # Get the mask from the internal function
        frame_threshold = self.returnMask(frame, morph_opening=morph_opening, blur=blur, kernel_size=kernel_size,
                                          iterations=iterations)
        # Return the AND image
        return cv2.bitwise_and(frame, frame_threshold)

    def returnMask(self, frame, morph_opening=True, blur=True, kernel_size=5, iterations=1):
        """Given an input frame in BGR return the black/white mask.

        @param frame the original frame (color)
        @param morph_opening it is a erosion followed by dilatation to remove noise
        @param blur to smooth the image it is possible to apply Gaussian Blur
        @param kernel_size is the kernel dimension used for morph and blur
        """
        if self.template_hsv is None:
            return None

        # Convert the input frame from BGR -> HSV
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Set the template histogram
        template_hist = cv2.calcHist([self.template_hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

        # Normalize the template histogram and apply backpropagation
        cv2.normalize(template_hist, template_hist, 0, 255, cv2.NORM_MINMAX)
        frame_hsv = cv2.calcBackProject([frame_hsv], [0, 1], template_hist, [0, 180, 0, 256], 1)

        # Get the kernel and apply a convolution
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        frame_hsv = cv2.filter2D(frame_hsv, -1, kernel)

        # Applying the morph open operation (erosion followed by dilation)
        if morph_opening is True:
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            frame_hsv = cv2.morphologyEx(frame_hsv, cv2.MORPH_OPEN, kernel, iterations=iterations)

        # Applying Gaussian Blur
        if blur is True:
            frame_hsv = cv2.GaussianBlur(frame_hsv, (kernel_size, kernel_size), 0)

        # Get the threshold
        ret, frame_threshold = cv2.threshold(frame_hsv, 50, 255, 0)

        # Merge the threshold matrices
        return cv2.merge((frame_threshold, frame_threshold, frame_threshold))


class MultiBackProjectionColorDetector:
    """Implementation of the Histogram Back-projection algorithm with multi-template.

    This class is the reimplementation of the BackProjectionColorDetector class for
    multi-template color detection. Instead of specifying a single template it is
    possible to pass a list of templates, which can be multiple sub-frame taken from
    different part of an object. Multiple version of the Backprojection algorithm
    are then run at the same time and the filtered output added together. The result
    of this process is much robust (but slower) than the standard class.
    """

    def __init__(self):
        self.template_hsv_list = list()

    def setTemplateList(self, frame_list):
        """Set the BGR image list used as container for the templates

        The template can be a specific region of interest of the main
        frame or a representative color scheme to identify. the template
        is internally stored as an HSV image.
        @param frame_list the template to use in the algorithm
        """
        for frame in frame_list:
            self.template_hsv_list.append(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV))

    def getTemplateList(self):
        """Get the BGR image list used as container for the templates

        Template can be a specific region of interest of the main frame or a representative color scheme to identify
        """
        output_list = list()
        for frame in self.template_hsv_list:
            output_list.append(cv2.cvtColor(frame, cv2.COLOR_HSV2BGR))
        return output_list

    def returnFiltered(self, frame, morph_opening=True, blur=True, kernel_size=5, iterations=1):
        """Given an input frame in BGR return the filtered version.

        @param frame the original frame (color)
        @param morph_opening it is a erosion followed by dilatation to remove noise
        @param blur to smooth the image it is possible to apply Gaussian Blur
        @param kernel_size is the kernel dimension used for morph and blur
        """
        if len(self.template_hsv_list) == 0:
            return None
        # Get the mask from the internal function
        frame_threshold = self.returnMask(frame, morph_opening=morph_opening, blur=blur, kernel_size=kernel_size,
                                          iterations=iterations)
        # Return the AND image
        return cv2.bitwise_and(frame, frame_threshold)

    def returnMask(self, frame, morph_opening=True, blur=True, kernel_size=5, iterations=1):
        """Given an input frame in BGR return the black/white mask.

        @param frame the original frame (color)
        @param morph_opening it is a erosion followed by dilatation to remove noise
        @param blur to smooth the image it is possible to apply Gaussian Blur
        @param kernel_size is the kernel dimension used for morph and blur
        """
        if len(self.template_hsv_list) == 0:
            return None
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = np.zeros((frame.shape[0], frame.shape[1]))
        for template_hsv in self.template_hsv_list:
            # Set the template histogram
            template_hist = cv2.calcHist([template_hsv], [0, 1], None, [256, 256], [0, 256, 0, 256])
            # Normalize the template histogram and apply backprojection
            cv2.normalize(template_hist, template_hist, 0, 255, cv2.NORM_MINMAX)
            frame_hsv_back = cv2.calcBackProject([frame_hsv], [0, 1], template_hist, [0, 256, 0, 256], 1)
            # Get the kernel and apply a convolution
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
            frame_hsv_clean = cv2.filter2D(frame_hsv_back, -1, kernel)
            # Applying the morph open operation (erosion followed by dilation)
            if morph_opening is True:
                kernel = np.ones((kernel_size, kernel_size), np.uint8)
                frame_hsv_clean = cv2.morphologyEx(frame_hsv_clean, cv2.MORPH_OPEN, kernel, iterations=iterations)
            # Applying Gaussian Blur
            if blur is True:
                frame_hsv_clean = cv2.GaussianBlur(frame_hsv_clean, (kernel_size, kernel_size), 0)
            # Get the threshold
            ret, frame_hsv_threshold = cv2.threshold(frame_hsv_clean, 50, 255, 0)
            mask = np.add(mask, frame_hsv_threshold)  # Add the threshold to the mask

        # Normalize the mask because it contains
        # values added during the previous loop
        # Attention: here it is not necessary to normalize because the astype(np.uint8) method
        # will resize to 255 each value which is higher that that...
        ret, mask = cv2.threshold(mask.astype(np.uint8), 50, 255, 0)
        return cv2.merge((mask, mask, mask))


class RangeColorDetector:
    """Using this detector it is possible to isolate colors in a specified range.

    In this detector the frame given as input is filtered and the pixel which
    fall in a specific range are taken, the other rejected. Some erosion and
    dilatation operation are used in order to remove noise.
    This class use the HSV (Hue, Saturation, Value) color representation to filter pixels.
    The H and S components characterize the color (independent of illumination)
    and V component specifies the illuminations.
    """

    def __init__(self, min_range, max_range):
        """Init the color detector object.

        The object must be initialised with an HSV range to use as filter.
        Ex: skin color in channel H is characterized by values between [0, 20],
        in the channel S=[48, 255] and V=[80, 255] (Asian and Caucasian). To
        initialise the vectors in this range it is possible to write:
        min_range = numpy.array([0, 48, 80], dtype = "uint8")
        max_range = numpy.array([20, 255, 255], dtype = "uint8")
        @param min_range the minimum HSV value to use as filer (numpy.array)
        @param max_range the maximum HSV value to use as filter (numpy.array)
        """
        # min and max range to use as filter for the detector (HSV)
        self.min_range = min_range
        self.max_range = max_range

    def setRange(self, min_range, max_range):
        """Set the min and max range used in the range detector

        The skin in channel H is characterized by values between 0 and 50,
        in the channel S from 0.23 to 0.68 (Asian and Caucasian).
        @parameter min_range the minimum HSV value to use as filer
        @parameter max_range the maximum HSV value to use as filter
        """
        # min and max range to use as filter for the detector (HSV)
        self.min_range = min_range
        self.max_range = max_range

    def getRange(self):
        """Return the min and max range used in the skin detector"""
        return self.min_range, self.max_range

    def returnFiltered(self, frame, morph_opening=True, blur=True, kernel_size=5, iterations=1):
        """Given an input frame return the filtered and deionised version.

        @param frame the original frame (color)
        @param morph_opening it is a erosion followed by dilatation to remove noise
        @param blur to smooth the image it is possible to apply Gaussian Blur
        @param kernel_size is the kernel dimension used for morph and blur
        @param iterations the number of time erode and dilate are called
        """
        frame_filtered = self.returnMask(frame, morph_opening=morph_opening, blur=blur, kernel_size=kernel_size,
                                         iterations=iterations)
        # bitwiseAND mask
        frame_deinoised = cv2.bitwise_and(frame, frame, mask=frame_filtered)
        return frame_deinoised

    def returnMask(self, frame, morph_opening=True, blur=True, kernel_size=5, iterations=1):
        """Given an input frame return the black/white mask.

        the function does not use the blur and bitwise operations, then the resulting frame contains white pixels
        in correspondence of the skin found during the searching process.
        @parameter frame is the original frame (color)
        """
        # Convert to HSV and eliminate pixels outside the range
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_filtered = cv2.inRange(frame_hsv, self.min_range, self.max_range)
        if morph_opening is True:
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            frame_filtered = cv2.morphologyEx(frame_filtered, cv2.MORPH_OPEN, kernel, iterations=iterations)
        # Applying Gaussian Blur
        if blur is True:
            frame_filtered = cv2.GaussianBlur(frame_filtered, (kernel_size, kernel_size), 0)
        return frame_filtered
