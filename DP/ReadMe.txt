
1. 文件相对路径要求
请把random.txt放在和EnumSort、MergeSort、QuickSort同一目录下。代码中均使用相对路径索引random.txt文件

2. 运行方式

2.1  
三种算法的串行、并行版本均在各自的唯一.java文件之中
三个.java文件中整型变量par_or_seq = 0/1指示当前算法是串行或并行。
其中par_or_seq = 0是串行、par_or_seq = 1是并行

2.2
不需要手动创建6个order.txt文件，如若当前文件夹下没有对应的order.txt文件，
代码中会自动创建对应.txt文件。