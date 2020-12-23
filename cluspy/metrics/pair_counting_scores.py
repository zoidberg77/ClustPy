"""
Achtert, Elke, et al. "Evaluation of clusterings--metrics and visual
support." 2012 IEEE 28th International Conference on Data
Engineering. IEEE, 2012.
"""
from .variation_of_information import _check_number_of_points

def _jaccard_score(n_tp, n_fp, n_fn):
    return 0 if (n_tp + n_fp + n_fn) == 0 else n_tp / (n_tp + n_fp + n_fn)


def _rand_score(n_tp, n_fp, n_fn, n_tn):
    return 0 if (n_tp + n_fp + n_fn + n_tn) == 0 else (n_tp + n_tn) / (n_tp + n_fp + n_fn + n_tn)


def _precision_score(n_tp, n_fp):
    return 0 if (n_tp + n_fp) == 0 else n_tp / (n_tp + n_fp)


def _recall_score(n_tp, n_fn):
    return 0 if (n_tp + n_fn) == 0 else n_tp / (n_tp + n_fn)


def _f1_score(n_tp, n_fp, n_fn):
    precision = _precision_score(n_tp, n_fp)
    recall = _recall_score(n_tp, n_fn)
    return 0 if (precision == 0 and recall == 0) else 2 * precision * recall / (precision + recall)


def _pair_counting_categories(ground_truth, prediction):
    if ground_truth.ndim != 1 or prediction.ndim != 1:
        raise Exception("Ground truth and prediction labels should just contain a single column.")
    n_tp = 0
    n_fp = 0
    n_fn = 0
    n_tn = 0
    for i in range(prediction.shape[0] - 1):
        for j in range(i + 1, prediction.shape[0]):
            if prediction[i] == prediction[j]:
                if ground_truth[i] == ground_truth[j]:
                    n_tp += 1
                else:
                    n_fp += 1
            else:
                if ground_truth[i] == ground_truth[j]:
                    n_fn += 1
                else:
                    n_tn += 1
    return n_tp, n_fp, n_fn, n_tn


def _pair_counting_categories_multiple_labelings(ground_truth, prediction):
    n_tp = 0
    n_fp = 0
    n_fn = 0
    n_tn = 0
    for i in range(prediction.shape[0] - 1):
        for j in range(i + 1, prediction.shape[0]):
            if _anywhere_same_cluster(prediction, i, j):
                if _anywhere_same_cluster(ground_truth, i, j):
                    n_tp += 1
                else:
                    n_fp += 1
            else:
                if _anywhere_same_cluster(ground_truth, i, j):
                    n_fn += 1
                else:
                    n_tn += 1
    return n_tp, n_fp, n_fn, n_tn

def _anywhere_same_cluster(labels, i, j):
    for s in range(labels.shape[1]):
        if labels[i, s] == labels[j, s]:
            return True
    return False

class PairCountingScore():
    def __init__(self, ground_truth, prediction, multiple_labelings=None):
        _check_number_of_points(ground_truth, prediction)
        if multiple_labelings is None:
            # Check if ground truth contains multiple labelings
            multiple_labelings = (ground_truth.ndim != 1)
        if multiple_labelings:
            n_tp, n_fp, n_fn, n_tn = _pair_counting_categories_multiple_labelings(ground_truth, prediction)
        else:
            n_tp, n_fp, n_fn, n_tn = _pair_counting_categories(ground_truth, prediction)
        self.n_tp = n_tp
        self.n_fp = n_fp
        self.n_fn = n_fn
        self.n_tn = n_tn

    def jaccard(self):
        return _jaccard_score(self.n_tp, self.n_fp, self.n_fn)

    def rand(self):
        return _rand_score(self.n_fp, self.n_fn, self.n_tn)

    def precision(self):
        return _precision_score(self.n_tp, self.n_fp)

    def recall(self):
        return _recall_score(self.n_tp, self.n_fn)

    def f1(self):
        return _f1_score(self.n_tp, self.n_fp, self.n_fn)