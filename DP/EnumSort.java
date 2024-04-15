
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.time.Duration;
import java.time.LocalTime;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;
import java.util.Arrays;

/*【串行】
 * 排序前的时间：15:15:36.462404500
排序后的时间：15:15:38.229392800
时间差(毫秒)：1756
文件写入成功
 * 
 */

 /*【并行】
  * 排序前的时间：17:38:27.250112300
排序后的时间：17:38:29.610645
时间差(毫秒)：2360
文件写入成功

枚举排序EnumSort-并行算法
排序前的时间：10:46:58.248254200
排序后的时间：10:47:14.467948900
时间差(毫秒)：16219
文件写入成功
  */
public class EnumSort {
    public static void main(String args[]){
        int arr[] = new int[30000];
        int par_or_seq = 1;//标志是否要并行执行，如果值是0，非并行-串行。值是1，并行
        if(par_or_seq == 0)
            System.out.println("枚举排序EnumSort-串行算法");
        else
            System.out.println("枚举排序EnumSort-并行算法");
        try{
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
        

        int[] correct = Arrays.copyOfRange(arr,0,arr.length); 
        Arrays.sort(correct);
        //正确的、已排序好的数组
        LocalTime before=LocalTime.now();  // 排序前时间
		System.out.println("排序前的时间：" + before); 
        
        int result[] = new int[arr.length];
        result = enum_sort(arr,par_or_seq);
        LocalTime after=LocalTime.now();   // 排序后时间
		Duration duration=Duration.between(before, after);
		System.out.println("排序后的时间：" + after);
		System.out.println("时间差(毫秒)：" + duration.toMillis());
        //for(int a : arr){
            //System.out.println(a);
        //}
        
        try {
            File file = new File("order3.txt");
            if(par_or_seq==1)
                file=new File("order4.txt");
            
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
        //【检查排序是否正确】
        boolean sen = true;
        for(int index_t=0; index_t<result.length; index_t++){
            if(result[index_t]!=correct[index_t]){
                sen = false;
                System.out.println("result" + result[index_t]);
                System.out.println("correct" + correct[index_t]);
                break;
            }
        }
        if(sen==true)
            System.out.println("使用java排序库函数验证：排序正确");
        else
            System.out.println("使用java排序库函数验证：排序错误");

    }

    public static int[] enum_sort(int[] arr,int whe){
        int result[] = new int[(int)arr.length];
        CyclicBarrier barrier = new CyclicBarrier(arr.length+1);//【必须k_m个线程都到达才能做！】
        for(int target : arr){//【可以并行化设计，一个进程对应一个元素小于它个数的计算】
            if(whe == 0){//【串行】
                int sum = 0;
                for(int item : arr){
                    if(item < target)
                        sum++; 
                }
                result[sum] = target; 
            }
            else if(whe == 1){//【并行】
                ES new_thread;
                new_thread = new ES(arr,result,target,barrier);
                new_thread.start();
            }
        }
        if(whe == 1){
            try {
                barrier.await();
            } catch (InterruptedException | BrokenBarrierException e) {
                //TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
        
        return result;
    }
    
}

class ES extends Thread{
    int target;
    int arr[],result[];
    CyclicBarrier barrier;
    ES(int[] arr,int[] result, int target, CyclicBarrier barrier){
        this.target = target;
        //this.arr = new int[arr.length];
        this.arr = arr;
        this.result = result;
        this.barrier = barrier;
    }

    public void run(){
        int sum = 0;
        for(int item:arr){
            if(item < target)
                sum++;
        }
        result[sum] = target;
        try {
            barrier.await();
        } catch (InterruptedException | BrokenBarrierException e) {
            //TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

}
