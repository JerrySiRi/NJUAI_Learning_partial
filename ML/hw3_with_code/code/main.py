import random
import csv
import numpy as np
import math
from sklearn.preprocessing import normalize
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
'''
数据集和第一次作业相同：
---一共27列，前26列为收集到的特征（x_i），最后一列是是否违约（y_i）
---一共含有8032条，随机抽取70%的数据作为训练集，剩余30%是测试集

TODO：
【step1】实现以下分类算法
1. 对数几率回归（LR），3.3节
2. 决策树模型（Decision Tree），第4章
3. 支持向量机（SVM），第6章

【step2：】
1. 记录在训练集、测试集上的精度
2. 不同模型在测试集上的ROC以及AUC
3. 把各个模型的ROC曲线画到同一张图中，对比各个模型的表现

本次作业可以使用 Scikit-learn 库中的类来完成。
请同学们自行查阅 Scikit-learn 库中的说明文档，并调用其中的类或函数实现本次作业。

'''

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)


def GenerateData(data_path):
    with open(data_path, "r", encoding="utf-8") as f:
        data = np.array(list(csv.reader(f))[1:])
    N = data.shape[0]#shape[0]读取ndarray第一维度的长度,相当于行数。行数！！即数据的个数
    X = data[:, :-1].astype(np.float64)#取的所有【训练数据】，除了第一行是标记呢
    X = normalize(X, axis=0, norm="max")  # [规范化]avoid overflow problem
    y = data[:, -1].astype(np.int32).reshape(N, 1) # 取的所有【测试数据】
    test_id = np.random.choice(N, int(0.3 * N), replace=False)
    X_train = np.delete(X, test_id, axis=0)#【训练集X_train】
    y_train = np.delete(y, test_id, axis=0)#【测试集Y_train】
    X_test = X[test_id]#【测试集】
    y_test = y[test_id]#【测试集】
    print("Dimension of the feature data in training set:", X_train.shape)
    print("Dimension of the feature data in testing set:", X_test.shape)
    return X_train, y_train, X_test, y_test



def PlotROCs(y_prob_lr, y_prob_tree, y_prob_svm, y_test):
#def PlotROC(fpr, tpr, auc):
    # TODO: Plot the ROCs in one graph
    from sklearn import metrics
    fpr_dt, tpr_dt, _ = metrics.roc_curve(y_test, y_prob_tree)
    auc_value_dt = metrics.auc(fpr_dt, tpr_dt)
    fpr_lr, tpr_lr, _ = metrics.roc_curve(y_test, y_prob_lr)
    auc_value_lr = metrics.auc(fpr_lr, tpr_lr)
    fpr_svm, tpr_svm, _ = metrics.roc_curve(y_test, y_prob_svm)
    auc_value_svm = metrics.auc(fpr_svm, tpr_svm)


    plt.figure(figsize=(8, 7), dpi=100, facecolor='w')  # dpi:每英寸长度的像素点数；facecolor 背景颜色
    plt.xlim((0, 1.02))  # x,y 轴刻度的范围
    plt.ylim((0, 1.02))
    plt.xticks(np.arange(0, 1.1, 0.1))  # 绘制刻度
    plt.yticks(np.arange(0, 1.1, 0.1))
    #plt.plot(fpr_lr, tpr_lr, lw=2, label='AUC_lr=%.4f' % auc_value_lr,color='b')  # 绘制AUC 曲线
    #plt.plot(fpr_dt, tpr_dt, lw=2, label='AUC_dt=%.4f' % auc_value_dt,color='g')  # 绘制AUC 曲线
    plt.plot(fpr_svm, tpr_svm, lw=2, label='AUC_svm=%.4f' % auc_value_svm,color='r')  # 绘制AUC 曲线
    plt.legend(loc='lower right')  # 设置显示标签的位置
    plt.xlabel('False Positive Rate(FPR)', fontsize=14)  # 绘制x,y 坐标轴对应的标签
    plt.ylabel('True Positive Rate(TPR)', fontsize=14)
    plt.grid( ls=':')  # 绘制网格作为底板;b是否显示网格线；ls表示line style
    plt.title(u' ROC curve And  AUC', fontsize=18)  # 打印标题
    plt.show()




