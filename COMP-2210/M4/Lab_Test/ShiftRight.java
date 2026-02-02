package M4.Lab_Test;

import java.util.Arrays;

/**
 * Implements shift-right behavior in an array.
 *
 */

 public class ShiftRight {

    public static void main(String[] args) {
        int[] a = {1, 3, 5, 7, 9, -1, -1, -1, -1, -1};
        System.out.println(Arrays.toString(shiftRight(a, 0)));
    }
    /**
     * Shifts the elements at a[index] through a[a.length - 2] one
     * position to the right. 
     */
    public static int[] shiftRight(int[] array, int index) {
        for (int i = array.length - 1; i > index; i--){ 
            array[i] = array[i - 1]; 
        }
        array[index] = -1;


        return array;
    }

}

