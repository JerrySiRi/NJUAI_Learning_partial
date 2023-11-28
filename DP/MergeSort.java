
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.time.Duration;
import java.time.LocalTime;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

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
        return merge(new_1, new_2);
    }

    public static int[] merge(int[] new_1, int[] new_2){
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
    
}
