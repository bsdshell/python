public class Hello
{
    public static void main(String[] args)
    {
        System.out.println("Hello World!");
        int[][] array2d = new int[3][2];
        for(int i=0; i<3; i++)
            array2d[i] = fun();

        for(int i=0; i<3; i++)
        {
            for(int j=0; j<2; j++)
                System.out.print("["+array2d[i][j]+"]");
            System.out.println();
        }
                
    }
    public static int[] fun()
    {
        int[] array = {1, 2};
        return array;
    }
}
