#include<bits/stdc++.h>
using namespace std;

string s="ABCDEFGHIJKLMNOPQRSTUVWXYZabcd";
string func[]={
"lg(lg^* n)","2^{lg^* n}", "(\\sqrt{3})^{lg n}", "n^2", "n!", "(lg n)!",
"(9/8)^n","n^3","lg^2 n", "lg (n!)", "2^{2^n}","n^{1/lg n}",
"ln ln n", "lg^* n","n 2^n","n^{lg lg n}","ln n","1",
"2^lg n","(lg n)^{lg n}","e^n","4^{lg n}","(n+1)!","\\sqrt{lg lg n}",
"lg^*(lg n)","2^{\\sqrt{2 lg n}}","n","2^n","n lg n","2^{2^{n+1}}"};

string ans="L=R<A<N=Y<B<X<M<Q<I<Z<C<a=S<c<J<D=V<H<F<P<T<G<b<O<U<E<W<K<d"; // update your answer here!

/* DO NOT CHANGE THE FOLLOWING CODE SEGMENT!!! */
int main(){
    auto check_valid=[&](){
        vector<int> cnt(30);
        auto to_idx=[&](char c){
            if (c>='A'&&c<='Z') return c-'A';
            if (c>='a'&&c<='d') return c-'a'+26;
            cout<<"Invalid answer! Expected [A-Z] or [a-d], found "<<c<<endl;
            return 0;
        };
        bool now=0;
        for (auto c:ans){
            if (now){
                if (c!='='&&c!='<') {cout<<"Invalid answer! Expected < or =, found "<<c<<endl; return 0;}
            }
            else{
                cnt[to_idx(c)]++;
                if (cnt[to_idx(c)]>1) {cout<<"Invalid answer! "<<c<<" appears more than once"<<endl; return 0;} 
            }
            now^=1;
        }
        for (int i=0;i<30;++i){
            if (!cnt[i]) {cout<<"Invalid answer! "<<s[i]<<" does not appear in your answer."<<endl; return 0;}
        } 
        if (ans.size()!=59){cout<<"Invalid anwer! The length of your answer is not 59."<<endl; return 0;}
        cerr<<"The following is a preview of your answer:"<<endl;
        int ccnt=0;
        for (auto c:ans){
            if (c=='='||c=='<') {cerr<<"  "<<c<<"  "; continue;}
            else {ccnt++; cerr<<func[to_idx(c)];
            if (ccnt%6==0) cerr<<endl;}
        }
        cerr<<endl;
        return 1;
    };
    if (check_valid()) cout<<ans<<endl;
    return 0;
}