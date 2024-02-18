import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import cvxpy as cp
from sklearn import metrics
import matplotlib.pyplot as plt
# 二分类数据集。数据维度30，每一维都是数值类型
# 训练阶段：label_X label_Y unlabel_X 
# 测试阶段：分别在unlabel_Y上进行测试、在test_X上跑+test_Y上测试
# TODO：报告两批数据的准确率、ROC曲线、AUC值


# 尝试使用各种方式提升模型在测试集上性能：数据预处理 + 超参数调参

# 两个单位向量，用于目标函数中的求和
unit_1 = np.array([1 for x in range(114)])
unit_2 = np.array([1 for x in range(342)])    
# 四个优化变量：w、b、xi_1、xi_2
w = cp.Variable(30) # 如果不给维度，就认为是标量了！
b = cp.Variable()
xi_1 = cp.Variable(114)
xi_2 = cp.Variable(342)
# 单位矩阵：用于表示QP中二次项
E_1 = np.eye(30)

class TSVM:

    def fit(self, X_l, y_l, X_u):
        for index in range(0,len(y_l)):
            if y_l[index] == 0:
                y_l[index] = -1

        initial_svm = SVC(C=1,kernel="linear").fit(X_l,y_l)
        y_u_pre = initial_svm.predict(X_u) # 唯一一次对未标记样本进行指派

         # 对y_u_pre更新
        for index in range(0,len(y_u_pre)):
            if y_u_pre[index] == 0:
                y_u_pre[index] = -1

        # 【【【此时是0、1的标记---要产生0，-1的标记呢！】】】
        # Tip：可调节参数 二者的比例 & 二者的绝对值。因为优化式中不知含有这两项，还有w项！
        C_u=np.random.randint(low=10,high=20)
        C_l=np.random.randint(low=1800,high=2000)

        while C_u < C_l:
            w, b, xi_1, xi_2 = self.con_sol(C_l, C_u, X_l, y_l, X_u, y_u_pre)
            for y1_index in range(0,len(y_u_pre)):
                for y2_index in range(0,len(y_u_pre)):
                    if y_u_pre[y1_index] * y_u_pre[y2_index]<0 and xi_2[y1_index]>0 and xi_2[y2_index]>0 \
                        and xi_2[y1_index]+xi_2[y2_index]>2:
                        y_u_pre[y1_index] = - y_u_pre[y1_index]
                        y_u_pre[y2_index] = - y_u_pre[y2_index]
                        w, b, xi_1, xi_2 = self.con_sol(C_l, C_u, X_l, y_l, X_u, y_u_pre)
            # print(class_not_balance(y_u_pre))
            C_u = min(2*C_u,C_l)
        # print("xi1=",xi_1,'\n',"xi2=",xi_2)
        # print("目标函数第一项","w的二范数平方",0.5*np.array(w).T @ np.array(w))
        # print("目标函数第二项","xi_1",C_l* (unit_1.T @ xi_1))
        # print("目标函数第三项","xi_2",C_u* (unit_2.T @ xi_2))
        self.w = w
        self.b = b
        
        X_f = np.concatenate((X_l ,X_u),axis=0)
        y_f = np.concatenate((y_l ,y_u_pre),axis=0)
        final_svm = SVC(C=1,kernel="linear",probability=True).fit(X_f,y_f) # 【纯半监督理解】
        for index in range(0,len(y_u_pre)):
            if y_u_pre[index] == -1:
                y_u_pre[index] = 0
        return (y_u_pre,final_svm) # 返回未标记样本的预测结果
    
    def predict(self, X): #【直推理解】
        """
        预测函数
        :param X: 预测数据的特征
        :return: 数据对应的预测值
        """
        result = np.where(X @ self.w + self.b >= 0, 1, -1)
        return result



    # 重新求解TSVM中的优化问题
    def con_sol(self, C_l, C_u, X_l, y_l, X_u, y_u_pre):
        obj = cp.Minimize((1/2)*cp.quad_form(w,E_1) + C_l *(unit_1.T @ xi_1) + C_u*(unit_2.T @ xi_2 ))
        # 和numpy不同，cvxpy中主元素相乘不使用*了，而改成了multiply函数
        cons = [cp.multiply(y_l , (X_l@ w + b)) >= unit_1 - xi_1, 
        cp.multiply(y_u_pre ,(X_u@ w + b)) >= unit_2 - xi_2,
        xi_1>=0,xi_2>=0 ]
        prob = cp.Problem(obj,cons)
        prob.solve(solver=cp.ECOS)
        # 迭代次数过多，可以使用更强的优化器：如ECOS求解器
        # verbose=True可以显示优化过程中具体信息
        return (w.value,b.value,xi_1.value,xi_2.value)



    



