import numpy as np
from .base_detector import BaseDetector
from scipy.optimize import linear_sum_assignment


class Tracker():
    """Tracker class to determine assignment from previous and current coordinates.

    """

    def __init__(self, params=None, detector=None):
        if params:
            self.params = params.copy()
        self.detector = detector
        self.is_init = False

    def set_params(self, params):
        self.params = params.copy()
        self.is_init = False

    def set_detector(self, detector):
        self.detector = detector
        self.is_init = False

    def initialize(self, image):
        if self.params and self.detector:
            self.prev_detection = self.detector.process(image)
            self.is_init = True
            self.max_id = len(self.prev_detection)
            self.id = list(range(self.max_id))
            self.lost = [0]*len(self.prev_detection)
            self.im = 0
            for i, j in enumerate(self.prev_detection):
                j["3"]["time"] = self.im
                j["3"]["id"] = self.id[i]
            self.im += 1
            return self.prev_detection

    def process(self, image):
        if self.is_init:
            self.current_detection = self.detector.process(image)
            order = self.assign(self.prev_detection, self.current_detection)
            losts = self.find_lost(order)
            self.current_detection = self.reassign(self.prev_detection,
                                                   self.current_detection, order)
            while len(self.current_detection) - len(self.id) != 0:
                self.max_id += 1
                self.id.append(self.max_id)
                self.lost.append(0)
            self.current, self.lost, self.id = self.clean(
                self.current_detection, self.lost, losts, self.id)
            for i, j in enumerate(self.current_detection):
                j["3"]["time"] = self.im
                j["3"]["id"] = self.id[i]
            self.im += 1
            self.prev_detection = self.current_detection
            return [j for i, j in enumerate(self.current_detection) if i not in losts]

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
        a = BaseDetector.modulo(a)
        b = BaseDetector.modulo(b)
        return -(BaseDetector.modulo(a - b + np.pi) - np.pi)

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
                prev_coord = l[str(int(self.params["spot"]))]
                for j, k in enumerate(current):
                    current_coord = k[str(int(self.params["spot"]))]

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

            # TODO: optimize
            assignment = []
            for i, __ in enumerate(prev):
                if i in row and (i, col[list(row).index(i)]) in valid:
                    assignment.append(col[list(row).index(i)])
                else:
                    assignment.append(-1)

        return assignment

    def reassign(self, past, current, order):
        """Reassign current based on order.

        Parameters
        ----------
        prev : list
            List of dict of previous detections.
        current : list
            List of dict of current detections.
        order : list
            Reassingment

        Returns
        -------
        list
            Reordered current.

        """
        tmp = past
        for i, j in enumerate(past):
            if order[i] != -1:
                tmp[i] = current[order[i]]

        for i, j in enumerate(current):
            if i not in order:
                tmp.append(j)

        return tmp

    def find_lost(self, assignment):
        """Find object lost at previous step.

        Parameters
        ----------
        assignment : list
            Assignment indexes.

        Returns
        -------
        list
            Indexes of lost objects.

        """
        return [i for i, j in enumerate(assignment) if j == -1]

    def clean(self, current, counter, lost, idty):
        """Delete objects that were lost.
        Only counter is copied in this function. Other lists act as pointer.

        Parameters
        ----------
        current : list
            List to clean.
        counter : list
            Counter of losses.
        lost : list
            Lost objects.
        idty : list
            Objects' identity

        Returns
        -------
        list
            Cleaned list.
        list
            Updated counter.

        """
        counter = [j + 1 if i in lost else 0 for i, j in enumerate(counter)]

        to_delete = sorted([i for i in lost if counter[i] >
                           self.params["maxTime"]], reverse=True)
        for i in to_delete:
            current.pop(i)
            counter.pop(i)
            idty.pop(i)
        return current, counter, idty
