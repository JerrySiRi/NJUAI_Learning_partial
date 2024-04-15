import java.util.ArrayList;

public class Hello
{
  public static void main(String args[])
  {
    System.out.println("hello world");
    Student stu= new Student();
    stu.speak("we are future");
    ArrayList<Integer> list_1 = new ArrayList<>();
    ArrayList<Integer> list_2 = new ArrayList<>();
    list_1.add(1);
    list_2.add(2);
    System.out.println(list_1.get(0));
    list_1.addAll(list_2);
    System.out.println(list_1);
  }
}
class Student
{
  public void speak(String s)
  {
    System.out.println(s);
  }
}
