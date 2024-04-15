#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // 你的代码
    }
};


int main(){




}
/*
【推荐写法--定义私有的全局变量+只在函数中定义局部变量】

class Solution {
private:
    // 类内
    unordered_map<int, int> visited;
public:
    vector<int> twoSum(vector<int>& nums, int target) {//----传入的时候都要用&地址传入的，直接操作传入的数组信息
        // 函数内
        // unordered_map<int, int> visited;
        for (int i = 0; i < nums.size(); ++i) {
            if (visited.count(target - nums[i])) {
                return {visited[target - nums[i]], i};
            }
            visited[nums[i]] = i;
        }
        return {};
    }
};

*/
/*
【实际中的评测过程】

unordered_map<int, int> visited;
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // 你的代码
    }
};

int main() {
    string line;
    while (getline(cin, line)) {
        // 读取输入的 nums
        vector<int> nums = stringToIntegerVector(line);
        // 读取输入的 target
        getline(cin, line);
        int target = stringToInteger(line);
        
        // 每次实例化一个 Solution()，并执行其 twoSum 方法
        vector<int> ret = Solution().twoSum(nums, target);
		
        // 输出结果
        string out = integerVectorToString(ret);
        cout << out << endl;
    }
    return 0;
}

*/