def class_not_balance(y_label):# 类别不平衡检测
    num_ne=0
    num_po=0
    for item in y_label:
        if item==-1:
            num_ne+=1
        else:
            num_po+=1
    return num_ne/num_po


def normalize(data):# 数据归一化处理
    data = pd.DataFrame(data)
    scaler = MinMaxScaler() #实例化
    scaler = scaler.fit(data) #fit，在这里本质是生成min(x)和max(x)
    result = scaler.transform(data) #通过接口导出结果
    return result

def standarize(data):#数据标准化处理
    scaler = StandardScaler() #实例化
    scaler = scaler.fit(data) #fit，本质是生成均值和方差
    x_std = scaler.transform(data) #通过接口导出结果
    return x_std

def load_data():
    label_X = np.loadtxt('label_X.csv', delimiter=',')
    label_y = np.loadtxt('label_y.csv', delimiter=',', dtype=np.int32)
    unlabel_X = np.loadtxt('unlabel_X.csv', delimiter=',')
    unlabel_y = np.loadtxt('unlabel_y.csv', delimiter=',', dtype=np.int32)
    test_X = np.loadtxt('test_X.csv', delimiter=',')
    test_y = np.loadtxt('test_y.csv', delimiter=',', dtype=np.int32)
    return label_X, label_y, unlabel_X, unlabel_y, test_X, test_y

def precision(label_1,label_2):
    sum=0
    for index in range(0,len(label_1)):
        if label_1[index] == label_2[index]:
            sum+=1
    return sum/len(label_1)

def preprocess(data):
    for index in range(0,len(data)):
        if data[index] == -1:
            data[index] = 0
    return data

def ROC_AUC_PlotROC(prob,real,string):# 画ROC曲线，计算AUC值
    prob_y=np.array(prob)[:,1] # 概率大-最有可能是正例，概率小-最有可能是负例！！！》》应该取第二列中数据
    fpr, tpr,_= metrics.roc_curve(real, prob_y)
    auc_value = metrics.auc(fpr, tpr)
    print("AUC in",string,"%.4f" % (auc_value))
    plt.figure(figsize=(8, 7), dpi=100, facecolor='w')      # dpi:每英寸长度的像素点数；facecolor 背景颜色
    plt.xlim((0, 1.02))                                     # x,y 轴刻度的范围
    plt.ylim((0, 1.02))
    plt.xticks(np.arange(0, 1.1, 0.1))                      # 绘制刻度
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.plot(fpr, tpr, 'r-', lw=2, label='AUC=%.4f' % auc_value)  # 绘制AUC 曲线
    plt.legend(loc='lower right')                           #设置显示标签的位置
    plt.xlabel('False Positive Rate(FPR)', fontsize=14)     # 绘制x,y 坐标轴对应的标签
    plt.ylabel('True Positive Rate(TPR)', fontsize=14)
    plt.grid(b=True, ls=':')                                # 绘制网格作为底板;b是否显示网格线；ls表示line style
    plt.title(u' ROC curve And  AUC', fontsize=18)          # 打印标题
    plt.show()


def prediction(model,real_x,real_y,string):
    pre_y = model.predict(real_x)
    prob_y = model.predict_proba(real_x)
    pre_y = preprocess(pre_y)
    print(string,"预测精度为",precision(pre_y,real_y))
    ROC_AUC_PlotROC(prob_y,real_y,string)



if __name__ == '__main__':
    label_X, label_y, unlabel_X, unlabel_y, test_X, test_y \
        = load_data()
    tsvm = TSVM()
    y_u_pre,final_svm = tsvm.fit(standarize(label_X), label_y, standarize(unlabel_X)) # 拿到返回的未标记样本的预测结果 & 最终的svm
    # 此时拿到的y_u_pre标记全是0和1啦！！！
    print("未标记数据（直推）:预测精度为",precision(y_u_pre,unlabel_y))
    print('\n')
    # 【直推理解】
    # y_unlabel = tsvm.predict(unlabel_X)
    # 【纯半监督理解】
    prediction(final_svm,standarize(unlabel_X),unlabel_y,"未标记数据 (纯)半监督：")
    print('\n')
    # 【直推理解】
    #  y_test = tsvm.predict(test_X)
    # 【纯半监督理解】
    prediction(final_svm,standarize(test_X),test_y,"测试数据 (纯)半监督：")


"""
(此结果好像收敛了，再提高C_l的值效果也不会增加了)
(好像是对的，最后sklearn训练和咱们每次解决优化问题做的事情应该是一样的！)
未标记数据（直推）:预测精度为 0.9385964912280702
未标记数据（纯半监督）：使用生成的svm模型预测精度为 0.9385964912280702
AUC in 未标记数据 0.9752

测试数据（纯半监督）：预测精度为 0.9469026548672567 
AUC in 测试数据 0.9835
"""
    