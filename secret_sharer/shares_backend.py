import sympy
import random
import math

from utils import *

def getShares(secret, numberOfParts, threshold, primeBits):
    rng = random.SystemRandom()
    randomNumbers = {}
    modulus = (2**primeBits)

    #Picks _threshold-1_ random numbers
    for i in range(0, threshold):
        randomNumbers[i] = rng.randint(1, modulus)

    print ""
    print "secret:", secret
    print "numberOfParts:", numberOfParts
    print "randomNumbers:", randomNumbers

    #If the secret is 0, we just return zero for the shares
    if (secret == 0):
        shares = []
        for i in range(1, numberOfParts+1):
            shares.append(["%s-%s" % (str(i), str(0))])

        return shares

    else:
        #Creates a polynomial of degree _threshold-1_, where x0 = secret and every other x is a term with a random coefficient
        #and increasing power of x
        x, y = sympy.symbols('x, y')
        polynomial = secret
        for i in range(0, threshold):
            polynomial = polynomial + (randomNumbers[i])*x**i
        print ""
        print "polynomial:", polynomial

        #Picks _numberOfParts_ number of points in order of x-value from the polynomial, and returns them
        shares = []
        for i in range(1, numberOfParts+1):
            yValue = polynomial.subs(x, i) % modulus
            shares.append(["%s-%s" % (str(i), str(yValue))])

        return shares

def splitSecret(secret, numberOfParts, threshold, primeBits = 8, padLength = 0):
    minimumPrimeBitsForNumberOfShares = int(math.ceil(math.log(numberOfParts, 2) + 1))

    #Converts secret to unicode codepoints to binary to decimal secret
    codepointsInBinary = ""
    for c in secret:
        unicodeCodepoint = ord(c)
        codepointInBinary = bin(unicodeCodepoint)[2:]
        sixteenBitCodepoint = (16-len(codepointInBinary))*"0" + codepointInBinary
        codepointsInBinary =  codepointsInBinary + sixteenBitCodepoint

    print ""
    print "codepointsInBinary:", codepointsInBinary

    #Pads overall codepoints by _padLength_ number of zeros
    lengthOfCodepoints = len(codepointsInBinary)
    zerosToAdd = 0
    if ( (padLength != 0) and ( (lengthOfCodepoints%padLength) != 0 ) ):
        zerosToAdd = ( padLength - (lengthOfCodepoints%padLength) )
    paddedCodepoints = zerosToAdd*"0" + codepointsInBinary

    #Pads zerosToAdd to a 16 bit integer, and prepends it to the padded codepoints
    zerosToAddInBinary = bin(zerosToAdd)[2:]
    lengthOfZerosToAddInBinary = len(zerosToAddInBinary)
    zerosToAddToZerosToAdd = 0
    if (lengthOfZerosToAddInBinary%16) != 0:
        zerosToAddToZerosToAdd = ( 16 - (lengthOfZerosToAddInBinary%16) )
    paddedZerosToAddInBinaryInBinary = zerosToAddToZerosToAdd*"0" + zerosToAddInBinary
    prependedCodepoints = paddedZerosToAddInBinaryInBinary + paddedCodepoints

    #Calculates new numberOfSections until _primeBits_ doesn't change
    newPrimeBits1 = 0
    newPrimeBits2 = primeBits
    numberOfSections = 0
    while (newPrimeBits1 != newPrimeBits2):
        newPrimeBits1 = newPrimeBits2
        numberOfSections = len(prependedCodepoints)/newPrimeBits1

        minimumPrimeBitsForNumberOfSections = int(math.ceil(math.log(numberOfSections*2, 2) + 1))
        minimumPrimeBits = max(minimumPrimeBitsForNumberOfSections, minimumPrimeBitsForNumberOfShares)
        newPrimeBits2 = max(primeBits, minimumPrimeBits)
    primeBits = newPrimeBits2
    newNumberOfSections = len(prependedCodepoints)/primeBits

    print ""
    print "zerosToAdd:", zerosToAdd
    print "zerosToAddInBinary:", zerosToAddInBinary
    print "zerosToAddToZerosToAdd:", zerosToAddToZerosToAdd
    print "paddedZerosToAddInBinaryInBinary:", paddedZerosToAddInBinaryInBinary
    print "len(paddedZerosToAddInBinaryInBinary):", len(paddedZerosToAddInBinaryInBinary)
    print "paddedCodepoints:", paddedCodepoints
    print "prependedCodepoints:", prependedCodepoints
    print "len(prependedCodepoints):", len(prependedCodepoints)
    print "number of newPrimeBits sections:", newNumberOfSections
    print "padLength: %s bits" % (padLength)
    print "primeBits: %s bits" % (primeBits)
    print "numberOfParts: %s" % (numberOfParts)
    print "threshold: %s" % (threshold)

    #Converts binary codepoints to decimal, uses sections of _primeBits_ length as secrets
    #and converts them to polynomial to points in polynomial to individual shares,
    #pads share y-value to _primeBits_ length, combines into y-value, converts to decimal,
    #to make overall shares of the form primeBits-x- collection of individual shares
    overallSharesDictionary = {}
    count = 0
    listOfSecretsInDecimal = []
    sharesForEachPrimeBitsLength = {}
    for i in range(0, len(prependedCodepoints), primeBits):
        count = i/primeBits
        bits = prependedCodepoints[i:i+primeBits]
        decimalBits = int(bits, 2)
        listOfSecretsInDecimal.append(decimalBits)

        #print ""
        #print "%sth %s bits: %s" % (count, primeBits , bits)
        #print "%sth %s bits in decimal: %s" % (count, primeBits , decimalBits)
        individualShare = getShares(decimalBits, numberOfParts, threshold, primeBits)
        sharesForEachPrimeBitsLength[count] = [individualShare[0][0], individualShare[1][0]]
        print "bits:", bits
        print "decimalBits:", decimalBits
        print "individualShare:", individualShare
        for j in range(1, numberOfParts+1):
            overallSharesDictionary[j] = overallSharesDictionary.get(j, []) + individualShare[j-1]
    print ""
    print "listOfSecretsInDecimal:", listOfSecretsInDecimal

    for i in range(0, len(sharesForEachPrimeBitsLength)):
        print "sharesForEachPrimeBitsLength[%s]: %s" % (i, sharesForEachPrimeBitsLength[i])

    print "sharesForEachPrimeBitsLength:", sharesForEachPrimeBitsLength
    #print "overallSharesDictionary:", overallSharesDictionary
    #print "count:", count

    print ""
    overallSharesCombined = []
    for i in overallSharesDictionary:
        yValue = ""
        for j in overallSharesDictionary[i]:
            splitShare = j.split("-")
            shareValue = int(splitShare[1])
            shareValueInBinary = bin(shareValue)[2:]
            lengthOfShareValueInBinary = len(shareValueInBinary)

            zerosToAddToShareValue = 0
            if (lengthOfShareValueInBinary%primeBits) != 0:
                zerosToAddToShareValue = ( primeBits - (lengthOfShareValueInBinary%primeBits) )
            primeBitsLengthShareValue = zerosToAddToShareValue*"0" + shareValueInBinary
            yValue = yValue + primeBitsLengthShareValue
        #print "Binary yValue:", yValue
        yValue = int(yValue, 2)
        ithShare = ["%s-%s-%s" % (str(primeBits), str(i), str(yValue))]
        #print "Decimal yValue:", yValue
        #print "%sth share: %s" % (i, ithShare)
        overallSharesCombined = overallSharesCombined + [ithShare]
    #print "overallSharesCombined:", overallSharesCombined

    return overallSharesCombined

