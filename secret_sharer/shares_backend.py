import sympy
import random
import math

from utils import *

def getShares(secret, numberOfParts, threshold):
    rng = random.SystemRandom()
    randomNumbers = {}

    #Max value of each secret (since they are bytes is 255)
    #269 is prime and bigger than 255, so we can use it
    modulus = 269

    #Picks _threshold-1_ random numbers
    for i in range(1, threshold):
        randomNumbers[i] = rng.randint(1, modulus)

    print ""
    print "secret:", secret
    print "numberOfParts:", numberOfParts
    print "randomNumbers:", randomNumbers

    #If the secret is 0, just return zero for the shares
    if (secret == 0):
        shares = []
        for i in range(1, numberOfParts+1):
            shares.append( "%s-0" % (str(i)) )

        return shares

    else:
        #Creates a polynomial of degree 'threshold-1', where x_0 = secret
        #and every other x is a term with a random coefficient
        #and increasing power of x
        x, y = sympy.symbols('x, y')
        polynomial = secret
        for i in range(1, threshold):
            polynomial = polynomial + (randomNumbers[i])*x**i
        print ""
        print "polynomial:", polynomial

        #Picks _numberOfParts_ number of points in order of x-value from the polynomial, and returns them
        shares = []
        for i in range(1, numberOfParts+1):
            yValue = polynomial.subs(x, i) % modulus
            shares.append( "%s-%s" % (str(i), str(yValue)) )

        return shares

def splitSecret(secret, numberOfParts, threshold):

    #Gets an array of the bytes of the secret, in decimal
    secretInDecimalBytes = list(bytearray(secret, "utf-8"))
    #secretInBinary = map(ord,secret.encode('utf8'))

    print ""
    print "secretInDecimalBytes: %s" % (secretInDecimalBytes)
    print "numberOfParts: %s" % (numberOfParts)
    print "threshold: %s" % (threshold)

    print ""

    #Makes a list that individual shares are appended to
    listOfShares = [(str(i) + "-") for i in range(1, numberOfParts+1)]

    #Uses the byte form of the secret
    #Gets 'numberOfParts' shares for each byte in the secret
    for byte in secretInDecimalBytes:

        #Gets the shares for this portion of the secret
        individualShare = getShares(byte, numberOfParts, threshold)

        print "individualShare: %s" % (individualShare)

        for i in range(0, numberOfParts):

            #Gets the number from the individual share and makes it 3 digits long
            decimalShare = individualShare[i].split("-")[1].zfill(3)

            #Appends to the list of shares
            listOfShares[i]= listOfShares[i] + decimalShare
            print "decimalShare: %s" % (decimalShare)

        print "##########"

    return listOfShares

def getSharesFromFrontendSecret(secret, numberOfParts, threshold):

    formattedSecret = secret

    combinedShares = splitSecret(formattedSecret, numberOfParts, threshold)

    return combinedShares

