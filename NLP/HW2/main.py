#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main script for Chinese Text Correction task.
This script provides a framework for analyzing and correcting errors in Chinese text.
"""

import os
import json
import argparse
from typing import Dict, List, Tuple, Any
from tqdm import tqdm

# Import modules
from data_analysis import analyze_data, visualize_error_distribution
from rule_based import RuleBasedCorrector
from statistical import *
from evaluation import evaluate_performance, print_detailed_metrics


def load_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Load data from jsonl file.

    Args:
        file_path: Path to the jsonl file.

    Returns:
        List of dictionaries containing the data.
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data


def main():
    """
    Main function to run the Chinese text correction pipeline.
    """
    parser = argparse.ArgumentParser(description='Chinese Text Correction')
    parser.add_argument('--train_file', type=str, default='data/train.jsonl', help='Path to training data')
    parser.add_argument('--test_file', type=str, default='data/test.jsonl', help='Path to test data')
    parser.add_argument(
        '--method',
        type=str,
        choices=['rule_pos', 'rule_dep', 'statistical', 'ensemble', 'pretrained'],
        default='statistical',
        help='Correction method to use',
    )
    # 巧！根据是否出现决定真假，而不用显示赋予他们True or False！
    # 这里--analyze，如果出现了那么就会被赋值为True！
    parser.add_argument('--analyze', action='store_true', help='Perform data analysis')
    parser.add_argument(
        '--statistical_method', 
        type=str, 
        choices = ['ngram', 'ml'],
        default='ml', 
        help='Statistical method to use')
    parser.add_argument('--evaluate', action='store_true', help='To choose whether we need evaluation')
    
    args = parser.parse_args()

    # Load data
    print("Loading data...")
    train_data = load_data(args.train_file)
    test_data = load_data(args.test_file)

    # TODO 1: Data analysis
    if args.analyze:
        print("\nPerforming data analysis...")
        analysis_results = analyze_data(train_data)
        visualize_error_distribution(analysis_results)

    # TODO 2: Initialize corrector based on method
    # 基于规则的额外处理（grammar rules有两种实现）
    if args.method.find("_") == -1:
        method = args.method
    else:
        method = args.method[0: args.method.find("_")]
        choice = args.method[args.method.find("_")+1: ]
    
    if method == 'rule':
        print("\nInitializing rule-based corrector...")
        corrector = RuleBasedCorrector()
        corrector.train(train_data, choice)
    elif method == 'statistical':
        print("\nInitializing statistical corrector...")
        corrector = StatisticalCorrector(args.statistical_method)
        corrector.train(train_data)
    elif method == 'pretrained':
        print("\nInitializing pretrained model...")
        model = BertCRFCorrector()
        corrector = StatisticalCorrector(args.statistical_method)
        corrector._train_ml_model(model, train_data + test_data)
    elif method == 'ensemble':
        print("\nInitializing ensemble corrector...")
        # TODO start
        # Implement ensemble method that combines rule-based and statistical methods
        rule_corrector = RuleBasedCorrector()
        rule_corrector.train(train_data)

        stat_corrector = StatisticalCorrector()
        stat_corrector.train(train_data)

        # You can implement a simple voting mechanism or a more sophisticated ensemble method
        # For example, you could use rule-based method first, then apply statistical method on the results
        # Or you could use different methods for different types of errors
        # TODO end


    # TODO 3: Evaluate on test data
    if args.evaluate:
        print("\nEvaluating on test data...")
        predictions = []
        test_data = test_data
        for sample in tqdm(test_data, ncols=100):
            source = sample['source']
            corrected = str()
            if method == 'pretrained':
                corrected = corrector._correct_with_ml(model, source)
            else:
                if args.method.find("_") != -1:
                    corrected = corrector.correct(source, choice)
                else:
                    corrected = corrector.correct(source)
            """
            print("==原来的句子:", source,"\n")
            print("==更改过后的句子:", corrected,"\n")
            print("------------------")
            """
            
            predictions.append(
                {'source': source, 'prediction': corrected, 'target': sample['target'], 'label': sample['label']}
            )

        # Calculate evaluation metrics
        metrics = evaluate_performance(predictions)
        print_detailed_metrics(metrics)


if __name__ == "__main__":
    main()
