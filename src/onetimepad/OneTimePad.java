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

	static {
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

	// Used in modding each character
	private static final int modValue = lettersToNumbersMap.size();

	// Returns an encryption key, whether random or user entered
	private static int[] getKey(String keyChoice, int lengthOfKey) {
		int[] encryptionKey = new int[lengthOfKey];

		if (keyChoice.equals("random")) {
			try {
				SecureRandom sr = SecureRandom.getInstance("SHA1PRNG", "SUN");
				byte[] bytes = new byte[20];
				sr.nextBytes(bytes);

				for (int i = 0; i < lengthOfKey; i++) {
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

	private static int[] getCipherText(int[] convertedInput, int[] encryptionKey) {
		int[] ciphertext = new int[convertedInput.length];

		for (int i = 0; i < convertedInput.length; i++) {
			ciphertext[i] = convertedInput[i] % encryptionKey[i];
		}

		return ciphertext;
	}

	private static void encrypt() {

		// Gets input text
		Scanner s2 = new Scanner(System.in);
		System.out.println("");
		System.out.println("Enter text to convert: ");

		String inputText = s2.nextLine();
		int convertedInput[] = new int[inputText.length()];
		int encryptionKey[] = new int[inputText.length()];
		System.out.println("");

		// Converts the input text to an array of integers, according to the
		// above hashMap
		for (int i = 0; i < inputText.length(); i++) {
			String character = Character.toString(inputText.charAt(i));
			int value = lettersToNumbersMap.get(character);
			convertedInput[i] = value;
		}

		System.out.println("Converted: ");
		for (int value : convertedInput) {
			System.out.print(value + ", ");
		}
		System.out.println("");

		// Lets the user pick between having a random encryption key, or
		// entering their own

		System.out.println("");
		System.out.println("Encryption key options:");
		System.out.println("#1: Random key");
		System.out.println("#2: User-entered key");
		System.out.print("Choice: ");
		int option = s2.nextInt();
		s2.close();

		switch (option) {
		case 1:
			encryptionKey = getKey("random", inputText.length());
			break;
		case 2:
			encryptionKey = getKey("user", inputText.length());
			break;
		}

		System.out.println("");
		System.out.println("encryptionKey:");
		for (int value : encryptionKey) {
			System.out.print(value + ", ");
		}
		System.out.println("");

		// Gets ciphertext
		int[] ciphertext = getCipherText(convertedInput, encryptionKey);

		System.out.println("");
		System.out.println("ciphertext:");
		for (int value : ciphertext) {
			System.out.print(value + ", ");
		}
		System.out.println("");
	}

	private static void decrypt() {

	}

	public static void main(String[] args) {
		System.out.println("lettersToNumbersMap: " + lettersToNumbersMap);

		Scanner s = new Scanner(System.in);

		// Lets the user pick between having a random encryption key, or
		// entering their own
		System.out.println("");
		System.out.println("Options:");
		System.out.println("#1: Encryption");
		System.out.println("#2: Decryption");
		System.out.print("Choice: ");
		int option = s.nextInt();
		s.close();

		switch (option) {
		case 1:
			encrypt();
			break;
		case 2:
			decrypt();
			break;
		}

	}

}