import math


class Line:
    """
    Represents a line with all necessary properties to use it for line calculations.
    """

    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        """
        Initializes a new line instance.
        :param x1: First corner X component.
        :param y1: First corner Y component.
        :param x2: Second corner X component.
        :param y2: Second corner Y component.
        """
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        try:
            self.slope = (y2 - y1) / (x2 - x1)
        except ZeroDivisionError:
            # Lines parallel to the y axis have a slope of infinity
            self.slope = float("inf")
        self.center = (y2 - y1, x2 - x1)

    def scale_centered(self, factor: float, test: bool = False) -> float:
        """
        Scales the line based on its center point (in-place).
        :param test: Whether to apply the change.
        :param factor: The scaling factor.
        :return: Resulting length of the line.
        """
        t0 = 0.5 * (1 - factor)
        t1 = 0.5 * (1 + factor)
        x1 = self.x1 + (self.x2 - self.x1) * t0
        y1 = self.y1 + (self.y2 - self.y1) * t0
        x2 = self.x1 + (self.x2 - self.x1) * t1
        y2 = self.y1 + (self.y2 - self.y1) * t1

        #print('x1: ' + str(self.x1) + ' -> ' + str(x1))
        #print('x2: ' + str(self.x2) + ' -> ' + str(x2))
        #print('y1: ' + str(self.y1) + ' -> ' + str(y1))
        #print('y2: ' + str(self.y1) + ' -> ' + str(y2))
        #print(' ')

        if not test:
            self.x1 = x1
            self.x2 = x2
            self.y1 = y1
            self.y2 = y2

        newlen = math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
        return newlen

    def get_length(self):
        """
        Returns the current length of the line.
        :return: float
        """
        return math.sqrt(pow(self.x2 - self.x1, 2) + pow(self.y2 - self.y1, 2))

    def scale_at_1(self, percentage_amount):
        """
        Scales the line at its first end by the given percentage.
        :param percentage_amount: The percentage by which the line is to be scaled.
        :return: None
        """
        factor = 1 - percentage_amount
        t0 = 0.5 * (1 - factor)
        x1 = self.x1 + (self.x2 - self.x1) * t0
        y1 = self.y1 + (self.y2 - self.y1) * t0
        self.x1 = x1
        self.y1 = y1

    def scale_at_2(self, percentage_amount):
        """
        Scales the line at its second end by the given percentage.
        :param percentage_amount: The percentage by which the line is to be scaled.
        :return: None
        """
        factor = 1 - percentage_amount
        t1 = 0.5 * (1 + factor)
        x2 = self.x1 + (self.x2 - self.x1) * t1
        y2 = self.y1 + (self.y2 - self.y1) * t1
        self.x2 = x2
        self.y2 = y2
