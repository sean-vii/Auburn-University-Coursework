package M4.Assignment_4;

import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * Provides an implementation of the Set interface.
 * A doubly-linked list is used as the underlying data structure.
 * Although not required by the interface, this linked list is
 * maintained in ascending natural order. In those methods that
 * take a LinkedSet as a parameter, this order is used to increase
 * efficiency.
 *
 * @author Dean Hendrix (dh@auburn.edu)
 * @author YOUR NAME (you@auburn.edu)
 *
 */
public class LinkedSet<T extends Comparable<T>> implements Set<T> {

    //////////////////////////////////////////////////////////
    // Do not change the following three fields in any way. //
    //////////////////////////////////////////////////////////

    /** References to the first and last node of the list. */
    Node front;
    Node rear;

    /** The number of nodes in the list. */
    int size;

    /////////////////////////////////////////////////////////
    // Do not change the following constructor in any way. //
    /////////////////////////////////////////////////////////

    /**
     * Instantiates an empty LinkedSet.
     */
    public LinkedSet() {
        front = null;
        rear = null;
        size = 0;
    }


    //////////////////////////////////////////////////
    // Public interface and class-specific methods. //
    //////////////////////////////////////////////////

    ///////////////////////////////////////
    // DO NOT CHANGE THE TOSTRING METHOD //
    ///////////////////////////////////////
    /**
     * Return a string representation of this LinkedSet.
     *
     * @return a string representation of this LinkedSet
     */
    @Override
    public String toString() {
        if (isEmpty()) {
            return "[]";
        }
        StringBuilder result = new StringBuilder();
        result.append("[");
        for (T element : this) {
            result.append(element + ", ");
        }
        result.delete(result.length() - 2, result.length());
        result.append("]");
        return result.toString();
    }


    ///////////////////////////////////
    // DO NOT CHANGE THE SIZE METHOD //
    ///////////////////////////////////
    /**
     * Returns the current size of this collection.
     *
     * @return  the number of elements in this collection.
     */
    public int size() {
        return size;
    }

    //////////////////////////////////////
    // DO NOT CHANGE THE ISEMPTY METHOD //
    //////////////////////////////////////
    /**
     * Tests to see if this collection is empty.
     *
     * @return  true if this collection contains no elements, false otherwise.
     */
    public boolean isEmpty() {
        return (size == 0);
    }


    /**
     * Ensures the collection contains the specified element. Neither duplicate
     * nor null values are allowed. This method ensures that the elements in the
     * linked list are maintained in ascending natural order.
     *
     * @param  element  The element whose presence is to be ensured.
     * @return true if collection is changed, false otherwise.
     */
    public boolean add(T element) {
        Node n = new Node(element); 

        if (element == null) { throw new NullPointerException(); }
        if (this.contains(element)) { return false; }

        if (isEmpty()) { 
            front = n;
            rear = n;
        } else if (front.element.compareTo(element) > 0) { 
            n.next = front; 
            front.prev = n;
            front = n; 
        } else if (front.element.compareTo(element) < 0) { 
            rear.next = n; 
            n.prev = rear; 
            rear = n; 
        } else { 
            Node before = prevNode(element);
            before.next.prev = n;   
            n.next = before.next; 
            before.next = n; 
            n.prev = before;       
        }

        size++;
        return true; 
    }

    /**
     * Ensures the collection does not contain the specified element.
     * If the specified element is present, this method removes it
     * from the collection. This method, consistent with add, ensures
     * that the elements in the linked lists are maintained in ascending
     * natural order.
     *
     * @param   element  The element to be removed.
     * @return  true if collection is changed, false otherwise.
     */
    public boolean remove(T element) {
        if (element == null) { throw new NullPointerException(); }
        if (isEmpty()) { return false; }

        Node temp = front; 
        
        while (temp != null) { 
            if (temp.element.equals(element)) { 
                if (temp == front) { 
                    front.prev = null; 
                    front = front.next; 
                } else if (temp == rear) { 
                    rear.next = null; 
                    rear = rear.prev;
                } else { 
                    temp.prev.next = temp.next;
                }
                
                size--; 
                return true; 
            }
            temp = temp.next;
        }
        return false; 
    }


