"""
Evaluation Metrics Module
Calculates Confusion Matrix, Accuracy, Precision, Recall, F1 Score, Detection Rate,
False Alarm Rate, Missed Detection Rate, Per-Class Accuracy, and Calibration Metrics.
"""

from typing import Dict, List, Any, Tuple
import numpy as np


class PerformanceMetrics:
    """Computes comprehensive classification metrics and confidence calibration statistics."""

    @staticmethod
    def calculate_classification_metrics(
        y_true: List[int],
        y_pred: List[int],
        class_true: List[str],
        class_pred: List[str],
        confidences: List[float]
    ) -> Dict[str, Any]:
        """
        Calculates full suite of classification and detection performance metrics.
        """
        y_t = np.array(y_true)
        y_p = np.array(y_pred)

        total_samples = len(y_t)
        if total_samples == 0:
            return {}

        # 1. Binary Detection Metrics (Target Detected vs No Target / Clutter)
        tp = int(np.sum((y_t == 1) & (y_p == 1)))
        fp = int(np.sum((y_t == 0) & (y_p == 1)))
        tn = int(np.sum((y_t == 0) & (y_p == 0)))
        fn = int(np.sum((y_t == 1) & (y_p == 0)))

        accuracy = (tp + tn) / total_samples
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        detection_rate = recall
        false_alarm_rate = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        missed_detection_rate = fn / (fn + tp) if (fn + tp) > 0 else 0.0

        # 2. Per-Class Accuracy Breakdown
        all_classes = sorted(list(set(class_true + class_pred)))
        per_class_metrics: Dict[str, Dict[str, float]] = {}

        for c in all_classes:
            c_true = np.array([1 if ct == c else 0 for ct in class_true])
            c_pred = np.array([1 if cp == c else 0 for cp in class_pred])
            
            c_tp = int(np.sum((c_true == 1) & (c_pred == 1)))
            c_total = int(np.sum(c_true == 1))
            c_acc = c_tp / c_total if c_total > 0 else 1.0

            per_class_metrics[c] = {
                "correct": c_tp,
                "total": c_total,
                "accuracy": round(c_acc, 3)
            }

        # 3. Confidence Calibration & Expected Calibration Error (ECE)
        conf_arr = np.array(confidences)
        correct_arr = np.array([1 if class_true[i] == class_pred[i] else 0 for i in range(total_samples)])
        
        overconfident_count = int(np.sum((conf_arr > 0.85) & (correct_arr == 0)))
        underconfident_count = int(np.sum((conf_arr < 0.50) & (correct_arr == 1)))

        # ECE calculation across 5 confidence bins
        bins = np.linspace(0.0, 1.0, 6)
        ece = 0.0
        for i in range(len(bins) - 1):
            bin_lower, bin_upper = bins[i], bins[i+1]
            in_bin = (conf_arr >= bin_lower) & (conf_arr < bin_upper)
            bin_size = np.sum(in_bin)
            if bin_size > 0:
                bin_acc = np.mean(correct_arr[in_bin])
                bin_conf = np.mean(conf_arr[in_bin])
                ece += (bin_size / total_samples) * abs(bin_acc - bin_conf)

        return {
            "total_samples": total_samples,
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1_score, 4),
            "detection_rate": round(detection_rate, 4),
            "false_alarm_rate": round(false_alarm_rate, 4),
            "missed_detection_rate": round(missed_detection_rate, 4),
            "confusion_matrix": {"TP": tp, "FP": fp, "TN": tn, "FN": fn},
            "per_class_metrics": per_class_metrics,
            "calibration": {
                "expected_calibration_error": round(ece, 4),
                "overconfident_predictions": overconfident_count,
                "underconfident_predictions": underconfident_count
            }
        }
