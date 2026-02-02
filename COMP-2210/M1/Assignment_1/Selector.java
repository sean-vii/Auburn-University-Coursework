package Assignment_1;

import java.util.Arrays;
/**
* Defines a library of selection methods
* on arrays of ints.
*
* @author   Sean Bevensee (smb0207@auburn.edu)
* @author   Dean Hendrix (dh@auburn.edu)
* @version  January 28, 2023
*
*/
public final class Selector {

    /**
     * Can't instantiate this class.
     *
     * D O   N O T   C H A N G E   T H I S   C O N S T R U C T O R
     *
     */
    private Selector() { }


    /**
     * Selects the minimum value from the array a. This method
     * throws IllegalArgumentException if a is null or has zero
     * length. The array a is not changed by this method.
     */
    public static int min(int[] a) {
        if ((a == null) || a.length == 0){ 
            throw new IllegalArgumentException();
        }
        int min = Integer.MAX_VALUE; 
        for (int i : a){
            if (i < min) {
                min = i;
            }  
        }
        return min; 
    }


    /**
     * Selects the maximum value from the array a. This method
     * throws IllegalArgumentException if a is null or has zero
     * length. The array a is not changed by this method.
     */
    public static int max(int[] a) {
        if ((a == null) || a.length == 0){ 
            throw new IllegalArgumentException(); 
        }
        int max = Integer.MIN_VALUE; 
        for (int i : a) { 
            if (i > max) { 
                max = i; 
            }
        }
        return max;
    }


    /**
     * Selects the kth minimum value from the array a. This method
     * throws IllegalArgumentException if a is null, has zero length,
     * or if there is no kth minimum value. Note that there is no kth
     * minimum value if k < 1, k > a.length, or if k is larger than
     * the number of distinct values in the array. The array a is not
     * changed by this method.
     */
    public static int kmin(int[] a, int k) {
        // Common error check: 
        if ((a == null) || (a.length == 0) || (k < 1) || (k > a.length)){
            throw new IllegalArgumentException(); 
        }
        if (k == 1) { return a[0]; }
        
        // Define variables
        int[] cA = a.clone();  // < Copy to not change original 
        int index = 0;         // < allows for ignorance of distinct variables 
        int kmin = 0;          // < variable to store kmin 
        int temp = cA[0];      // < temporary # 

        // Check array for min 
        Arrays.sort(cA);
        System.out.println(Arrays.toString(cA));
        for (int i = 0; i < cA.length; i++){ 
            if (cA[i] != temp || i == 0) { // we're on distinct #...
                index++; 
                if (index == k) { kmin = cA[i]; }
            }  
            temp = cA[i];
        }

        // RETURN 
        if (k > index) { 
            throw new IllegalArgumentException();
        } else { 
            return kmin; 
        }
    }


    /**
     * Selects the kth maximum value from the array a. This method
     * throws IllegalArgumentException if a is null, has zero length,
     * or if there is no kth maximum value. Note that there is no kth
     * maximum value if k < 1, k > a.length, or if k is larger than
     * the number of distinct values in the array. The array a is not
     * changed by this method.
     */
    public static int kmax(int[] a, int k) {
        // Common error check: 
        if ((a == null) || (a.length == 0) || (k < 1) || (k > a.length)){
            throw new IllegalArgumentException(); 
        }
        if (k == 1) { return a[0]; }
        
        // Define variables
        int[] cA = a.clone();  // < Copy to not change original 
        int index = 0;         // < allows for ignorance of distinct variables 
        int kmax = 0;          // < variable to store kmax 
        int temp = cA[cA.length-1];     // < temporary # 

        // Check array for max 
        Arrays.sort(cA);
        for (int i = cA.length - 1; i >= 0; i--){ 
            if (cA[i] != temp || i == 0) { 
                index++; 
                if (index == k) { kmax = cA[i]; }
            }  
        }

        // RETURN 
        if (k > index) { 
            throw new IllegalArgumentException();
        } else { 
            return kmax; 
        }   
    }


    /**
     * Returns an array containing all the values in a in the
     * range [low..high]; that is, all the values that are greater
     * than or equal to low and less than or equal to high,
     * including duplicate values. The length of the returned array
     * is the same as the number of values in the range [low..high].
     * If there are no qualifying values, this method returns a
     * zero-length array. Note that low and high do not have
     * to be actual values in a. This method throws an
     * IllegalArgumentException if a is null or has zero length.
     * The array a is not changed by this method.
     */
    public static int[] range(int[] a, int low, int high) {
        // Common error check
        if ((a == null) || (a.length == 0)) {
            throw new IllegalArgumentException();
        }

        // Finds # in range 
        int nA_size = 0; 
        for (int i : a){ 
            if ((i >= low) && (i <= high)) { nA_size++; }
        }

        // Variables 
        int[] nA = new int[nA_size]; 
        int index = 0; 

        // Create new array 
        if (nA_size == 0) { 
            return nA; 
        } else { 
            for (int i = 0; i <= a.length - 1; i++){ 
                if (a[i] >= low && a[i] <= high) { nA[index] = a[i]; index++; }
            }
        }

        // RETURN 
        return nA;
    }


    /**
     * Returns the smallest value in a that is greater than or equal to
     * the given key. This method throws an IllegalArgumentException if
     * a is null or has zero length, or if there is no qualifying
     * value. Note that key does not have to be an actual value in a.
     * The array a is not changed by this method.
     */
    public static int ceiling(int[] a, int key) {
        // Common error check
        if ((a == null) || (a.length == 0)) {
            throw new IllegalArgumentException();
        }

        // Variables 
        int ceiling = Integer.MAX_VALUE; 

        // Find ceiling 
        for (int i = 0; i <= a.length - 1; i++) { 
            if (a[i] >= key && a[i] <= ceiling) { 
                ceiling = a[i];
            }
        } 

        // RETURN 
        if (ceiling == Integer.MAX_VALUE) { 
            throw new IllegalArgumentException(); 
        } else { 
            return ceiling;
        }
    }


    /**
     * Returns the largest value in a that is less than or equal to
     * the given key. This method throws an IllegalArgumentException if
     * a is null or has zero length, or if there is no qualifying
     * value. Note that key does not have to be an actual value in a.
     * The array a is not changed by this method.
     */
    public static int floor(int[] a, int key) {
        // Common error check
        if ((a == null) || (a.length == 0)) {
            throw new IllegalArgumentException();
        }

        // Variables 
        int floor = Integer.MIN_VALUE; 

        // Find floor 
        for (int i = 0; i <= a.length - 1; i++) { 
            if (a[i] <= key && a[i] >= floor) { 
                floor = a[i];
            }
        } 

        // RETURN 
        if (floor == Integer.MIN_VALUE) { 
            throw new IllegalArgumentException(); 
        } else { 
            return floor;
        }
    }

}