    /**
     * Searches for specified element in this collection.
     *
     * @param   element  The element whose presence in this collection is to be tested.
     * @return  true if this collection contains the specified element, false otherwise.
     */
    public boolean contains(T element) {
        if (isEmpty() || front == null) { return false; }

        Node n = front; 
        while (n != null) { 
            if (n.element.equals(element)) { return true; }
            n = n.next; 
        } 
        return false; 
    }


    /**
     * Tests for equality between this set and the parameter set.
     * Returns true if this set contains exactly the same elements
     * as the parameter set, regardless of order.
     *
     * @return  true if this set contains exactly the same elements as
     *               the parameter set, false otherwise
     */
    public boolean equals(Set<T> s) {
        if (size == s.size() && complement(s).size() == 0) { 
            return true;
        } else { 
            return false; 
        }
    }


    /**
     * Tests for equality between this set and the parameter set.
     * Returns true if this set contains exactly the same elements
     * as the parameter set, regardless of order.
     *
     * @return  true if this set contains exactly the same elements as
     *               the parameter set, false otherwise
     */
    public boolean equals(LinkedSet<T> s) {
        if (size == s.size() && complement(s).size() == 0) { 
            return true;
        } else { 
            return false; 
        }
    }


    /**
     * Returns a set that is the union of this set and the parameter set.
     *
     * @return  a set that contains all the elements of this set and the parameter set
     */
    public Set<T> union(Set<T> s){
        if (s == null) { throw new NullPointerException(); }

        LinkedSet<T> returnSet = new LinkedSet<T>(); 
        
        Node temp = front; 
        while (temp != null) { 
            returnSet.add(temp.element);
            temp = temp.next;
        }

        Iterator<T> temp2 = s.iterator(); 
        while (temp2.hasNext()) { 
            returnSet.add(temp2.next());
        } 

        return returnSet;
    }


    /**
     * Returns a set that is the union of this set and the parameter set.
     *
     * @return  a set that contains all the elements of this set and the parameter set
     */
    public Set<T> union(LinkedSet<T> s){
        if (s == null) { throw new NullPointerException(); }

        LinkedSet<T> returnSet = new LinkedSet<T>(); 
        
        Node temp = front; 
        while (temp != null) { 
            returnSet.add(temp.element);
            temp = temp.next;
        }

        Iterator<T> temp2 = s.iterator(); 
        while (temp2.hasNext()) { 
            returnSet.add(temp2.next());
        } 

        return returnSet;
    }


    /**
     * Returns a set that is the intersection of this set and the parameter set.
     *
     * @return  a set that contains elements that are in both this set and the parameter set
     */
    public Set<T> intersection(Set<T> s) {
        if (s == null) { throw new NullPointerException(); }

        LinkedSet<T> returnSet = new LinkedSet<T>();

        Node temp = front; 
        while (temp != null) { 
            if (s.contains((T)temp.element)) { returnSet.add((T)temp.element); } 
            temp = temp.next;
        }

        return returnSet; 
    }

    /**
     * Returns a set that is the intersection of this set and
     * the parameter set.
     *
     * @return  a set that contains elements that are in both
     *            this set and the parameter set
     */
    public Set<T> intersection(LinkedSet<T> s) {
        if (s == null) { throw new NullPointerException(); }

        LinkedSet<T> returnSet = new LinkedSet<T>();

        Node temp = front; 
        while (temp != null) { 
            if (s.contains((T)temp.element)) { returnSet.add((T)temp.element); } 
            temp = temp.next;
        }

        return returnSet; 
    }


    /**
     * Returns a set that is the complement of this set and the parameter set.
     *
     * @return  a set that contains elements that are in this set but not the parameter set
     */
    public Set<T> complement(Set<T> s) {
        if (s == null) { throw new NullPointerException(); }

        LinkedSet<T> returnSet = new LinkedSet<T>();

        Node temp = front;
        while (temp != null) { 
            if(!s.contains((T)temp.element)) { returnSet.add((T)temp.element); }
            temp = temp.next;
        }

        return returnSet;
    }


