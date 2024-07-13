#include <iostream>
#include <cstring>
#include <iomanip>
using namespace std;
int main(){
	int n,i,j;
	int a[100];
	cin>>n;
	for(i=0;i<n;i++){
		cin>>a[i];
	}
	for(i=0;i<n-1;i++){
		for(j=i+1;j<n;j++){
			if(a[i]==a[j]){
				for(int k=j;k<n-1;k++){
					a[k]=a[k+1];
				}
				j=j-1;
				n=n-1;
			}
		}
		for(int g=0;g<n;g++)
			cout << a[g]<<" ";
			cout <<endl;
	}
	for(i=0;i<n;i++){
		cout<<a[i]<<" ";
	}
	return 0;
}

