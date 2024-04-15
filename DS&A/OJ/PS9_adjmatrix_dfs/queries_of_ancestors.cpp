#include <bits/stdc++.h>
#include <iostream>
#include <vector>
#include <cmath>
#include <cassert>
using namespace std;

pair<vector<int>,vector<pair<int,int>>> gen(int n, int q,int seed, int parameter){
    vector<int> res(n,-1);
    vector<pair<int,int>> queries(q);
    mt19937 rng(seed);
    for (int i=1;i<n;++i){
        int w=i-1;
        for (int j=0;j<parameter;++j){
            w=rng()%(w+1);
        }
        res[i]=i-1-w;       
    }
    for (int i=0;i<q;++i){
        queries[i].first=rng()%n;
        queries[i].second=rng()%n; 
    }
    return {res,queries};
}

enum Color{WHITE,GRAY,BLACK};


typedef struct {
      vector<int> children;//用来存放子节点的【邻接矩阵的一部分】
      Color node_co=WHITE;
      long long int start=0;
      long long int end=0;
 }TreeNode ;

static long long int dfs_time=0;//【全局变量dfs_time】【BUG！如果定义成time会造成和库函数同名？命名的时候要注意！！！】


void DFS_VISIT(vector<TreeNode>& adj_li,int cur,int n){//【当前节点是i】
    dfs_time++;
    adj_li[cur].start=dfs_time;
    adj_li[cur].node_co=GRAY;
    //vector<int> kids(adj_li[cur].children);//用向量adj_li[i].chilren给新的向量cur_chi赋值，两者完全一样
    for(long unsigned int i=0; i < adj_li[cur].children.size() ;i++){//每一个子节点的编号就是kids[i]啦！！！
        if(adj_li[adj_li[cur].children[i]].node_co==WHITE)
            DFS_VISIT(adj_li,adj_li[cur].children[i],n);
    }
    adj_li[cur].node_co=BLACK;
    dfs_time++;
    adj_li[cur].end=dfs_time;
}

void DFS(vector<TreeNode>& adj_li,int n){//临接矩阵以引用的方式使用，最后DFS什么都不返回
    for(int cur=0;cur<n;cur++){//【对所有节点】
        if(adj_li[cur].node_co==WHITE)
            DFS_VISIT(adj_li,cur,n);
    }
}


signed main(){
    ios::sync_with_stdio(false);
    cin.tie(0), cout.tie(0);
    int n,q,seed,parameter;
    cin>>n>>q>>seed>>parameter;
    auto ret=gen(n,q,seed,parameter);
    //vector<int> fu=ret.first;//【包含一系列父节点的信息】
    //vector<pair<int,int>> queries=ret.second;//【包含所有需要询问的信息】
    vector<TreeNode> adj_li(n);//【即将创建的邻接矩阵】
    for(int i=1;i<n;i++){
        int temp=ret.first[i];//i节点的父亲节点是temp
        //adj_li[i].parent=temp;//i节点的父亲节点是temp
        adj_li[temp].children.push_back(i);//父亲节点有一个子节点i.从1开始没有问题，根节点不会成为任何节点的子节点的
    }

    DFS(adj_li,n);
    //此时拿到的是更改之后的adj_li啦
    long long int sum=0;
    long long int temp=1;
    for(int i=0;i<q;i++){//对每一个询问进行考察
        int qian=ret.second[i].first;
        int hou=ret.second[i].second;
        //此时qian是hou的祖先
            //此时i可能会很大，最大会到达2^(2^18)
            //998244353大约是2的30次方不到
            //【BUG！】29、30一次都是正确的，31一次就不对了。可能的原因是yu*temp在乘的时候溢出了！！！
            //（还没到%998244353的时候就已经溢出了呢）
        temp*=2;
        temp%=998244353;
        //【【【【【【【【好方法！每次都暂存一个变量，不管用不用先给他算出来】】】】】】】】
        //这样用的时候直接加一下就可以了，不用每一次要用的时候重新计算！！！！！！！！
        if(i==0)
            temp>>=1;
        if(adj_li[qian].start <= adj_li[hou].start && adj_li[hou].end <= adj_li[qian].end ){
            //此时qian是hou的祖先
            //此时i可能会很大，最大会到达2^(2^18)
            //998244353大约是2的30次方不到
            //【BUG！】29、30一次都是正确的，31一次就不对了。可能的原因是yu*temp在乘的时候溢出了！！！
            //（还没到%998244353的时候就已经溢出了呢）
            sum+=temp;

        }
        
    }
    cout << (sum % 998244353);


}
/*
    //此时拿到的是更改之后的adj_li啦
    long long int sum=0;
    //long int temp=0;
    long long int yu=(1<<30)%998244353;//75497471
    for(int i=0;i<q;i++){//对每一个询问进行考察
        int qian=ret.second[i].first;
        int hou=ret.second[i].second;
        long long int temp=1;
        int shun=i;
        if(adj_li[qian].start <= adj_li[hou].start && adj_li[hou].end <= adj_li[qian].end ){
            //此时qian是hou的祖先
            //此时i可能会很大，最大会到达2^(2^18)
            //998244353大约是2的30次方不到
            //【BUG！】29、30一次都是正确的，31一次就不对了。可能的原因是yu*temp在乘的时候溢出了！！！
            //（还没到%998244353的时候就已经溢出了呢）
            
            while(shun>30){
                temp*=yu;
                temp%=998244353;
                shun-=30;
            }
            temp*=(1<<shun);
            temp%=998244353;
            sum+=temp;
            sum%=998244353;
        }
        
    }
    cout << (sum % 998244353);

*/