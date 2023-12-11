
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.time.Duration;
import java.time.LocalTime;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.util.Arrays;

import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;

/*
 * 排序前的时间：15:50:35.184368600
排序后的时间：15:50:35.193369900
时间差(毫秒)：9
文件写入成功
 */



public class MergeSort {
    public static void main(String args[]){
        //int[] arr = {3,1,6,4,5,2,8,7};
        int[] arr = {3,1,4,5};
        //int arr[] = new int[30000];
        int par_or_seq = 1;//【指示是否是并行】0：非并行，是串行。1：并行
        /*try{
            int data[] = new int[30000];
            FileInputStream fileInputStream = new FileInputStream("random.txt");
            InputStreamReader inputStreamReader = new InputStreamReader(fileInputStream);
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
            String line;
            int index = 0;
            while ((line = bufferedReader.readLine()) != null) {
                String[] words = line.split(" ");
                for (String word : words) {
                    data[index]= Integer.parseInt(word);
                    index++;
                }
            }
            bufferedReader.close();
            arr = data;
        }
        catch (IOException e){
            System.out.println("读取错误，请检查是否有random.txt在相同目录下");
        }
         * 
         */
        
        
        LocalTime before=LocalTime.now();  // 排序前时间
		System.out.println("排序前的时间：" + before); 
        
        int result[] = new int[arr.length];

        result = merge_sort(arr,0,arr.length-1,par_or_seq);

        LocalTime after=LocalTime.now();   // 排序后时间
		Duration duration=Duration.between(before, after);
		System.out.println("排序后的时间：" + after);
		System.out.println("时间差(毫秒)：" + duration.toMillis());
        try {
            File file=new File("order5.txt");
            if(par_or_seq == 1)
                file=new File("order6.txt");
            if(!file.exists()) {
                file.createNewFile();
            }
            //创建文件输出流
            FileOutputStream fout=new FileOutputStream(file);
            for(int a:result){
                fout.write(String.valueOf(a).getBytes());
                fout.write(String.valueOf(" ").getBytes());//输出空格
            }
            System.out.println("文件写入成功");
            fout.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }



    public static int[] merge_sort(int[] arr,int L, int R,int whe){
        if(R==L){
            int result[] = {arr[L]};
            
            return result;
        }
            
        int new_1[] = new int[(int)(Math.floor((R+L)/2))-L+1];
        int new_2[] = new int[R-(int)(Math.floor((R+L)/2))];

        new_1 = merge_sort(arr, L, (int)(Math.floor((R+L)/2)), whe);
        //System.out.println(new_1[0]);
        new_2 = merge_sort(arr, (int)(Math.floor((R+L)/2))+1, R, whe);
        //System.out.println(new_2[0]);
        if(whe==0)//串行
            return merge(new_1, new_2);

        int temp[] = merge_par(new_1,new_2);
        System.out.println("main函数中拿到的temp:" + Arrays.toString(temp));
        return temp;//并行
    }

    public static int[] merge(int[] new_1, int[] new_2){
        //【串行】
        int index_1 = 0; 
        int index_2 = 0;
        int res[] = new int[new_1.length + new_2.length];
        for(int index=0; index < new_1.length + new_2.length; index++){
            if(index_1 == new_1.length){//【BUG】必须加超了才能停止，否则下标越界（两个数组各一个元素情况）
                res[index] = new_2[index_2];
                index_2++;
            }
            else if(index_2 == new_2.length){
                res[index] = new_1[index_1];
                index_1++;
            }
            else{
                if(new_1[index_1]<=new_2[index_2]){
                    res[index] = new_1[index_1];
                    index_1++;
                }
                else{
                    res[index] = new_2[index_2];
                    index_2++;
                }
            }   
        }
            return res;
    }

    public static int[] merge_par(int[] A, int[] B){
        int ans[] = new int[A.length+B.length]; //merge的结果
        int n = A.length;
        int m = B.length;
        int k_m;
        if(m==1)
            k_m = 1;
        else
            k_m = (int)(m/Math.log(m));
        int index_A[] = new int[k_m+1];//下标从0-k_m,指示数组A划分区间【k_m段，含开始结束，共k_m+1个位置】
        index_A[0]=0;index_A[k_m]=n;//指示A：数组最终划分区间
        //【最后一个位置只会用在串行merge中，而merge前需要切片，末尾不含】
        int temp=0;//【记录上次A遍历的位置，不用从头开始！！】

        for(int i=1;i<k_m;i++){//【简化：串行来做，O(n)一定做完】【也可以用并行】

            //step1: 求B主元在A中的位置
            int pivot = B[i*(int)(Math.log(m))];
            int sum=0;//A中小于等于B的个数
            for(;temp<n;temp++){
                if(A[temp]<=pivot)
                    sum++;
                else
                    break;
            }

            //step2：把A的划分位置确定下来
            index_A[i] = sum;
        }
        

        // 多线程，每个线程从哪里开始对ans数组进行赋值
        int ans_start_index[] = new int[k_m];
        ans_start_index[0] = 0;
        if(k_m>1)
            ans_start_index[1] = 0 + (int)(Math.log(m))+1+ index_A[1]-index_A[0];
        for(int j = 2;j<k_m; j++)
            ans_start_index[j] = ans_start_index[j-1] + (int)(Math.log(m)) + index_A[j]-index_A[j-1];


        CyclicBarrier barrier = new CyclicBarrier(k_m);//【必须k_m个线程都到达才能做！】
        System.out.println("当前划分段数k_m"+k_m);
        for(int process=0; process<k_m; process++){//每一个process对应一个A和B的划分区间，分别串行来merge
            
            int start_A = index_A[process];
            int end_A = index_A[process+1];//以下copy的时候取不到！
            //if(start_A == end_A)
                //end_A++;
            int start_B = process * (int)(Math.log(m));
            int end_B;//以下copy的时候取不到！
            if(process!=k_m-1)
                end_B = (process+1) * (int)(Math.log(m))+1;
            else
                end_B = m;
            int[] A_partial = Arrays.copyOfRange(A, start_A, end_A); // 进行数组切片操作
            int[] B_partial = Arrays.copyOfRange(B, start_B, end_B); // 进行数组切片操作
            
            
            ES2 new_thread = new ES2(barrier,A_partial, B_partial, ans, ans_start_index[process] );//多线程不能确保每个线程在什么时候完成。线程结束后返回数组最终再排序并不现实
            //TODO：可以每个线程直接在“原数组result”上进行修改
            new_thread.start();

        }
        System.out.println("merge_par:ans"+Arrays.toString(ans));
        return ans;

    }
}


//每个线程串行对划分出来的小数组进行merge
//BUG！！！vscode会把一个项目（目录）下的java文件编译到一起！如果和其他文件中的类重名就会报错！！！
class ES2 extends Thread{ //在result数组上直接进行修改，从start_index位置开始
    int ans[];
    int A[],B[];
    int start;
    private CyclicBarrier barrier;
    public ES2(CyclicBarrier barrier,int[] A, int[] B, int[] ans, int start_index){
        this.A = A;
        //this.arr = new int[arr.length];
        this.B = B;
        this.ans = ans;
        this.start = start_index;
        this.barrier = barrier;
    }

