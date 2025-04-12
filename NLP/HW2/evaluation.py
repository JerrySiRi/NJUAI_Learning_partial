#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Evaluation module for Chinese Text Correction task.
This module provides functions for evaluating the performance of correction models,
including precision, recall, F1, and F0.5 metrics for both detection and correction.
"""

import re
import json
import numpy as np
import Levenshtein
from typing import Dict, List, Tuple, Any
from collections import Counter, OrderedDict


def get_edits(src_text: str, tgt_text: str) -> List[Tuple]:
    """
    Calculate edit operations between source text and target text.

    Args:
        src_text: Source text
        tgt_text: Target text

    Returns:
        List of edit operations, each operation is a tuple (operation_type, start_pos, end_pos, [replacement_text])
    """
    # Use Levenshtein library to calculate edit operations
    edits = Levenshtein.opcodes(src_text, tgt_text)

    # Generate standardized edit sequence
    result = []
    for edit in edits:
        if edit[0] == 'equal':
            continue
        elif edit[0] == "insert":
            result.append(("M", edit[1], edit[1], tgt_text[edit[3] : edit[4]]))
        elif edit[0] == "replace":
            result.append(("S", edit[1], edit[2], tgt_text[edit[3] : edit[4]]))
        elif edit[0] == "delete":
            result.append(("R", edit[1], edit[2]))
        else:
            print(f"Unknown edit operation: {edit}")

    return result


def evaluate_performance(predictions: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Evaluate the performance of correction models.

    Args:
        predictions: List of dictionaries containing source, prediction, target, and label.

    Returns:
        Dictionary containing evaluation metrics.
    """
    gold_edits = []
    pred_edits = []

    for sample in predictions:
        src = sample['source']
        tgt = sample['target']
        pred = sample['prediction']

        gold_edits.append(get_edits(src, tgt))
        pred_edits.append(get_edits(src, pred))

    # Calculate detection and correction metrics
    detection_TP = 0  # Detected errors
    detection_FP = 0  # False positives in error detection
    detection_FN = 0  # Undetected errors

    correction_TP = 0  # Correctly corrected errors
    correction_FP = 0  # False positives in error correction
    correction_FN = 0  # Uncorrected errors

    for i in range(len(gold_edits)):
        gold_edit_set = set([(e[0], e[1], e[2]) for e in gold_edits[i]])
        gold_edit_map = {(e[0], e[1], e[2]): e for e in gold_edits[i]}

        pred_edit_set = set([(e[0], e[1], e[2]) for e in pred_edits[i]])
        pred_edit_map = {(e[0], e[1], e[2]): e for e in pred_edits[i]}

        # Evaluate detection performance
        detection_TP += len(gold_edit_set & pred_edit_set)
        detection_FP += len(pred_edit_set - gold_edit_set)
        detection_FN += len(gold_edit_set - pred_edit_set)

        # Evaluate correction performance
        for edit_key in gold_edit_set & pred_edit_set:
            gold_edit = gold_edit_map[edit_key]
            pred_edit = pred_edit_map[edit_key]

            # For replacement and insertion operations, check if replacement text is correct
            if edit_key[0] in ['S', 'M']:
                if len(gold_edit) > 3 and len(pred_edit) > 3 and gold_edit[3] == pred_edit[3]:
                    correction_TP += 1
                else:
                    correction_FP += 1
            else:  # Deletion operation
                correction_TP += 1

        # Undetected errors are also counted as uncorrected
        correction_FN += len(gold_edit_set - pred_edit_set)
        correction_FP += len(pred_edit_set - gold_edit_set)

    # Calculate evaluation metrics
    metrics = {}

    # Detection metrics
    detection_precision = detection_TP / (detection_TP + detection_FP) if (detection_TP + detection_FP) > 0 else 0
    detection_recall = detection_TP / (detection_TP + detection_FN) if (detection_TP + detection_FN) > 0 else 0
    detection_f1 = (
        2 * (detection_precision * detection_recall) / (detection_precision + detection_recall)
        if (detection_precision + detection_recall) > 0
        else 0
    )

    # F0.5 metric calculation
    detection_f05 = (
        (1 + 0.5**2) * (detection_precision * detection_recall) / ((0.5**2 * detection_precision) + detection_recall)
        if (detection_precision + detection_recall) > 0
        else 0
    )

    # Correction metrics
    correction_precision = correction_TP / (correction_TP + correction_FP) if (correction_TP + correction_FP) > 0 else 0
    correction_recall = correction_TP / (correction_TP + correction_FN) if (correction_TP + correction_FN) > 0 else 0
    correction_f1 = (
        2 * (correction_precision * correction_recall) / (correction_precision + correction_recall)
        if (correction_precision + correction_recall) > 0
        else 0
    )

    # F0.5 metric calculation
    correction_f05 = (
        (1 + 0.5**2)
        * (correction_precision * correction_recall)
        / ((0.5**2 * correction_precision) + correction_recall)
        if (correction_precision + correction_recall) > 0
        else 0
    )

    # Calculate sample-level accuracy
    accuracy = sum(1 for sample in predictions if sample['prediction'] == sample['target']) / len(predictions)

    # Calculate character-level accuracy
    total_chars = sum(len(sample['target']) for sample in predictions)
    correct_chars = sum(
        sum(1 for p_char, t_char in zip(sample['prediction'], sample['target']) if p_char == t_char)
        for sample in predictions
    )
    character_accuracy = correct_chars / total_chars if total_chars > 0 else 0

    # Return all metrics
    metrics = {
        'accuracy': accuracy,
        'character_accuracy': character_accuracy,
        'detection_precision': detection_precision,
        'detection_recall': detection_recall,
        'detection_f1': detection_f1,
        'detection_f05': detection_f05,
        'correction_precision': correction_precision,
        'correction_recall': correction_recall,
        'correction_f1': correction_f1,
        'correction_f05': correction_f05,
        # F0.5 as the final evaluation metric
        'final_score': correction_f05,
    }

    return metrics


