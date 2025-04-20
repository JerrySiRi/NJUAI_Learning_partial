#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data analysis module for Chinese Text Correction task.
This module provides functions for analyzing error patterns in the dataset.
"""

import re
import json
import numpy as np
from typing import Dict, List, Tuple, Any
from collections import Counter, defaultdict

# Try to import optional dependencies for visualization
try:
    import matplotlib.pyplot as plt

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not available. Visualization features will be disabled.")

try:
    import Levenshtein
    LEVENSHTEIN_AVAILABLE = True
except ImportError:
    LEVENSHTEIN_AVAILABLE = False
    print("Warning: Levenshtein库未在当前环境中被下载，请使用\"conda list\"检查当前环境配置.")


def analyze_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze the dataset to extract statistics and error patterns.
    Args:
        data: List of dictionaries containing the data.
    Returns:
        Dictionary containing analysis results.
    """
    # TODO 完成数据分析，可以从数据中观察【统计信息】、【错误模式】和【难度分布】等，帮助后续的方法设计。
    # 用Levenshtein库很方便~
    # 【把纠错行为分类成了“替换”，“删除”，“插入”】
    # 而不是spelling errors，redundant words，missing words，word order errors
    error_type_counter = Counter() # 对三种错误形式进行计数，和dict功能类似，但封装的更好呢
    total_edits = 0
    total_samples = len(data)

    for sample in data:
        source = sample["source"]
        target = sample["target"]
        if source == target:
            continue
        edits = Levenshtein.opcodes(source, target)

        for tag, i1, i2, j1, j2 in edits:
            if tag == "equal":
                continue
            elif tag == "replace":
                error_type_counter["Replace"] += 1
            elif tag == "insert":
                error_type_counter["Insert"] += 1
            elif tag == "delete":
                error_type_counter["Delete"] += 1
            total_edits += 1

    # 当前数据集中所有样本的三种错误形式的汇总~
    error_distribution = {
        "error_type_distribution": dict(error_type_counter),
        "total_edits": total_edits,
        "total_samples": total_samples
    }

    return error_distribution


def visualize_error_distribution(analysis_results: Dict[str, Any], data_type: str="Training data") -> None:
    """
    Visualize the error distribution from analysis results.
    Args:
        analysis_results: Dictionary containing analysis results.
    """
    if not MATPLOTLIB_AVAILABLE:
        print("Cannot visualize results: matplotlib not available.")
        return

    # TODO 可视化数据分析
    
    # Tip：使用 .get("key", default_value) 可以在 key 不存在时自动返回默认值，设定默认值是一个空字典 {}
    # 【不会因为因为keyerror而引发的报错行为】
    # 【但可能会让调试找不到错误点】
    distribution = analysis_results.get("error_type_distribution", {})
    labels = list(distribution.keys())
    values = list(distribution.values())
    
    plt.rcParams['font.family'] = 'SimHei'
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建画布：1行2列子图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5), gridspec_kw={'width_ratios': [1, 1.5]})
    
    # ---------- 柱状图 ----------
    width = 0.3
    bars = ax1.bar(labels, values, width, color=['skyblue', 'lightgreen', 'salmon'])
    ax1.set_title(f"{data_type}纠错类型分布（柱状图）")
    ax1.set_xlabel("错误类型")
    ax1.set_ylabel("出现次数")
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, yval + 2, int(yval), ha='center', va='bottom')

    # ---------- 饼图 ----------
    explode = [0.03, 0.06, 0.10]
    ax2.pie(values, labels=labels, explode = explode, autopct='%1.1f%%', \
                startangle=0, shadow=True,\
                    colors=['skyblue', 'lightgreen', 'salmon'])
    ax2.set_title(f"{data_type}纠错类型分布（饼状图）")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    
    train_data = "data/train.jsonl"
    test_data = "data/test.jsonl"

    # 加载 jsonl 文件
    train_dataset = []
    test_dataset = []
    with open(train_data, "r", encoding="utf-8") as f:
        for line in f:
            train_dataset.append(json.loads(line.strip()))
    train_results = analyze_data(train_dataset)
    print("训练集分析结果：", train_results)
    visualize_error_distribution(train_results, "Training data")
    
    with open(test_data, "r", encoding="utf-8") as f:
        for line in f:
            test_dataset.append(json.loads(line.strip()))
    test_results = analyze_data(test_dataset)
    print("测试集分析结果，仅用于结果分析说明，不对模型性能产生影响：", test_results)
    visualize_error_distribution(test_results, "Testing data")

    