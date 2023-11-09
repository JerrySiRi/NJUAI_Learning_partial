import random
import csv
import numpy as np
import math
from tqdm import tqdm
from sklearn.preprocessing import normalize
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)


def GenerateData(data_path):
    with open(data_path, "r", encoding="utf-8") as f:
        data = np.array(list(csv.reader(f))[1:])
    N = data.shape[0]
    X = data[:, :-1].astype(np.float64)
    X = normalize(X, axis=0, norm="max")  # avoid overflow problem
    X = np.insert(X, 0, values=1, axis=1)  # insert bias term
    print("Dimension of the feature data:", X.shape)
    y = data[:, -1].astype(np.int32).reshape(N, 1)
    test_id = np.random.choice(N, int(0.25 * N), replace=False)
    X_train = np.delete(X, test_id, axis=0)
    y_train = np.delete(y, test_id, axis=0)
    X_test = X[test_id]
    y_test = y[test_id]

    return X_train, y_train, X_test, y_test


def nabla_l(w_old, X, y):
    """
    A function expression for the gradient of l(w) w.r.t. w
    """

    p = 1 / (1 + math.e ** (-X @ w_old))
    return X.T @ -(y - p)


def nabla_2_l(w_old, X, y):
    """
    A function expression for the Hessian matrix of l(w) w.r.t. w
    """
    # %%
    # TODO: Compute the Hessian matrix of log-likelihood function
    p = 1 / (1 + math.e ** (-X @ w_old))
    return (X.T) @ (X*p*(1-p))
    # End your code here
    # %%


def Newton_Solver_for_LR(w_old, nabla_l, nabla_2_l, X, y):
    """
    Solving the minimizer for log-likelihood in Logistic Regression((3.27) in the book).
        param nabla_l: function, nabla_l(w) is the gradient of l(w) w.r.t. w
        param nabla_2_l: function, nabla_2_l(w) is the Hessian matrix of l(w) w.r.t. w
        param X, y: parameters in l(w)
        return: optimize one_step for w_new
    """
    # %%
    # TODO: Finish the code here
    u, s, v = np.linalg.svd(nabla_2_l(w_old,X,y), full_matrices=False)  # 截断式矩阵分解
    inv = np.matmul(v.T * 1 / s, u.T)  # 求逆矩阵
    w_new = w_old-inv @ nabla_l(w_old,X,y)
    # End your code here
    # %%

    return w_new


class LogisticRegression:
    def __init__(self, iter_num, Solver):
        self.name = "Logistic Regression"
        self.iter_num = iter_num
        self.Solver = Solver

    def train(self, X_train, y_train):
        self.w = np.random.randn(X_train.shape[1], 1)  # initialize w_0
        for _ in tqdm(range(self.iter_num)):
            self.w = self.Solver(
                w_old=self.w,
                nabla_l=nabla_l,
                nabla_2_l=nabla_2_l,
                X=X_train,
                y=y_train,
            )
        return self.w

    def predict(self, X_new):
        # %%
        # TODO: Finish the code here to predict the label for new data
        # Please return the probability vector P(X=1), rather than a 0-1 vector
        p = 1 / (1 + math.e ** (-X_new @ self.w))
        N=X_new.shape[0]#新数据有几个
        y_prob = p
        # End your code here
        # %%

        return y_prob

    def evalute(self, X, y):
        # %%
        # TODO: Compute the accuracy when using parameter self.w
        p = 1 / (1 + math.e ** (-X @ self.w))#最终计算的结果
        N=X.shape[0]
        '''
        max=0
        div_target=0
        for step in range(0,100,1):#python中range步长最多只能取到整数！
            sum = 0
            for i in range(N):
                if p[i]>=(step/100) and y[i]==1:
                    sum+=1
                elif p[i]<(step/100) and y[i]==0:
                    sum+=1
            if sum >= max:
                max=sum
                div_target=step/100
            print("step=",step,"sum=",sum)
        print("max=",max,"div",div_target)----------在0.44为分界的时候最好
        '''
        sum=0
        for i in range(N):
            if p[i]>=0.44 and y[i]==1:
                sum+=1
            elif p[i]<0.44 and y[i]==0:
                sum+=1
        accuracy = sum/N
        # End your code here
        # %%

        return accuracy


def PlotROC(fpr,tpr,auc):
    # %%
    # TODO: Plot the ROC
    plt.figure(figsize=(8, 7), dpi=100, facecolor='w')      # dpi:每英寸长度的像素点数；facecolor 背景颜色
    plt.xlim((0, 1.02))                                     # x,y 轴刻度的范围
    plt.ylim((0, 1.02))
    plt.xticks(np.arange(0, 1.1, 0.1))                      # 绘制刻度
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.plot(fpr, tpr, 'r-', lw=2, label='AUC=%.4f' % auc)  # 绘制AUC 曲线
    plt.legend(loc='lower right')                           #设置显示标签的位置
    plt.xlabel('False Positive Rate(FPR)', fontsize=14)     # 绘制x,y 坐标轴对应的标签
    plt.ylabel('True Positive Rate(TPR)', fontsize=14)
    plt.grid(b=True, ls=':')                                # 绘制网格作为底板;b是否显示网格线；ls表示line style
    plt.title(u' ROC curve And  AUC', fontsize=18)          # 打印标题
    plt.show()

    # %%


if __name__ == "__main__":
    set_seed(6)
    iter_num = 20
    data_path = "data.csv"

    (
        X_train,
        y_train,
        X_test,
        y_test,
    ) = GenerateData(data_path)

    model = LogisticRegression(
        iter_num=iter_num,
        Solver=Newton_Solver_for_LR,
    )
    model.train(X_train=X_train, y_train=y_train)
    test_acc = model.evalute(X_test, y_test)
    print("Accuracy in test set: %.4f" % (test_acc))
    y_prob = model.predict(X_test)
    #y_prob是模型预测出来的【【【BUG！！！此时的y_prob一定是带有小数的值呢！！！，是要排序的】】】
    #y_test是X_test在数据集中真正的标记呢！》》通过这两个产生假正例率（FPR）+真正例率(TPR)

    from sklearn import metrics
    # TODO: Compute the AUC
    #算作业中的AUC和ROC
    #y_test=np.array([1,0,1,0,1,0,0,1,0])
    #y_prob=np.array([0.9,0.8,0.8,0.7,0.6,0.5,0.4,0.4,0.2])
    fpr, tpr,_= metrics.roc_curve(y_test, y_prob)
    auc_value = metrics.auc(fpr, tpr)
    # %%
    print("AUC in test set: %.4f" % (auc_value))
    import matplotlib.pyplot as plt
    PlotROC(fpr,tpr,auc_value)