def main(data_path):
    (X_train, y_train, X_test, y_test,) = GenerateData(data_path)
    # %%
    # TODO: Plot the ROCs in one graph
    #==================决策树========================
    from sklearn import tree  # 导入决策树模块
    max=0
    target=0
    clf = tree.DecisionTreeClassifier(criterion="entropy",
                                    random_state=30,
                                    splitter="random",
                                    max_depth=6,
                                    min_samples_leaf=10,
                                    min_samples_split=10)  # 实例化
    #TODO:经过调整参数，发现决策树最大深度为6时最好【剪枝】。若一个节点不足10个样本或分支后不足10个样本就不分支【剪枝】
    tree_model = clf.fit(X_train, y_train)# 【决策树训练后的模型】
    tree_result_train = tree_model.score(X_train, y_train)# 【训练集中的精度】
    tree_result_test = tree_model.score(X_test, y_test)  # 【测试集中的精度】
    print("Decision tree:Accuracy in train set: %.4f" % (tree_result_train))
    print("Decision tree:Accuracy in test set: %.4f" % (tree_result_test))


    #========================线性回归================

    from sklearn import linear_model
    lr = linear_model.LogisticRegression(C=0.6)#采用了逻辑斯蒂回归，也就是对数几率回归！
    #TODO:经调参，在正则化系数取得0.6的时候效果最好啦！
    lr_model = lr.fit(X_train, y_train)# 【线性回归训练后的模型】
    lr_result_train = lr_model.score(X_train, y_train)  # 【测试集中的精度】
    lr_result_test = lr_model.score(X_test, y_test)# 【测试集中的精度】
    print("LR:Accuracy in train set: %.4f" % (lr_result_train))
    print("LR:Accuracy in test set: %.4f" % (lr_result_test))



    #======================支持向量机=================
    from sklearn import svm
    svm_tem = svm.SVC(kernel="linear",probability=True,C=0.5)
    #TODO：不断调整SVM所应用的核函数，在线性核（linear）、多项式核（poly）、双曲正切核（sigmod）、高斯径向核（rbf）
    #最终发现线性核实现准确度最高！
    #TODO:引入软间隔，同时衡量“训练样本的正确分类【经验风险】”和“决策函数的边际最大化【结构风险】”
    #最终发现C=0.5效果最好
    svm_model = svm_tem.fit(X_train, y_train)
    svm_result_train = svm_model.score(X_train, y_train)# 【测试集中的精度】
    svm_result_test = svm_model.score(X_test, y_test)  # 【测试集中的精度】
    print("SVM:Accuracy in train set: %.4f" % (svm_result_train))
    print("SVM:Accuracy in test set: %.4f" % (svm_result_test))
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # predicted probability on test set using logistic regression model
    y_prob_lr = lr_model.predict_proba(X_test)#训练后的模型对测试集进行预测！
    y_prob_lr = y_prob_lr[:,1]#预测属于正例的概率，在绘制roc的时候，从大到小来排，不断分隔即可啦！！！
    print("linear",y_prob_lr)#----打印出来的是只有0和1！

    # predicted probability on test set using tree model
    y_prob_tree = tree_model.predict_proba(X_test)#训练后的模型对测试集进行预测！
    y_prob_tree = y_prob_tree[:,1]
    print("tree",y_prob_tree)#---打印出来的是会有小数点的！

    # predicted probability on test set using svm model
    y_prob_svm = svm_model.predict_proba(X_test)
    y_prob_svm = y_prob_svm[:, 1]
    print("svm",y_prob_svm)#---打印出来的只有0和1
    # %%


    PlotROCs(y_prob_lr, y_prob_tree, y_prob_svm, y_test)






if __name__ == "__main__":
    set_seed(6)
    data_path = "data.csv"
    main(data_path)

