from typing import Dict, List, Tuple, Any, Set

# ------------- 尝试 1 -------------- #
from transformers import AutoTokenizer, AutoModelForTokenClassification
from treebuilder import TreeBuilder

class HuggingfaceConstituencyParser:
    # A constituent parser based on LTP's HuggingFace model (LTP/biaffine-constituency)
    # Outputs one constituent label per character in the input.

    def __init__(self):
        print("Loading constituent parser model...")
        self.tokenizer = AutoTokenizer.from_pretrained("fnlp/biaffine-parser-zh")
        self.model = AutoModelForTokenClassification.from_pretrained("fnlp/biaffine-parser-zh")
        self.builder = TreeBuilder(self.tokenizer, self.model)

    def get_constituent_labels(self, text: str) -> List[str]:

        # Perform constituent parsing and assign each character in the text a constituent label

        # Parse into tree structure
        try:
            trees = self.builder([text])
            tree = trees[0]
        except Exception as e:
            raise RuntimeError(f"TreeBuilder failed: {e}")

        # Assign labels to each character
        labels = [""] * len(text)
        offset = 0

        def assign(node):
            nonlocal offset
            if not node.children:
                for i in range(len(node.word)):
                    if offset < len(labels):
                        labels[offset] = node.label
                        offset += 1
            else:
                for child in node.children:
                    assign(child)
        assign(tree)

        if len(labels) != len(text):
            raise ValueError(f"Length mismatch: text has {len(text)} chars, but got {len(labels)} labels")
        return labels



# -------------------- 尝试 2 --------------------- #
from ltp import LTP

class LTPWrapper:
    def __init__(self):
        self.ltp = LTP("LTP/base")
        print(dir(self.ltp))  # 查看有哪些函数

    def get_constituent_labels(self, text: str) -> list:

        # BUG：新版的ltp不支持seg, encoder接口，而是统一用pipeline了
        # 返回字符级别 constituent label。

        # Step 1: 先用 pipeline 分词
        output = self.ltp.pipeline([text], tasks=["cws"], return_dict=True)
        words = output["cws"][0]  # 分词结果，如 ['他的', '回答', '很', '精彩', '。']

        # Step 2: constituent 成分分析
        tree = self.ltp.constituency([words])[0]  # 注意这里输入的是词 list！

        # Step 3: 将每个词的 label 映射到字符（每字共享该词 label）
        labels = [""] * len(text)
        offset = 0

        def assign_labels(node):
            nonlocal offset
            if not hasattr(node, "children") or len(node.children) == 0:
                for i in range(len(node.word)):
                    labels[offset] = node.label
                    offset += 1
            else:
                for child in node.children:
                    assign_labels(child)

        assign_labels(tree)

        if len(labels) != len(text):
            raise ValueError(f"标签数 {len(labels)} 与文本长度 {len(text)} 不一致")
        return labels

