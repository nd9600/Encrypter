package onetimepad;

import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class OneTimePad {
    
	//Sets up hashMap for converting
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
        lettersToNumbersMap.put(" ", 27);
        lettersToNumbersMap.put(".", 28);
        lettersToNumbersMap.put(",", 29);
    }
	
	//Used in modding each character
	private static final int modValue = lettersToNumbersMap.size();
	
	//Returns an encryption key, whether random or user entered
	private static String getKey(String choice, int lengthOfKey){
		return "abc";
	}
	
	public static void main(String[] args){
		System.out.println("lettersToNumbersMap: " + lettersToNumbersMap);
		
		Scanner s = new Scanner(System.in);
		String outputText = "";
		String key = "";
		
		//Gets input text
		System.out.println("Enter text to convert: ");
		String inputText = s.nextLine();
		System.out.println("");
		
		//Converts the input text to a string of numbers, according to the above hashMap
		for (int i = 0; i < inputText.length(); i++){
			String character = Character.toString( inputText.charAt(i) );
			String value = lettersToNumbersMap.get(character).toString();
			outputText = (outputText + "," + value);
		}
		
		//Removes the first and last "," characters
		outputText = outputText.substring(1, (outputText.length()) );
		
		System.out.println("Converted: ");
		System.out.println(outputText);
		
		//Lets the user pick between having a random encryption key, or entering their own
		System.out.println("");
		System.out.println("Options:");
		System.out.println("#1: Random key");
		System.out.println("#2: User-entered key");
		System.out.print("Choice: ");
		int option = s.nextInt();
		
        switch (option) {
            case 1:  key = getKey("random" , inputText.length());
                     break;
            case 2:  key = getKey("user", inputText.length());
            break;
        }
        
        System.out.println("");
		System.out.println("Key: " + key);
        
        s.close();
		
	}
	
}