package onetimepad;

import java.util.HashMap;
import java.util.Map;

public class OneTimePad {
    
	private static final Map<String, Integer> lettersToNumbersMap;
	static
    {
		lettersToNumbersMap = new HashMap<String, Integer>();
        lettersToNumbersMap.put("a", 1);
        lettersToNumbersMap.put("b", 2);
        lettersToNumbersMap.put("c", 3);
        lettersToNumbersMap.put("d", 4);
        lettersToNumbersMap.put("e", 5);
        lettersToNumbersMap.put("f", 6);
        lettersToNumbersMap.put("g", 7);
        lettersToNumbersMap.put("h", 8);
        lettersToNumbersMap.put("i", 9);
        lettersToNumbersMap.put("j", 10);
        lettersToNumbersMap.put("k", 11);
        lettersToNumbersMap.put("l", 12);
        lettersToNumbersMap.put("m", 13);
        lettersToNumbersMap.put("n", 14);
        lettersToNumbersMap.put("o", 15);
        lettersToNumbersMap.put("p", 16);
        lettersToNumbersMap.put("q", 17);
        lettersToNumbersMap.put("r", 18);
        lettersToNumbersMap.put("s", 19);
        lettersToNumbersMap.put("t", 20);
        lettersToNumbersMap.put("u", 21);
        lettersToNumbersMap.put("v", 22);
        lettersToNumbersMap.put("w", 23);
        lettersToNumbersMap.put("x", 24);
        lettersToNumbersMap.put("y", 25);
        lettersToNumbersMap.put("z", 26);
    }
	
	public static void main(String[] args){
		System.out.println("lettersToNumbersMap: " + lettersToNumbersMap);
	}
	
}