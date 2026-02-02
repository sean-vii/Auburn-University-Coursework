package M3.Assignment_3;

import java.util.Comparator;

/**
 * Autocomplete term representing a (query, weight) pair.
 * 
 */
public class Term implements Comparable<Term> {
    private String query = ""; 
    private Long weight = null; 
    /**
     * Initialize a term with the given query and weight.
     * This method throws a NullPointerException if query is null,
     * and an IllegalArgumentException if weight is negative.
     */
    public Term(String queryInput, long weightInput) {
        if (query == null || query == "") { throw new NullPointerException(); } 
        if (weightInput < 0) { throw new IllegalArgumentException(); }
        
        query = queryInput; 
        weight = weightInput;
    }

    /**
     * Compares the two terms in descending order of weight.
     */
    public static Comparator<Term> byDescendingWeightOrder() {
        return new Comparator<Term>() {
            public int compare(Term T1, Term T2) { 
                return T2.weight.compareTo(T1.weight);    
            }
        };
    }

    /**
     * Compares the two terms in ascending lexicographic order of query,
     * but using only the first length characters of query. This method
     * throws an IllegalArgumentException if length is less than or equal
     * to zero.
     */
    public static Comparator<Term> byPrefixOrder(int length) {
        if (length <= 0) { throw new IllegalArgumentException(); }
        
        return new Comparator<Term>() {
            public int compare(Term T1, Term T2) { 
                String T1_trim = T1.query;
                String T2_trim = T2.query;
                
                if (length < T1.query.length()) { T1_trim = T1_trim.substring(0, length); }
                if (length < T2.query.length()) { T2_trim = T2_trim.substring(0, length); }
                
                return T1_trim.compareToIgnoreCase(T2_trim);
            }
        };
    }

    /**
     * Compares this term with the other term in ascending lexicographic order
     * of query.
     */
    @Override
    public int compareTo(Term other) {
        return this.query.compareTo(other.query);
    }

    /**
     * Returns a string representation of this term in the following format:
     * query followed by a tab followed by weight
     */
    @Override
    public String toString(){
        return query + "\t" + weight.toString();
    }

    public String getQuery(){ return query; }

}

