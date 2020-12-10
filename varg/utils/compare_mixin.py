""" Mixin class for comparisons """

import logging

LOG = logging.getLogger(__name__)

STRING_SAME = "same"
STRING_DIFF = "diff"
NUM_SAME = "same"
NUM_LOWER = "lower"
NUM_HIGHER = "higher"
LIST_SAME = "same"
LIST_UNKNOWN = "unknown"
LIST_DIFF = "diff"


class CompareMixin:
    """Mixin class for compaisons"""

    def _evaluate_comparison(self, value_1, value_2, value_ids=[]):

        evaluation = dict()

        if isinstance(value_1, str):
            if value_1 == value_2:
                evaluation["status"] = STRING_SAME
            else:
                evaluation["status"] = STRING_DIFF

        # For float or int, add the abs diff between values
        elif isinstance(value_1, (float, int)):
            if value_1 == value_2:
                evaluation["status"] = NUM_SAME
            elif value_2 > value_1:
                evaluation["status"] = NUM_HIGHER
            else:
                evaluation["status"] = NUM_LOWER
            evaluation["diff"] = value_2 - value_1

        elif isinstance(value_1, (tuple, list)):
            if len(value_1) != len(value_2):
                LOG.error(
                    "Unable to compare arrays of length %d and %d, must be same",
                    len(value_1),
                    len(value_2),
                )
                raise IndexError
            similarity = LIST_SAME

            if "GT" in value_ids:
                evaluation["status"] = self.compare_GT(value_1, value_2)
            else:
                for element_1, element_2 in zip(value_1, value_2):
                    if all((isinstance(element_1, str), isinstance(element_2, str))):
                        if "." in element_1 or "." in element_2:
                            similarity = LIST_UNKNOWN
                        elif element_1 != element_2:
                            similarity = LIST_DIFF
                            break
                    elif element_1 != element_2:
                        similarity = LIST_DIFF
                evaluation["status"] = similarity
        return evaluation

    @staticmethod
    def compare_GT(gt_1: list, gt_2: list):

        for index in range(len(gt_1)):
            if "|" in gt_1[index]:
                gt_1[index] = gt_1[index].replace("|", "/")
            if "|" in gt_2[index]:
                gt_2[index] = gt_2[index].replace("|", "/")

            similarity = LIST_SAME
            for element_1, element_2 in zip(gt_1, gt_2):
                if all((isinstance(element_1, str), isinstance(element_2, str))):
                    if "." in element_1 or "." in element_2:
                        if element_1 != element_2:
                            similarity = LIST_UNKNOWN
                    elif element_1 != element_2:
                        similarity = LIST_DIFF
                        break
                elif element_1 != element_2:
                    similarity = LIST_DIFF

            return similarity
