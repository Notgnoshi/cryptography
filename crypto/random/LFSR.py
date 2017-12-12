from collections import deque
import numpy


class LinearFeedbackShiftRegister(object):
    """
        Implements a Linear Feedback Shift Register. Given some initial values and recurrence
        relation coefficients, generates the sequence given by some specified recurrence relation.
    """

    def __init__(self, initial_values, coeffs, base=2):
        """
            Generates a LinearFeedbackShiftRegister object from a set of coefficients and initial
            values.

            Example:
            >>> IV = numpy.array([0, 0, 1, 1, 0])
            >>> coeffs = numpy.array([1, 1, 0, 0, 1])
            >>> lfsr = LinearFeedbackShiftRegister(IV, coeffs)
            >>> next(lfsr)
            0
        """
        self.initial_values = deque(initial_values)
        self.current_values = initial_values
        self.coeffs = coeffs
        self.base = base

    def __iter__(self):
        return self

    def __next__(self):
        """
            Returns the next item in the sequence. Starts yielding values beginning
            with the first given initial value.
        """

        # Consume the initial values before moving on to generating new ones.
        if self.initial_values:
            return self.initial_values.popleft()

        # Generate new values based on the old ones.
        next_element = numpy.mod(numpy.dot(self.coeffs, self.current_values), self.base)
        self.current_values = numpy.append(self.current_values[1:], next_element)

        return next_element