def getOverallShares():
    print ""
    print "#####"
    secret = raw_input("Secret: ")
    codepointsInBinary = ""
    padLength = 0
    primeBits = 8

    print ""

    numberOfParts = input("Number of parts: ")
    thresholdBooleanValue = False
    threshold = 0
    while not thresholdBooleanValue:
        threshold = input("Threshold: ")
        thresholdBooleanValue = insistentFunction(numberOfParts, threshold)

    changePadLength = raw_input("Change pad length (default 0 bits) [y/N]: ")
    if (changePadLength == "y"):
        padLength = input("New pad length ie padLength = 2^bits (max 16): ")
    if (padLength != 0):
        padLength = 2**padLength

    if (padLength > 65536):
       padLength = 65536

    changePrimeBits = raw_input("Change prime bits - ie prime = 2^bits (default %s) [y/N]: " % (primeBits))
    if (changePrimeBits == "y"):
        primeBits = input("New prime bits: ")

    overallSharesCombined = splitSecret(secret, numberOfParts, threshold, primeBits, padLength)

    print ""
    print "Overall shares:"
    for i in overallSharesCombined:
        print str(i)[2:][:-2]
    print "#####"

def reconstructSecretFromShares(overallSharesCombined):
    print "overallSharesCombined:", overallSharesCombined
    print "overallSharesCombined[0]:", overallSharesCombined[0]
    print "overallSharesCombined[0][0]:", overallSharesCombined[0][0]
    primeBits = int(str(overallSharesCombined[0][0]).split("-")[0])
    print "primeBits:", primeBits

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

def readShares():
    #Reads in shares and puts in a single list
    print ""
    print "#####"
    overallSharesCombined = []
    share = raw_input("Share (-1 to finish): ")
    while (share != "-1"):
        overallSharesCombined = overallSharesCombined + [[share]]
        share = raw_input("Share (-1 to finish): ")
    print ""
    print "overallSharesCombined:", overallSharesCombined

    secret = reconstructSecretFromShares(overallSharesCombined)
    print "secret:", secret
    print "#####"
