package M5.Assignment_5;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;
import java.util.SortedSet;
import java.util.TreeSet;

public class WordSearch implements WordSearchGame {

    private TreeSet<String> words;
    private String[][] board;
    private int size;

    private SortedSet<String> wordsList;

    public WordSearch() {
        words = null;
        size = 4;
        board = new String[size][size];
    }

    public void loadLexicon(String fileName) {
        if (fileName == null) { throw new IllegalArgumentException(); }

        try {
            words = new TreeSet<String>();
            Scanner file = new Scanner(new File(fileName));

            while (file.hasNext()) { words.add(file.next().toUpperCase()); }

            file.close();
        } catch (FileNotFoundException e) {
            throw new IllegalArgumentException();
        }
    }

    public void setBoard(String[] letterArray) {
        if (letterArray == null) { throw new IllegalArgumentException(); }

        double n = Math.sqrt(Double.valueOf(letterArray.length));
        if (n % 1 > 0.0001) { throw new IllegalArgumentException(); }
        board = new String[(int) n][(int) n];

        int cnt = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                board[i][j] = letterArray[cnt++];
            }
        }
        size = (int) n;
    }

    public String getBoard() {
        String boardString = "";
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) { 
                boardString += board[i][j] + " "; 
            }
        }
        return boardString;
    }

    public SortedSet<String> getAllScorableWords(int minimumWordLength) {
        if (minimumWordLength < 1) { throw new IllegalArgumentException(); }
        if (words == null) { throw new IllegalStateException(); }

        wordsList = new TreeSet<String>();
        LinkedList<Integer> tempList = new LinkedList<Integer>();
        for (int i = 0; i < (size * size); i++) {
            tempList.add(i);
            String tempString = toWord(tempList);
            if (isValidWord(tempString) && tempString.length() >= minimumWordLength) {
                wordsList.add(tempString);
            } else if (isValidPrefix(tempString)) {
                search(tempList, minimumWordLength);
            }

            tempList.clear();
        }

        return wordsList;
    }

    public String toWord(LinkedList<Integer> listIn) {
        String word = "";
        for (int i : listIn) { word += new Position(i).getLetter(); }
        return word;
    }

    private LinkedList<Integer> search(LinkedList<Integer> wordPre, int min) {
        Position[] next = new Position(wordPre.getLast()).next(wordPre);

        for (Position pos : next) {
            if (pos == null) { break; }
            wordPre.add(pos.getIndex());
            String wordStr = toWord(wordPre);
            if (isValidPrefix(wordStr)) {
                if (isValidWord(wordStr) && wordStr.length() >= min) {
                    wordsList.add(wordStr);
                }
                search(wordPre, min);
            } else {
                wordPre.removeLast();
            }
        }

        wordPre.removeLast();
        return wordPre;
    }

    private LinkedList<Integer> searchForWord(LinkedList<Integer> wordPre, int index, String wordToCheck) {
        if (wordPre.size() > 0 && !wordToCheck.equals(toWord(wordPre))) {
            Position[] next = new Position(wordPre.getLast()).next(wordPre);
            for (Position p : next) {
                if (p == null) {
                    break;
                }
                wordPre.add(p.getIndex());
                String wordStr = toWord(wordPre);
                if (wordToCheck.equals(wordStr)) { 
                    break;
                } else if (wordToCheck.startsWith(wordStr)) {
                    searchForWord(wordPre, p.getIndex(), wordToCheck);
                } else {
                    wordPre.removeLast();
                }
            }
        }

        if (wordPre.size() == 0) {
            while (index < size * size) {
                if (wordToCheck.startsWith(new Position(index).getLetter())) {
                    wordPre.add(index);
                    searchForWord(wordPre, index, wordToCheck);
                }
                index++;
            }
            return wordPre;
        }

        if (toWord(wordPre).equals(wordToCheck)) {
            return wordPre;
        } else {
            wordPre.removeLast();
            return wordPre;
        }
    }

    private class Position {
        private int x;
        private int y;
        private int index;
        private String letter;

        Position(int indexIn) {
            this.index = indexIn;
            if (index == 0) {
                this.x = 0;
                this.y = 0;
            } else {
                this.x = index % size;
                this.y = index / size;
            }
            this.letter = board[y][x];
        }

        Position(int xIn, int yIn) {
            this.x = xIn;
            this.y = yIn;
            this.index = (y * size) + x;
            this.letter = board[y][x];
        }

        private boolean isValid(int iIn, int jIn) {
            return (iIn >= 0) && (iIn < size) && (jIn >= 0) && (jIn < size);
        }

        public Position[] next(LinkedList<Integer> visited) {
            Position[] nbrs = new Position[8];
            int count = 0;

            for (int i = this.x - 1; i <= this.x + 1; i++) {
                for (int j = this.y - 1; j <= this.y + 1; j++) {
                    if (!((i == this.x) && (j == this.y))) {
                        if (isValid(i, j) && !visited.contains((j * size) + i)) {
                            Position p = new Position(i, j);
                            nbrs[count++] = p;
                        }
                    }
                }
            }
            return nbrs;

        }

        public String getLetter() { return letter; }
        public int getIndex() { return index; }
    }

    public int getScoreForWords(SortedSet<String> words, int minimumWordLength) {
        if (minimumWordLength < 1) { throw new IllegalArgumentException(); }
        if (words == null) { throw new IllegalStateException(); }

        int score = 0;
        Iterator<String> iter = words.iterator();
        while (iter.hasNext()) {
            String curr = iter.next();
            if (curr.length() >= minimumWordLength && isValidWord(curr) && !isOnBoard(curr).isEmpty()) {
                score += 1 + (curr.length() - minimumWordLength);
            }
        }
        return score;
    }

    public boolean isValidWord(String wordToCheck) {
        if (wordToCheck == null) { throw new IllegalArgumentException(); }
        if (words == null) { throw new IllegalStateException(); }
        
        return words.contains(wordToCheck);
    }

    public boolean isValidPrefix(String prefixToCheck) {
        if (prefixToCheck == null) { throw new IllegalArgumentException(); }
        if (words == null) { throw new IllegalStateException(); }

        String temp = words.ceiling(prefixToCheck);
        if (temp == null) { return false; }

        return temp.startsWith(prefixToCheck);
    }

    public List<Integer> isOnBoard(String wordToCheck) {
        if (wordToCheck == null) { throw new IllegalArgumentException(); }
        if (words == null) { throw new IllegalStateException(); }

        LinkedList<Integer> pathList = new LinkedList<Integer>();
        List<Integer> finalPath = searchForWord(pathList, 0, wordToCheck);

        return finalPath;
    }
}