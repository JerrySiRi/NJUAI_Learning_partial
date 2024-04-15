#include<iostream>
using namespace std;

int main(){
    long int len_1=4;
    long int len_2=3;
    long int L[len_1]={1,2,4,6},R[len_2]={3,5,7};
    long int a[7];
    long int i=0,j=0;
    long int count=0;
    for(long int k=0;k<=5;k++){
        if(i==len_1){
            a[k]=R[j];
            j++;
            continue;
        }
        if(j==len_2){
            a[k]=L[i];
            i++;
            continue;
        }
        if(L[i]<=R[j]){
            a[k]=L[i];
            i++;
        }
        else{
            a[k]=R[j];
            count+=3-i+1;
            j++;
        }
    }
    cout <<count;


}