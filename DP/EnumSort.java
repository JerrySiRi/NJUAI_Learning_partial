
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.time.Duration;
import java.time.LocalTime;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

/*
 * 排序前的时间：15:15:36.462404500
排序后的时间：15:15:38.229392800
时间差(毫秒)：1756
文件写入成功
 * 
 */
public class EnumSort {
    public static void main(String args[]){
        int arr[] = new int[30000];
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
        result = enum_sort(arr);
        LocalTime after=LocalTime.now();   // 排序后时间
		Duration duration=Duration.between(before, after);
		System.out.println("排序后的时间：" + after);
		System.out.println("时间差(毫秒)：" + duration.toMillis());
        //for(int a : arr){
            //System.out.println(a);
        //}
        
        try {
            File file=new File("order3.txt");
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

    public static int[] enum_sort(int[] arr){
        int result[] = new int[(int)arr.length];
        for(int target : arr){
            int sum = 0;
            for(int item : arr){
                if(item < target)
                    sum++; 
            }
            result[sum] = target;    
        }
        return result;
    }
    
}
