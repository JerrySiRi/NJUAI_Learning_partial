/*
 * file 1: quick_sort 串行 、 并行
 * 读取乱序数据文件random.txt，排序完成后输出排序文件order*.txt。
 * （需提交六份order*.txt，命名为order1.txt，order2.txt…以此类推）
 */

public static void main(String[] args){
    //   int[] array = {91,92,95,89,88,90};
       int[] array = {6,4,5,-1,0,100};
       print(array,"原始数组");
    //   sort(array,0,array.length-1);
       QuickSort(array,0,array.length-1);
       print(array,"结果");
   }
   public static void quick_sort(int[] array,int left,int right){
        if (left>=right){
            return;
        }
        // 先求出基准数的下标
       int index = sort(array,left,right);
        // 对基准数左边递归
        QuickSort(array,left,index);
        // 对基准数右边递归
        QuickSort(array,index+1,right);
   }
   /**
    * left，左边界.
    * right,右边界.范围array.length-1
    */
   public static int sort(int[] array,int start,int end){
       // 找出一个基准数,使得左边的数<=基准数,基准数>=右边的数,返回此基准数下标
       // 假设第一个数就是基准数
       int s = start;
       while (start<end){
           // 从右边开始找到小于等于基准数的
           while (start<end && array[end]>array[s]){
               end--;
               System.out.println("end = "+end);
           }
           // 从左边开始找到大于基准数的
           while (start<end && array[s]>=array[start]){
               start++;
               System.out.println("start = "+start);
           }
           // end>start 说明小于等于基准数还在右边,大于基准数的在左边,两两交换即可
           if (end>start) {
                   swap(array, start, end);
           }
       }
       swap(array,s,start);
       return start;
   }
