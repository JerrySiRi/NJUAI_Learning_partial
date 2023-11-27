
public class Hello
{
  public static void main(String args[])
  {
    System.out.println("hello world");
    Student stu= new Student();
    stu.speak("we are future");
  }
}
class Student
{
  public void speak(String s)
  {
    System.out.println(s);
  }
}