    public void run(){
        System.out.println("线程" + Thread.currentThread().getName() + "正在写入数据...");
        int temp[] = new int[A.length+B.length];
        temp = MergeSort.merge(A, B);
        for(int i=0; i<A.length+B.length ;i++){//从temp的下标来访问
            ans[start+i] = temp[i];
            System.out.println( Thread.currentThread().getName() + "temp结果为"+ temp[i]);
        }
        System.out.println("线程" + Thread.currentThread().getName() + "写入数据完毕，等待其他线程写入完毕...");
        try {//等待其他线程完成对result的赋值！
            barrier.await();
        } catch (InterruptedException | BrokenBarrierException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        System.out.println("所有线程写入完毕，继续处理其他任务...");
        System.out.println("ans:"+Arrays.toString(ans));
    }

}

/*
     * public static ArrayList<Integer> merge_par(ArrayList<Integer> list_1, ArrayList<Integer> list_2,int whe){
        //【并行】通过划分+递归使大merge，变成小merge
        //以下采用方根划分技术，merge的两数组长度最多差1
        if(list_1.size()==0)//【merge完成，传入的new_1没有元素了！】
            return list_2;
                    //ArrayList<String> arrayList = new ArrayList<>(Arrays.asList(array));
                    //有BUG

        int seg_1 = (int)Math.ceil(Math.sqrt(list_1.size()));//划分长度
        int seg_2 = (int)Math.ceil(Math.sqrt(list_2.size()));

        int pivot_1[] = new int[seg_1];//A主元所在下标,一共seg_1个，最后一个是数组最后
        for(int i=0;i<seg_1-1;i++)
            pivot_1[i]=(i+1)*seg_1;
        pivot_1[seg_1-1] = list_1.size()-1;
        int pivot_2[] = new int[seg_2];//B主元所在下标，一共seg_2个，最后一个是数组最后
        for(int i=0;i<seg_2-1;i++)
            pivot_2[i]=(i+1)*seg_2;
        pivot_2[seg_2-1] = list_2.size()-1;

        for(int i=0; i<seg_1; i++){//【可以并行来做，一个处理器负责一段】
            int pivot = list_1.get(pivot_1[i]);
            int r_index=list_2.size()-1;//B中目标数据段的右侧索引.如果下面的if不满足，则A中所有的主元比B的主元要大！
            
            int index_last = 0;
            if(i!=0)
                index_last = pivot_1[i-1]; 
            int index_now=pivot_1[i];

            for(int j=0; i<seg_2-1; j++){
                if(list_2.get(pivot_2[j])<=pivot && list_2.get(pivot_2[j+1])>=pivot){
                    r_index = pivot_2[j+1];
                    break;
                }    
            }

            //此时A的范围是index_last---index_now
            //此时A主元插入B的范围是l_index---r_index
            // 简化版，在B的范围是0---r_index中插入。如果按照书上写，就会出现以下BUG
            //【BUG】如果A是：1,3,8,8,8,8,15,16 、、B是：2,4,5,6,7,10,12,14,17。A的两个主元都是8，划分到B的一段中
            r_index = list_2.size()-1; //test:对完整的B来merge
            ArrayList<Integer> par_A = new ArrayList<Integer>();
            ArrayList<Integer> par_B = new ArrayList<Integer>();
            for(int cur=index_last; cur<=index_now; cur++)
                par_A.add(list_1.get(cur));
            for(int cur_b=0; cur_b< r_index;cur_b++ )
                par_B.add(list_2.get(cur_b));
            
            //以下：对par_A和par_B来merge。结果返回merge好的，更新作为新的list_2以供下次for循环使用 
        }   
    }
     * 
     */
    
        
    

