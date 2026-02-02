package Testing;
import static org.junit.Assert.assertEquals;
import org.junit.Test;

/**
 * LinearSearch1Test.java
 * Illustrates JUnit tests for the LinearSearch1 class.
 */
public class MinOfThreeTest {

    /** Test case for the search method. */
    @Test
    public void testSearch1() {
        int[] a = {2, 2, 3};
        int expected = 2;
        int actual = MinOfThree.min1(a[0], a[1], a[2]);
        assertEquals(expected, actual);
    }

    @Test
    public void testSearch2() {
        int[] a = {5, 5, 5};
        int expected = 5;
        int actual = MinOfThree.min2(a[0], a[1], a[2]);
        assertEquals(expected, actual);
    }
}