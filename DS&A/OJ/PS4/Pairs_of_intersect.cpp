#include <bits/stdc++.h>
#include <iostream>
using namespace std;
/*

n小于10的6次方
pi和qi都小于10的9次方【oj中的int是16位的，只有65536，还不够呢，得用long int】

5
1 3 5 4 6
4 5 2 7 6
*/


/*
现在的想法，按照pi先排序，再计算qi的逆序对就行啦！计算逆序对也是nlongn>>>整体的时间都是nlongn，应该问题不大
*/

//【BUG！】数组的长度和下标在有没有等号上面，可是不一样的处理呢！！！
//【BUG! 】对问题的的理解不透彻，**尤其是在换不同的做法的时候！**不同的理解，对不同变量的变化可都不一样！！！

//TODO：solution---每次可以通过cout来理解程序运行方式，而不是通过调试来迭代他！！！

void Merge(long int a[],long int b[],long int start,long int fen,long int end){//每次给pi排好序之后，并返回这次找到的线段交点数
//同时在merge a的时候，只以a元素的具体值，对b进行换位！！
    long int len_1=fen-start+1;
    long int len_2=end-fen;
    long int L[len_1],R[len_2];
    long int b_L[len_1],b_R[len_2];//要操作b的移动呢
    for(long int i=0;i<len_1;i++)
        {L[i]=a[start+i];b_L[i]=b[start+i];}
    for(long int i=0;i<len_2;i++)
        {R[i]=a[fen+i+1];b_R[i]=b[fen+i+1];}
    long int i=0,j=0;
    for(long int k=start;k<=end;k++){
        if(i==len_1){
            a[k]=R[j];
            b[k]=b_R[j];
            j++;
            continue;
        }
        if(j==len_2){
            a[k]=L[i];
            b[k]=b_L[i];
            i++;
            continue;
        }
        if(L[i]<=R[j]){
            a[k]=L[i];
            b[k]=b_L[i];
            i++;
        }
        else{
            a[k]=R[j];
            b[k]=b_R[j];
            j++;
        }
    }
}

void Merge_sort(long int a[],long int b[],long int start,long int end){//递归，先算出分界点，左边调用+右边调用，两侧同时Merge
//同时在merge_sort a的时候，只以a元素的具体值，对b进行换位！！
    if(start<end){
        long int fen=(start+end)/2;
        Merge_sort(a,b,start,fen);
        Merge_sort(a,b,fen+1,end);
        Merge(a,b,start,fen,end);
    }
}

//合并有序数列，并在合并时计算逆序对
long int mergeCountInversions(long int a[], long int left, long int mid,long int right,long int n)
{
	long int count = 0;
    long int len_1=mid-left+1;
    long int len_2=right-mid;
    long int L[len_1],R[len_2];
    for(long int i=0;i<len_1;i++)
        L[i]=a[left+i];
    for(long int i=0;i<len_2;i++)
        R[i]=a[mid+1+i];
	//归并到临时数组中
	long int i = 0, j = 0;
	for (long int k = left; k <= right; k++) {
		if ((j > len_2-1) || ((i <= len_1-1) && (L[i] <= R[j])))
			a[k] = L[i++];
		else {
			a[k] = R[j++];
			count += mid - (i+left) + 1;		//计算逆序对数
            //cout << "count plus"<< mid-(i+left)+1;
		}
	}
    /*
    for(int i=0;i<right-left+1;i++)
        cout <<a[i+left]<<' ';
    cout << "count="<<count;
    cout <<endl;
    */
	return count;
}

//通过归并排序计算逆序对
long int countInversions(long int a[], long int left, long int right,long int n)
{
	if (left < right) {
		long int mid = (left + right) / 2;
		//当前数组内的逆序对数等于两个子数组的逆序对数加上归并时计算出的逆序对数
		return countInversions(a, left, mid,n) 
			+ countInversions(a, mid + 1, right,n)
			+ mergeCountInversions(a, left, mid, right,n);
	}
	else
		return 0;
}


int main(){
    ios::sync_with_stdio(false);
    cin.tie(0), cout.tie(0);
    //关闭同步，以提高输入输出的速率（当数据很大的时候且使用cin cout，可以明显提速）
    long int n;
    cin >> n;
    long int a[n];
    long int b[n];
    for(long int i=0;i<n;i++){
        cin >> a[i];
    }
    for(long int i=0;i<n;i++){
        cin >> b[i];
    }
    Merge_sort(a,b,0,n-1);//此时a已经排序完成，b已经按照a的排序进行了换位（保证了一一对应）
    long int count=0;
    count=countInversions(b,0,n-1,n);
    cout<<count;
    return 0;
}