def reconstructSecretFromShares(combinedShares):

    for share in combinedShares:
        splitShare = share.split("-")
        xValue = int(splitShare[0])
        yValues = []

        yValuesString = splitShare[1]
        for i in range(0, len(yValuesString), 3):
            yValues.append(yValuesString[i:i+3])

        print ""
        print "xValue: %s" % (xValue)
        print "yValues: %s" % (yValues)

    return "Not done yet"

    allSharesForXValues = {}
    for i in overallSharesCombined:
        splitShare = i[0].split("-")
        xValue = int(splitShare[1])
        yValue = int(splitShare[2])
        shareValueInBinary = bin(yValue)[2:]
        lengthOfShareValueInBinary = len(shareValueInBinary)
        zerosToAddToShareValue = 0
        if ((lengthOfShareValueInBinary%primeBits) != 0):
            zerosToAddToShareValue = ( primeBits - (lengthOfShareValueInBinary%primeBits) )
        primeBitsLengthShareValue = zerosToAddToShareValue*"0" + shareValueInBinary
        #print "primeBitsLengthShareValue:", primeBitsLengthShareValue
        #print "lengthOfPrimeBitsLengthShareValueInBinary:", len(primeBitsLengthShareValue)

        print ""
        print "xValue:", xValue
        print "yValue:", yValue
        #print "shareValueInBinary:", shareValueInBinary

        print "primeBitsLengthShareValue:", primeBitsLengthShareValue
        print "lengthOfPrimeBitsLengthShareValueInBinary:", len(primeBitsLengthShareValue)
        for j in range(0, len(primeBitsLengthShareValue), primeBits):
            individualShareInBinary = primeBitsLengthShareValue[j:j+primeBits]
            individualShareInDecimal = int(individualShareInBinary, 2)
            allSharesForXValues[xValue] = allSharesForXValues.get(xValue, []) + ["%s-%s" % (str(xValue), str(individualShareInDecimal))]
            print "individualShareInBinary:", individualShareInBinary
            print "individualShareInDecimal:", individualShareInDecimal
        print "allSharesForXValues[%s]: %s" % (xValue, allSharesForXValues[xValue])
    print "allSharesForXValues:", allSharesForXValues
    print ""

    sharesForEachPrimeBitsLength = {}
    xValues = sorted(allSharesForXValues.keys())
    for i in range(0, len(allSharesForXValues[xValues[0]])):
        for j in xValues:
            sharesForEachPrimeBitsLength[i] = sharesForEachPrimeBitsLength.get(i, []) + [allSharesForXValues[j][i]]
        print "sharesForEachPrimeBitsLength[%s]: %s" % (i, sharesForEachPrimeBitsLength[i])
    print "sharesForEachPrimeBitsLength:", sharesForEachPrimeBitsLength

    #Converts coordinates to points to polynomial to decimal codepoints (from constant coefficient) to binary codepoints
    prependedCodepoints = ""
    listOfSecretsInDecimal = []
    modulus = (2**primeBits)
    numberOfBitsSections = len(sharesForEachPrimeBitsLength)
    print "numberOfBitsSections:", numberOfBitsSections
    for i in sharesForEachPrimeBitsLength:
        coordinates = []
        for j in range(0, len(sharesForEachPrimeBitsLength[0])):
            splitShare = sharesForEachPrimeBitsLength[i][j].split("-")
            coordinateX = int(splitShare[0])
            coordinateY = int(splitShare[1])
            coordinates.append([coordinateX, coordinateY])
        print ""
        print "#########################"
        print "sharesForEachPrimeBitsLength[i]:", sharesForEachPrimeBitsLength[i]
        print "coordinates:", coordinates

        x = sympy.symbols('x')
        polynomial = getPolynomial(coordinates)
        print "polynomial for bits:", polynomial

        coefficients = sympy.Poly(polynomial, x).coeffs()
        lastCoefficient = coefficients[len(coefficients)-1]
        primeBitsSecret = 0
        if (len(coefficients) != 1):
            primeBitsSecret = (lastCoefficient) % modulus

        print "primeBitsSecret after modding:", primeBitsSecret
        print "type(primeBitsSecret) after modding:", type(primeBitsSecret)

        if (type(primeBitsSecret) not in [int, sympy.numbers.Integer, sympy.numbers.One]):
            primeBitsSecret = 0

        listOfSecretsInDecimal.append(primeBitsSecret)

        #Pads primeBitsSecretInBinary to the required number of digits; if not the last section, then _primeBits_ length, else the number of digits required to make codepointsInBinary % 16 = 0:
        #codepointsInBinary = prependedCodepoints - padLength - zerosPrepended, zerosToAdd = normal no. of zeros - length of current primeBitsSecretInBinary
        primeBitsSecretInBinary = bin(primeBitsSecret)[2:]
        paddedPrimeBitsSecretInBinary = primeBitsSecretInBinary
        if (( len(primeBitsSecretInBinary) % primeBits ) != 0):
            zerosToAddToPrimeBitsSecret = 0
            if ((i+1) != numberOfBitsSections):
                zerosToAddToPrimeBitsSecret = ( primeBits - (len(primeBitsSecretInBinary) % primeBits) )
            else:
                zerosPrepended = int(prependedCodepoints[0:16], 2)
                lengthToMod = (len(prependedCodepoints) - 16 - zerosPrepended)
                zerosToAddToPrimeBitsSecret = (( 16 - (lengthToMod % 16) ) - len(primeBitsSecretInBinary))
            paddedPrimeBitsSecretInBinary = zerosToAddToPrimeBitsSecret*"0" + primeBitsSecretInBinary

        print "i:", i
        print "coefficients for bits:", coefficients
        print "lastCoefficient:", lastCoefficient
        print "type(lastCoefficient):", type(lastCoefficient)
        print "primeBitsSecret:", primeBitsSecret
        print "type(primeBitsSecret):", type(primeBitsSecret)
        print "primeBitsSecretInBinary:", primeBitsSecretInBinary
        print "paddedPrimeBitsSecretInBinary:", paddedPrimeBitsSecretInBinary

        print "#########################"
        prependedCodepoints = prependedCodepoints + paddedPrimeBitsSecretInBinary
    print ""
    print "listOfSecretsInDecimal:", listOfSecretsInDecimal
    print "prependedCodepoints:", prependedCodepoints

    zerosPrepended = int(prependedCodepoints[0:16], 2)
    paddedCodepoints = prependedCodepoints[16:]
    codepointsInBinary = paddedCodepoints[zerosPrepended:]
    print "zerosPrepended:", zerosPrepended
    print "zerosToAddInBinary:", prependedCodepoints[0:16]
    print "paddedCodepoints:", paddedCodepoints
    print "codepointsInBinary:", codepointsInBinary

    #Converts binary codepoints to unicode codepoints to UTF-8 string
    secret = ""
    for i in range(0, len(codepointsInBinary), 16):
        binaryChars = codepointsInBinary[i:i+16]
        unicodeCodepoint = int(binaryChars, 2)
        strChar = unichr(unicodeCodepoint).encode("utf-8")
        if (len(strChar) != 1):
            strChar = strChar[len(strChar)-1]
        secret = secret + strChar

    return secret
