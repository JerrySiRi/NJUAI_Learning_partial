
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.time.Duration;
import java.time.LocalTime;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.Collectors;

/*
 * 排序前的时间：15:50:35.184368600
排序后的时间：15:50:35.193369900
时间差(毫秒)：9
文件写入成功
 */

public class MergeSort {
    public static void main(String args[]){
        int arr[] = new int[30000];
        int par_or_seq = 0;//【指示是否是并行】0：非并行，是串行。1：并行
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
        new_2 = merge_sort(arr, (int)(Math.floor((R+L)/2))+1, R, whe);
        if(whe==0)//串行
            return merge(new_1, new_2);
        return merge_par(new_1,new_2);//并行
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
        int n = A.length;
        int m = B.length;
        int k_m = (int)(m/Math.log(m));
        int index[] = new int[k_m+1];//下标从0-k_m
        index[0]=0;index[k_m]=n-1;//指示A：数组最终划分区间
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
            index[i] = sum;
        }




        return new int[];



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
    
        
    

