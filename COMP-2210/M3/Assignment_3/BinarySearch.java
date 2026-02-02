package M3.Assignment_3;

import java.util.Arrays;
import java.util.Comparator;

/**
 * Binary search.
 */
public class BinarySearch {

    /**
     * Returns the index of the first key in a[] that equals the search key, 
     * or -1 if no such key exists. This method throws a NullPointerException
     * if any parameter is null.
     */
    public static <Key> int firstIndexOf(Key[] a, Key key, Comparator<Key> comparator) {
        if (a == null || key == null || comparator == null) { throw new NullPointerException(); }

        int low = 0, high = a.length - 1; 
        int temp = Integer.MIN_VALUE;

        Arrays.sort(a);
        while (low <= high) { 
            int mid = (low + high) / 2;
            int comp = comparator.compare(a[mid], key); 

            if (comp > 0) { 
                high = mid - 1;
            }  else if (comp < 0) { 
                low = mid + 1; 
            } else { 
                temp = mid; 
                high = mid - 1; 
            }
        }
        return temp; 
    }

    /**
     * Returns the index of the last key in a[] that equals the search key, 
     * or -1 if no such key exists. This method throws a NullPointerException
     * if any parameter is null.
     */
    public static <Key> int lastIndexOf(Key[] a, Key key, Comparator<Key> comparator) {
        if (a == null || key == null || comparator == null) { throw new NullPointerException(); }

        int low = 0, high = a.length - 1; 
        int temp = Integer.MIN_VALUE;

        Arrays.sort(a);
        while (low <= high) { 
            int mid = (low + high) / 2;
            int comp = comparator.compare(a[mid], key); 

            if (comp > 0) { 
                high = mid - 1;
            }  else if (comp < 0) { 
                low = mid + 1; 
            } else { 
                temp = mid; 
                low = mid + 1; 
            }
        }
        return temp; 
    }

}