def print_detailed_metrics(metrics: Dict[str, float]) -> None:
    """
    Print detailed evaluation metrics.

    Args:
        metrics: Dictionary containing evaluation metrics
    """
    print("=" * 10 + " Chinese Text Correction Evaluation Results " + "=" * 10)

    print("\nSample-level Evaluation:")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Character Accuracy: {metrics['character_accuracy']:.4f}")

    print("\nDetection Evaluation:")
    print(f"Precision: {metrics['detection_precision']:.4f}")
    print(f"Recall: {metrics['detection_recall']:.4f}")
    print(f"F1 Score: {metrics['detection_f1']:.4f}")
    print(f"F0.5 Score: {metrics['detection_f05']:.4f}")

    print("\nCorrection Evaluation:")
    print(f"Precision: {metrics['correction_precision']:.4f}")
    print(f"Recall: {metrics['correction_recall']:.4f}")
    print(f"F1 Score: {metrics['correction_f1']:.4f}")
    print(f"F0.5 Score: {metrics['correction_f05']:.4f}")

    print("\nFinal Score:")
    print(f"F0.5 Score: {metrics['final_score']:.4f}")
    print("=" * 45)


def evaluate_from_files(src_path: str, tgt_path: str, pred_path: str) -> Dict[str, float]:
    """
    Evaluate correction performance from file paths.

    Args:
        src_path: Path to source text file
        tgt_path: Path to target text file
        pred_path: Path to prediction text file

    Returns:
        Dictionary containing evaluation metrics
    """
    sources = []
    targets = []
    predictions = []

    with open(src_path, 'r', encoding='utf-8') as f:
        for line in f:
            items = line.strip().split('\t')
            if len(items) > 1:
                sources.append(items[1])
            else:
                sources.append(line.strip())

    with open(tgt_path, 'r', encoding='utf-8') as f:
        for line in f:
            targets.append(line.strip())

    with open(pred_path, 'r', encoding='utf-8') as f:
        for line in f:
            predictions.append(line.strip())

    assert len(sources) == len(targets) == len(predictions), "Number of lines in input files is inconsistent"

    # Build predictions list
    pred_list = [
        {'source': src, 'target': tgt, 'prediction': pred, 'label': 1 if src != tgt else 0}
        for src, tgt, pred in zip(sources, targets, predictions)
    ]

    return evaluate_performance(pred_list)
