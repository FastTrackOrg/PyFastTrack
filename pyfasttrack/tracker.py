import numpy as np
import base_detector
from scipy.optimize import linear_sum_assignment


class Tracker():
    """Tracker class to determine assignment from previous and current coordinates.

    """

    def __init__(self, params):
        self.params = params.copy()

    @staticmethod
    def angle_difference(a, b):
        """Get the minimal difference, a-b), between two angles.

        Parameters
        ----------
        a : float
            First angle.
        b : float
            Second angle.

        Returns
        -------
        float
            a-b.

        """
        a = base_detector.BaseDetector.modulo(a)
        b = base_detector.BaseDetector.modulo(b)
        return -(base_detector.BaseDetector.modulo(a - b + np.pi) - np.pi)

    @staticmethod
    def div(a, b):
        """Division by zero, a/0=0.

        Parameters
        ----------
        a : float
            Dividend.
        b : float
            Divisor.

        Returns
        -------
        float
            a/b.

        """
        if b != 0:
            return a/b
        else:
            return 0

    def compute_cost(self, var, norm):
        """Compute the cost.

        Parameters
        ----------
        var : List
            List of variable.
        norm : list
            Normalization coefficient associated to var.

        Returns
        -------
        float
            Cost.

        """
        cost = 0
        for i, j in zip(var, norm):
            cost += self.div(i, j)
        return cost

    def assign(self, prev, current):
        """Find the optimal assignent.

        Parameters
        ----------
        prev : list
            List of dict. Each dict is one object with 4 key "0", "1", "2", "3".
            0,1,2 is the {center, orientation} of the head, tail and body respectively.
            3 is {area, perim} of the object.
        current : list
            List of dict. Each dict is one object with 4 key "0", "1", "2", "3".
            0,1,2 is the {center, orientation} of the head, tail and body respectively.
            3 is {area, perim} of the object.

        Returns
        -------
        list
            Assignment.

        """
        if len(prev) == 0:
            assignment = []
        elif len(current) == 0:
            assignment = [-1]*len(prev)
        else:
            cost = np.zeros((len(prev), len(current)))
            valid = []
            for i, l in enumerate(prev):
                prev_coord = l[self.params["spot"]]
                for j, k in enumerate(current):
                    current_coord = k[self.params["spot"]]

                    distance = np.sqrt((prev_coord["center"][0] - current_coord["center"][0])**2 + (
                        prev_coord["center"][1] - current_coord["center"][1])**2)
                    angle = np.abs(self.angle_difference(
                        prev_coord["orientation"], current_coord["orientation"]))
                    area = np.abs(l["3"]["area"] - k["3"]["area"])
                    perim = np.abs(l["3"]["perim"] - k["3"]["perim"])

                    if distance < self.params["maxDist"]:
                        cost[i, j] = self.compute_cost([distance, angle, area, perim], [
                                                       self.params["normDist"], self.params["normAngle"], self.params["normArea"], self.params["normPerim"]])
                        valid.append((i, j))
                    else:
                        cost[i, j] = 1e34

            row, col = linear_sum_assignment(cost)

            assignment = []
            for i in zip(row, col):
                if i in valid:
                    assignment.append(i[1])
                else:
                    assignment.append(-1)

        return assignment
