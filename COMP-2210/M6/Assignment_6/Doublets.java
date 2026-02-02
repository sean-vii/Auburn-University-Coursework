package M6.Assignment_6;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

import java.util.Arrays;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;
import java.util.TreeSet;

import java.util.stream.Collectors;

/**
 * Provides an implementation of the WordLadderGame interface. 
 *
 * @author Your Name (you@auburn.edu)
 */
public class Doublets implements WordLadderGame {

    // The word list used to validate words.
    // Must be instantiated and populated in the constructor.
    /////////////////////////////////////////////////////////////////////////////
    // DECLARE A FIELD NAMED lexicon HERE. THIS FIELD IS USED TO STORE ALL THE //
    // WORDS IN THE WORD LIST. YOU CAN CREATE YOUR OWN COLLECTION FOR THIS     //
    // PURPOSE OF YOU CAN USE ONE OF THE JCF COLLECTIONS. SUGGESTED CHOICES    //
    // ARE TreeSet (a red-black tree) OR HashSet (a closed addressed hash      //
    // table with chaining).
    /////////////////////////////////////////////////////////////////////////////

    private TreeSet<String> lexicon = new TreeSet<String>();

    /**
     * Instantiates a new instance of Doublets with the lexicon populated with
     * the strings in the provided InputStream. The InputStream can be formatted
     * in different ways as long as the first string on each line is a word to be
     * stored in the lexicon.
     */
    public Doublets(InputStream in) {
        try {
            lexicon = new TreeSet<String>();
            Scanner s = new Scanner(new BufferedReader(new InputStreamReader(in)));
            while (s.hasNext()) {
                String str = s.next();
                lexicon.add(str.toLowerCase());
                s.nextLine();
            }
            in.close();
        }
        catch (java.io.IOException e) {
            System.err.println("Error reading from InputStream.");
            System.exit(1);
        }
    }

    //////////////////////////////////////////////////////////////
    // ADD IMPLEMENTATIONS FOR ALL WordLadderGame METHODS HERE  //
    //////////////////////////////////////////////////////////////

    public int getWordCount() {
        return lexicon.size();
    }

    public boolean isWord(String str) {
        str = str.toLowerCase();
        if (lexicon.contains(str)) {
           return true;
        } else { 
            return false;
        }
    }

    public int getHammingDistance(String str1, String str2) {
        int ham = 0; 

        str1 = str1.toLowerCase();
        str2 = str2.toLowerCase();

        if (str1.length() != str2.length()) { 
            return -1; 
        } else { 
            for (int i = 0; i < str1.length(); i++) {
                if (str1.charAt(i) != str2.charAt(i)) { ham++; }
            }
            return ham; 
        }
    }

    public List<String> getNeighbors(String word) {
        List<String> neighbors = new ArrayList<String>(); 
        for (String current : lexicon) { 
            if (getHammingDistance(word, current) == 1) { neighbors.add(current); }
        } 

        return neighbors;
    }

    public boolean isWordLadder(List<String> sequence) {
        if (sequence.isEmpty()) { return false; }

        for (int i = 0; i < sequence.size() - 1; i++) {
            if (!isWord(sequence.get(i)) 
                    || !isWord(sequence.get(i + 1)) 
                    || getHammingDistance(sequence.get(i), sequence.get(i + 1)) != 1) {
                return false;
            }
        }
        return true;
    }

    public List<String> getMinLadder(String start, String end) {
        List<String> temp = new ArrayList<String>();
        List<String> ladder = new ArrayList<String>();
        
        start = start.toLowerCase();
        end = end.toLowerCase();

        if (start == null 
            || end == null
            || getHammingDistance(start, end) == -1
            || !isWord(start) 
            || !isWord(end)) { 
            return temp; 
        } else if (start.equals(end)) { 
            ladder.add(start);
            return ladder; 
        }

        ArrayDeque<Node> remaining = new ArrayDeque<Node>();
        HashSet<String> handled = new HashSet<String>();

        Node firstNode = new Node(start, null);
        handled.add(firstNode.position);
        remaining.add(firstNode);

        while (!remaining.isEmpty()) { 
            Node current = remaining.removeFirst();
            List<String> neighbors = getNeighbors(current.position); 
            for (String neighbor : neighbors) {
                if (!handled.contains(neighbor)) {
                    Node neighborNode = new Node(neighbor, current);
                    handled.add(neighbor);
                    remaining.addLast(neighborNode);
                    if (neighbor.equals(end)) { // Once end is reached return path
                        return toList(new Node(neighbor, current));
                    }
                }
            }
        }
        return temp;
    }

    private List<String> toList(Node n) {
        List<String> list = new ArrayList<String>();
        String word = n.position;
        Node prev = n.predecessor;
        list.add(word);
        while (prev != null) {
            word = prev.position;
            list.add(0, word);
            prev = prev.predecessor;
        }
        return list;
    }

    private class Node {
        String position;
        Node predecessor;

        public Node(String p, Node pred) {
            position = p;
            predecessor = pred;
        }
    }
}

