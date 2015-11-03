package onetimepad;

import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.SecureRandom;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class OneTimePad {

	// Sets up hashMap for converting
	private static final Map<String, Integer> lettersToNumbersMap;
	private static Scanner s = new Scanner(System.in);

	static {
		lettersToNumbersMap = new HashMap<String, Integer>();
		lettersToNumbersMap.put("a", 0);
		lettersToNumbersMap.put("b", 1);
		lettersToNumbersMap.put("c", 2);
		lettersToNumbersMap.put("d", 3);
		lettersToNumbersMap.put("e", 4);
		lettersToNumbersMap.put("f", 5);
		lettersToNumbersMap.put("g", 6);
		lettersToNumbersMap.put("h", 7);
		lettersToNumbersMap.put("i", 8);
		lettersToNumbersMap.put("j", 9);
		lettersToNumbersMap.put("k", 10);
		lettersToNumbersMap.put("l", 11);
		lettersToNumbersMap.put("m", 12);
		lettersToNumbersMap.put("n", 13);
		lettersToNumbersMap.put("o", 14);
		lettersToNumbersMap.put("p", 15);
		lettersToNumbersMap.put("q", 16);
		lettersToNumbersMap.put("r", 17);
		lettersToNumbersMap.put("s", 18);
		lettersToNumbersMap.put("t", 19);
		lettersToNumbersMap.put("u", 20);
		lettersToNumbersMap.put("v", 21);
		lettersToNumbersMap.put("w", 22);
		lettersToNumbersMap.put("x", 23);
		lettersToNumbersMap.put("y", 24);
		lettersToNumbersMap.put("z", 25);
		lettersToNumbersMap.put(" ", 26);
		lettersToNumbersMap.put(".", 27);
		lettersToNumbersMap.put(",", 28);
	}

	// Used in modding each character
	private static final int modValue = lettersToNumbersMap.size();

	// Converts the passed string to an array of integers
	private static int[] convertToIntArray(String inputString) {
		int textLength = inputString.length();
		int convertedInput[] = new int[textLength];

		// Converts the input text to an array of integers, according to the
		// above hashMap
		for (int i = 0; i < inputString.length(); i++) {
			String character = Character.toString(inputString.charAt(i));

			// If this character is a key in the hashMap, convert to to an
			// integer
			// If it isn't, set the integer to 27, a full stop
			if (lettersToNumbersMap.keySet().contains(character)) {
				int value = lettersToNumbersMap.get(character);
				convertedInput[i] = value;
			} else {
				convertedInput[i] = 27;
			}
		}

		return convertedInput;
	}

	// Converts the passed int array to a string
	private static String convertToString(int[] intArray) {

		String outputString = "";

		// Loops through the array
		for (int elementInArray : intArray) {

			// Loops through every key in the hashMap
			for (String character : lettersToNumbersMap.keySet()) {
				// If the key is the same as the element in the array, add it to
				// the string
				if (lettersToNumbersMap.get(character).equals(elementInArray)) {
					outputString = outputString + character;
				}
			}
		}
		return outputString;
	}

	// Returns an encryption key, whether random or user entered
	private static int[] getKey(String keyChoice, int lengthOfKey) {
		int[] encryptionKey = new int[lengthOfKey];

		// Creates a random key
		if (keyChoice.equals("random")) {
			try {

				// Makes a SecureRandom instance and seeds with 2^20 bits
				SecureRandom sr = SecureRandom.getInstance("SHA1PRNG", "SUN");
				byte[] bytes = new byte[20];
				sr.nextBytes(bytes);

				// Sets the i_th index of encryptionKey to a random integer
				// between 1 and modValue, inclusive
				for (int i = 0; i < lengthOfKey; i++) {

					// Avoids dividing by zero
					int randomInt = sr.nextInt(modValue - 1) + 1;
					encryptionKey[i] = randomInt;
				}

			} catch (NoSuchProviderException | NoSuchAlgorithmException e) {
				System.out.println("Exception: " + e.getMessage());
				System.out.println("Exception: " + e.getStackTrace());
			}
		}

		return encryptionKey;
	}

	// Returns the ciphertext of convertedInput % encryptionKey
	private static int[] getCipherText(int[] convertedInput, int[] encryptionKey) {
		int[] ciphertext = new int[convertedInput.length];

		for (int i = 0; i < convertedInput.length; i++) {
			ciphertext[i] = (convertedInput[i] + encryptionKey[i]) % modValue;
		}

		return ciphertext;
	}

	private static String getPlaintext(int[] encryptionKeyArray, int[] ciphertextArray, int textLength) {

		int[] plaintextArray = new int[textLength];

		// Works out the plaintext
		for (int i = 0; i < textLength; i++) {
			plaintextArray[i] = Math.floorMod(ciphertextArray[i] - encryptionKeyArray[i], modValue);
		}

		// Prints the plaintextArra without the first and last commas
		System.out.println("plaintextArray: ");
		String plaintextArrayString = "";
		for (int value : plaintextArray) {
			plaintextArrayString = (plaintextArrayString + ", " + value);
		}
		plaintextArrayString = plaintextArrayString.substring(2, plaintextArrayString.length());
		System.out.println(plaintextArrayString);
		System.out.println("");

		String plaintext = convertToString(plaintextArray);
		return plaintext;
	}

	private static void encrypt() {

		// Gets input text
		System.out.println("");
		System.out.println("Enter text to convert: ");
		String inputText = s.nextLine().toLowerCase();
		System.out.println("");

		int convertedInput[] = convertToIntArray(inputText);
		int encryptionKey[] = new int[inputText.length()];

		// Prints the encryptionKey without the first and last commas
		System.out.println("convertedInput:");
		String convertedInputString = "";
		for (int value : convertedInput) {
			convertedInputString = (convertedInputString + ", " + value);
		}
		convertedInputString = convertedInputString.substring(2, convertedInputString.length());
		System.out.println(convertedInputString);
		System.out.println("");

		// Lets the user pick between having a random encryption key, or
		// entering their own

		System.out.println("Encryption key options:");
		System.out.println("#1: Random key");
		System.out.println("#2: User-entered key");
		System.out.print("Choice: ");

		// Catches any number format errors
		int option = 1;
		try {
			option = Integer.parseInt(s.nextLine());
		} catch (NumberFormatException e) {
			System.out.println("NumberFormatException: " + e.getMessage());
			System.out.println("NumberFormatException: " + e.getStackTrace());

		}
		System.out.println("");

		switch (option) {
		case 1:
			encryptionKey = getKey("random", inputText.length());
			break;
		case 2:
			encryptionKey = getKey("user", inputText.length());
			break;
		}

		// Prints the encryptionKey without the first and last commas
		System.out.println("encryptionKey (copy this):");
		String encryptionKeyString = "";
		for (int value : encryptionKey) {
			encryptionKeyString = (encryptionKeyString + ", " + value);
		}
		encryptionKeyString = encryptionKeyString.substring(2, encryptionKeyString.length());
		System.out.println(encryptionKeyString);

		String encryptionKeyString2 = convertToString(encryptionKey);
		System.out.println(encryptionKeyString2);
		System.out.println("");

		// Gets ciphertext
		int[] ciphertext = getCipherText(convertedInput, encryptionKey);

		// Prints the ciphertext without the first and last commas
		System.out.println("ciphertext (copy this):");
		String ciphertextString = "";
		for (int value : ciphertext) {
			ciphertextString = (ciphertextString + ", " + value);
		}
		ciphertextString = ciphertextString.substring(2, ciphertextString.length());
		System.out.println(ciphertextString);

		String ciphertextString2 = convertToString(ciphertext);
		System.out.println(ciphertextString2);
		System.out.println("");
	}

	private static void decrypt() {

		// Gets the encryptionKey as an array of integers
		System.out.println("");
		System.out.println("Enter encryptionKey: ");
		String encryptionKeyString = s.nextLine();

		// Parses the string array to an int array
		int[] encryptionKeyArray = convertToIntArray(encryptionKeyString);
		int keyLength = encryptionKeyArray.length;

		// Prints the encryptionKey without the first and last commas
		System.out.println("encryptionKey:");
		String encryptionKeyString2 = "";
		for (int value : encryptionKeyArray) {
			encryptionKeyString2 = (encryptionKeyString2 + ", " + value);
		}
		encryptionKeyString2 = encryptionKeyString2.substring(2, encryptionKeyString2.length());
		System.out.println(encryptionKeyString2);
		System.out.println("");

		// Gets the ciphertext as an array of integers
		System.out.println("Enter ciphertext: ");
		String ciphertextString = s.nextLine();

		// Parses the string array to an int array
		int[] ciphertextArray = convertToIntArray(ciphertextString);

		// Prints the ciphertext without the first and last commas
		System.out.println("ciphertext :");
		String ciphertextString2 = "";
		for (int value : ciphertextArray) {
			ciphertextString2 = (ciphertextString2 + ", " + value);
		}
		ciphertextString2 = ciphertextString2.substring(2, ciphertextString2.length());
		System.out.println(ciphertextString2);
		System.out.println("");

		String plaintext = getPlaintext(encryptionKeyArray, ciphertextArray, keyLength);
		System.out.println("Original plaintext: ");
		System.out.println(plaintext);

	}

	public static void main(String[] args) {
		System.out.println("lettersToNumbersMap: " + lettersToNumbersMap);

		// Lets the user pick between having a random encryption key, or
		// entering their own
		System.out.println("");
		System.out.println("Options:");
		System.out.println("#1: Encryption");
		System.out.println("#2: Decryption");
		System.out.print("Choice: ");

		// Catches any number format errors
		int option = 1;
		try {
			option = Integer.parseInt(s.nextLine());
		} catch (NumberFormatException e) {
			System.out.println("NumberFormatException: " + e.getMessage());
			System.out.println("NumberFormatException: " + e.getStackTrace());
		}

		switch (option) {
		case 1:
			encrypt();
			break;
		case 2:
			decrypt();
			break;
		}

		s.close();

	}

}