    /**
     * Returns a set that is the complement of this set and
     * the parameter set.
     *
     * @return  a set that contains elements that are in this
     *            set but not the parameter set
     */
    public Set<T> complement(LinkedSet<T> s) {
        if (s == null) { throw new NullPointerException(); }

        LinkedSet<T> returnSet = new LinkedSet<T>();

        Node temp = front;
        while (temp != null) { 
            if(!s.contains((T)temp.element)) { returnSet.add((T)temp.element); }
            temp = temp.next;
        }
        
        return returnSet;
    }


    /**
     * Returns an iterator over the elements in this LinkedSet.
     * Elements are returned in ascending natural order.
     *
     * @return  an iterator over the elements in this LinkedSet
     */
    public Iterator<T> iterator() { return new myIterator(); }

    /**
     * Returns an iterator over the elements in this LinkedSet.
     * Elements are returned in descending natural order.
     *
     * @return  an iterator over the elements in this LinkedSet
     */
    public Iterator<T> descendingIterator() { return new myDescendingIterator(rear); }


    /**
     * Returns an iterator over the members of the power set
     * of this LinkedSet. No specific order can be assumed.
     *
     * @return  an iterator over members of the power set
     */
    public Iterator<Set<T>> powerSetIterator() { return new myPowerIterator(front, size); }

    //////////////////////////////
    // Private utility methods. //
    //////////////////////////////

    private Node prevNode(T element) {
        Node n = front;
        while (n != null) {
           if (n.element.compareTo(element) > 0) {
              return n.prev;
           }
           n = n.next;
        }
        return n;
     }

    ////////////////////
    // Nested classes //
    ////////////////////

    private class myIterator implements Iterator<T> { 
        private Node current = front; 

        public boolean hasNext() { return current != null; }
        public void remove() { throw new UnsupportedOperationException(); }
        public T next() { 
            if (!hasNext()) { throw new NoSuchElementException(); }
            T result = current.element; 
            current = current.next; 
            return result; 
        }
    }

    private class myDescendingIterator implements Iterator<T> { 
        private Node temp; 
        
        public myDescendingIterator(Node rear) { 
            temp = rear; 
        }

        public boolean hasNext() { return temp != null && temp.element != null; }
        public void remove() { throw new UnsupportedOperationException(); }
        public T next() { 
            if (temp != null){ 
                T r = temp.element; 
                temp = temp.prev;
                return r; 
            }
            return null;
        }
    }
        
    private class myPowerIterator implements Iterator<Set<T>> { 
        private Node temp; 
        private int current1, current2; 
        private int bit = 0;

        public myPowerIterator(Node front, int size) {
            temp = front; 
            current1 = size; 
            current2 = 0; 
        }

        public boolean hasNext() { return (current2 < (int) Math.pow(2, current1)); } 
        public void remove() { throw new UnsupportedOperationException(); }
        public Set<T> next() { 
            Set<T> r = new LinkedSet<T>(); 
            int m = 1; 
            for (int i = 0; i < current1; i++) { 
                if ((bit & m) != 0) { 
                    r.add(temp.element);
                    temp = temp.next;
                } else { 
                    temp = temp.next;
                }
            }
            current2++; 
            bit = 0; 
            temp = front; 
            return r;
        }
    }


    //////////////////////////////////////////////
    // DO NOT CHANGE THE NODE CLASS IN ANY WAY. //
    //////////////////////////////////////////////

    /**
     * Defines a node class for a doubly-linked list.
     */
    class Node {
        /** the value stored in this node. */
        T element;
        /** a reference to the node after this node. */
        Node next;
        /** a reference to the node before this node. */
        Node prev;

        /**
         * Instantiate an empty node.
         */
        public Node() {
            element = null;
            next = null;
            prev = null;
        }

        /**
         * Instantiate a node that containts element
         * and with no node before or after it.
         */
        public Node(T e) {
            element = e;
            next = null;
            prev = null;
        }
    }

}
