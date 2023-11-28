import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.time.Duration;
import java.time.LocalTime;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

/*
 * 排序前的时间：15:15:21.843083800
排序后的时间：15:15:21.851086100
时间差(毫秒)：8
文件写入成功
 * 
 */
public class QuickSort{
    public static void main(String[] args){
        //int[] arr = {3,1,6,4,5,2,8,7};
        int arr[] = new int[30000];
        try{
            /*
             * FileInputStream in = new FileInputStream("random.txt");
            byte data[] = new byte[30000];
            int item;
            while((item = in.read(data,0,30000))!=-1){
                System.out.println("文件读取成功，读取数据个数"+item);
            }
             * 
             */
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

        quickSort(arr,0,arr.length-1);

        LocalTime after=LocalTime.now();   // 排序后时间
		Duration duration=Duration.between(before, after);
		System.out.println("排序后的时间：" + after);
		System.out.println("时间差(毫秒)：" + duration.toMillis());
        
        try {
            File file=new File("order1.txt");
            if(!file.exists()) {
                file.createNewFile();
            }
            //创建文件输出流
            FileOutputStream fout=new FileOutputStream(file);
            // for(int a:arr){
                //fout.write(a);//【BUG】不通过string的转换得到的是乱码！
            //}
            for(int a:arr){
                fout.write(String.valueOf(a).getBytes());
                fout.write(String.valueOf(" ").getBytes());//输出空格
                //fout.write(System.lineSeparator().getBytes());//输出换行符
            }
            System.out.println("文件写入成功");
            fout.close();

        } catch (IOException e) {
            System.out.println(e.getMessage());
        }

    }

    public static void quickSort(int[] arr,int Left,int Right){
          if(Left < Right){
            // 随机生成一个数作为基准值
            // 为了不用传pivot，一直以最右元素作为pivot，调换一个位置即可
            swap(arr, Left + (int)(Math.random()*(Right - Left + 1)), Right);
            // patitition返回：小于pivot的数组最高位置，大于pivot的数组最小位置
            int[] p = partition(arr, Left, Right);
            quickSort(arr, Left, p[0]-1);
            quickSort(arr, p[1]+1, Right);
          }
    }

    public static int[] partition(int[] arr, int L,int R ) {
       int less = L; //小于pivot的新数组右边界,本次可以直接交换的位置
       int more = R; //大于pivot的新数组左边界
        // L: 本次要和pivot大小比较的元素
       while(L < more){
        if(arr[L] < arr[R])
            swap(arr, less++, L++); 
            // L+1，因为L左侧都认为是比pivot小，且L和less位置直接交换，less位置已经判断过比pivot小！
        else if(arr[L] > arr[R])
            swap(arr, --more, L); // 【BUG！每次必须先-1，保证pivot位置不动！】
            // L不能+1，不知道交换完的元素和pivot的大小关系！
        else// 如果遍历到的数与基准值arr[R]相等就跳过 
            L++;
    }
    // pivot与大于pivot数组的第一个数进行交换，无所谓和哪个数字交换，pivot值位置正确即可！
    swap(arr,more,R);
    int result[] = {less,more};
    return result;
} 


    // 在数组中直接交换下标i和j的元素
    public static void swap(int[] arr,int i,int j){
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}