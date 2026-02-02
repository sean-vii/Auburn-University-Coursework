package M3.Assignment_3;

import java.util.Arrays;

/**
 * Autocomplete.
 */
public class AutoComplete {

	private Term[] terms;

	/**
	 * Initializes a data structure from the given array of terms.
	 * This method throws a NullPointerException if terms is null.
	 */
	public void Autocomplete(Term[] termsInput) {
        if (termsInput == null) { throw new NullPointerException(); }

        terms = termsInput; 
    }

	/** 
	 * Returns all terms that start with the given prefix, in descending order of weight. 
	 * This method throws a NullPointerException if prefix is null.
	 */
	public Term[] allMatches(String prefix) {
        if (prefix == null) { throw new NullPointerException(); }

        int numPrefixes = 0;  
        Term[] tempPrefixes = new Term[terms.length]; 
        for(int i = 0; i < terms.length; i++) { 
            if (terms[i].getQuery().startsWith(prefix)) { 
                tempPrefixes[i] = terms[i];
                numPrefixes++;  
            }
        } 

        Term[] prefixes = new Term[numPrefixes];
        for (int i = 0; i < numPrefixes; i++) { 
            prefixes[i] = tempPrefixes[i];
        }

        Arrays.sort(prefixes, Term.byDescendingWeightOrder()); 

        return prefixes; 
    }
}