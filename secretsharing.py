from sympy import symbols, Eq, Basic, solve, expand, Poly
from random import SystemRandom
primeBits = 8

def insistentFunction(numberOfParts, threshold):
    booleanValue = True
    try:
        if ((type(threshold) is not int) or (threshold > numberOfParts) or (threshold > primeBits)):
            raise Exception, "%s is not a valid integer" % (threshold)
    except Exception as e:
        print e
        booleanValue = False
        
    return booleanValue
    
def getShares(secret, numberOfParts, threshold):
    rng = SystemRandom()
    randomNumbers = {}
    modulus = (2**primeBits)
    
    #Picks _threshold-1_ random numbers
    for i in range(1, threshold):
        randomNumbers[i] = rng.randint(0, modulus)  
    #print "randomNumbers:", randomNumbers
    
    #Creates a polynomial of degree _threshold-1_, where x0 = secret and every other x is a term with a random coefficient
    #and increasing power of x
    x, y = symbols('x, y')
    polynomial = secret
    for i in range(1, threshold):
        polynomial = polynomial + (randomNumbers[i])*x**i
    print ""
    print "polynomial:", polynomial
    
    #Picks _numberOfParts_ number of points in order of x-value from the polynomial, and returns them
    shares = []
    for i in range(1, numberOfParts+1):
        yValue = polynomial.subs(x, i) % modulus
        shares.append(["%s-%s" % (str(i), str(yValue))])
        
    return shares
    
def splitSecret():
    print ""
    print "#####"
    secret = raw_input("Secret: ")
    codepointsInBinary = ""
    padLength = 64
    global primeBits
    
    changePadLength = raw_input("Change pad length (default 64, max 1024 bits) [y/N]: ")
    if (changePadLength == "y"):
        padLength = input("New pad length (in bits): ")
        
    if (padLength > 1024):
       padLength = 1024

    changePrimeBits = raw_input("Change prime bits - ie prime = 2^bits (default 8) [y/N]: ")
    if (changePrimeBits == "y"):
        primeBits = input("New prime bits ( >3 ): ")
        
    numberOfParts = input("Number of parts (must be less than %s): " % (2**primeBits - 1))
    thresholdBooleanValue = False
    threshold = 0
    while not thresholdBooleanValue:
        threshold = input("Threshold: ")
        thresholdBooleanValue = insistentFunction(numberOfParts, threshold)
    
    #Converts secret to unicode codepoints to binary to decimal secret
    for c in secret:
        unicodeCodepoint = ord(c)
        codepointInBinary = bin(unicodeCodepoint)[2:]
        sixteenBitCodepoint = (16-len(codepointInBinary))*"0" + codepointInBinary
        codepointsInBinary = codepointsInBinary + sixteenBitCodepoint
        
    print ""    
    print "codepointsInBinary:", codepointsInBinary
    
    #Pads overall codepoints by _padLength_ number of zeros
    lengthOfCodepoints = len(codepointsInBinary)
    zerosToAdd = 0
    if ( (padLength != 0) and ( (lengthOfCodepoints%padLength) != 0 ) ):
        zerosToAdd = ( padLength - (lengthOfCodepoints%padLength) )  
    paddedCodepoints = zerosToAdd*"0" + codepointsInBinary
    print "paddedCodepoints:  ", paddedCodepoints
    
    #Pads padLength to an 11 bit integer, and prepends it to the padded codepoints
    padLengthInBinary = bin(padLength)[2:]
    lengthOfPadLengthInBinary = len(padLengthInBinary)
    zerosToAddToPadLength = 0
    if (lengthOfPadLengthInBinary%11) != 0:
        zerosToAddToPadLength = ( 11 - (lengthOfPadLengthInBinary%11) ) 
    paddedPadLengthInBinary = zerosToAddToPadLength*"0" + padLengthInBinary
    prependedCodepoints = paddedPadLengthInBinary + paddedCodepoints
    print "paddedPadLengthInBinary:", paddedPadLengthInBinary
    print "prependedCodepoints:", prependedCodepoints

    #Converts binary codepoints to decimal, uses sections of _primeBits_ length as secrets
    #and converts them to polynomial to points in polynomial to individual shares,
    #pads share y-value to _primeBits_ length, combines into y-value, converts to decimal,
    #to make overall shares of the form primeBits-x- collection of individual shares 
    overallSharesDictionary = {}
    for i in range(0, len(prependedCodepoints), primeBits):
        count = i/primeBits
        bits = prependedCodepoints[i:i+primeBits]
        decimalBits = int(bits, 2)
        
        #print ""
        #print "%sth %s bits: %s" % (count, primeBits , bits)
        #print "%sth %s bits in decimal: %s" % (count, primeBits , decimalBits)
        individualShare = getShares(decimalBits, numberOfParts, threshold)
        print "bits:", bits
        print "decimalBits:", decimalBits
        #print "individualShareInBinary: %s, %s, %s, %s" % (bin(int(individualShare[0][0].split("-")[1]))[2:], bin(int(individualShare[1][0].split("-")[1]))[2:], bin(int(individualShare[2][0].split("-")[1]))[2:], bin(int(individualShare[3][0].split("-")[1]))[2:])
        print "individualShare:", individualShare
        for j in range(1, numberOfParts+1):
            overallSharesDictionary[j] = overallSharesDictionary.get(j, []) + individualShare[j-1]
    #print ""
    #print "overallSharesDictionary:", overallSharesDictionary
    
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
        print "Binary yValue:", yValue
        yValue = int(yValue, 2)
        ithShare = ["%s-%s-%s" % (str(primeBits), str(i), str(yValue))]
        print "Decimal yValue:", yValue
        print "%sth share: %s" % (i, ithShare)
        overallSharesCombined = overallSharesCombined + [ithShare]
    #print "overallSharesCombined:", overallSharesCombined
    
    print ""
    print "Overall shares:"
    for i in overallSharesCombined:
        print str(i)[2:][:-2]    
    print "#####"
    
def getPolynomial(coordinates):
    x, y, a = symbols('x, y, a')

    numberOfPoints = len(coordinates)
    setOfPoints = {}

    #Creates a dictionary setOfPoints of the form
    #  {0: [[1,1], [2,0], [3,0], [4,0]], 1: [[1,0], [2,8], [3,0], [4,0]], 2: ...}
    for i in range(0,numberOfPoints):
        for j in range(0,numberOfPoints):
            if (j == i):
                setOfPoints[i] = setOfPoints.get( i, [] ) + [[coordinates[i][0], coordinates[i][1]]]
            elif (j != i):
                setOfPoints[i] = setOfPoints.get( i, [] ) + [[coordinates[j][0], 0]]

    #Creates a polynomial for each of the coordinates of the previous dictionary where y is non-zero, 
    #subs in the other coordinate to find the constant a
    setOfEquations = {}
    setOfSubbedEquations = {}
    for i in range(0, len(setOfPoints)):
        #print ""
        #print "setOfPoints[{0}]: {1}".format(i, setOfPoints[i])
        
        setOfEquations[i] = a
        for j in range(0, len(setOfPoints[i]) ):
            #Constructs initial polynomial
            if (setOfPoints[i][j][1] == 0):
                setOfEquations[i] = setOfEquations[i]*(x-setOfPoints[i][j][0])
        
        #print ""
        #print "setOfPoints[{0}]: {1}".format(i, setOfPoints[i])
        
        #Subs in the non-zero coordinates
        unSubbedEquation = Eq(y, setOfEquations[i])
        subbedEquation = unSubbedEquation.subs([ (y, setOfPoints[i][i][1]), (x, setOfPoints[i][i][0]) ] )
        #Solves each polynomial to find the constant a, and subs into the final set
        solutionForA = solve(subbedEquation, a)[0]
        setOfSubbedEquations[i] = setOfEquations[i].subs(a, solutionForA)
        #print "setOfEquations[{0}]: {1}".format(i, setOfEquations[i]) 
        #print "a:", solutionForA
        #print "setOfSubbedEquations[{0}]: {1}".format(i, setOfSubbedEquations[i])

    summedEquations = sum(setOfSubbedEquations.itervalues())
    #print ""
    #print "setOfSubbedEquations:", setOfSubbedEquations
    #print "summedEquations:", summedEquations
    
    #Sums each polynomial and expands it into a simpler form
    finalPolynomial = expand(summedEquations)
    return finalPolynomial

def reconstructSecret():   
    #Reads in shares and puts in a single list
    print ""
    print "#####"
    overallSharesCombined = []
    share = raw_input("Share (-1 to finish): ")
    while (share != "-1"):
        overallSharesCombined = overallSharesCombined + [share]
        share = raw_input("Share (-1 to finish): ")
    print ""
    print "overallSharesCombined:", overallSharesCombined
    
    primeBits = int(overallSharesCombined[0].split("-")[0])
    print "primeBits:", primeBits
    allSharesForXValues = {}
    for i in overallSharesCombined:
        splitShare = i.split("-")
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
        #for j in range(0, len(shareValueInBinary), primeBits):
        #   individualShareInBinary = shareValueInBinary[j:j+primeBits]
        for j in range(0, len(primeBitsLengthShareValue), primeBits):
            individualShareInBinary = primeBitsLengthShareValue[j:j+primeBits]
            individualShareInDecimal = int(individualShareInBinary, 2)
            allSharesForXValues[xValue] = allSharesForXValues.get(xValue, []) + ["%s-%s" % (str(xValue), str(individualShareInDecimal))]
            print "individualShareInBinary:", individualShareInBinary
            print "individualShareInDecimal:", individualShareInDecimal
        print "allSharesForXValues[%s]: %s" % (xValue, allSharesForXValues[xValue])
    print "allSharesForXValues:", allSharesForXValues
    print ""
    
    #return
    
    sharesForEachPrimeBitsLength = {}
    xValues = sorted(allSharesForXValues.keys())
    for i in range(0, len(allSharesForXValues[xValues[0]])):
        for j in range(xValues[0], xValues[-1] + 1):
            #print ""
            #print "i:", i
            #print "j:", j
            #print "j-loop sharesForEachPrimeBitsLength.get(%s, []): %s" % (i, sharesForEachPrimeBitsLength.get(i, []))
            #print "j-loop [allSharesForXValues[%s][%s]]: %s" % (j, i, [allSharesForXValues[j][i]])
            sharesForEachPrimeBitsLength[i] = sharesForEachPrimeBitsLength.get(i, []) + [allSharesForXValues[j][i]]                
        print "sharesForEachPrimeBitsLength[%s]: %s" % (i, sharesForEachPrimeBitsLength[i])
    print "sharesForEachPrimeBitsLength:", sharesForEachPrimeBitsLength
    
    #return
    
    #Converts coordinates to points to polynomial to decimal codepoints (from constant coefficient) to binary codepoints
    prependedCodepoints = ""
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
        
        x = symbols('x')
        polynomial = getPolynomial(coordinates)
        print "polynomial for bits:", polynomial
        
        coefficients = Poly(polynomial, x).coeffs()
        primeBitsSecret = (coefficients[len(coefficients)-1]) % modulus
        primeBitsSecretInBinary = bin(primeBitsSecret)[2:]
        paddedPrimeBitsSecretInBinary = primeBitsSecretInBinary
        if (((i+1) != numberOfBitsSections) and (( len(primeBitsSecretInBinary) % primeBits ) != 0)):
            zerosToAddToPrimeBitsSecret = ( primeBits - (len(primeBitsSecretInBinary) % primeBits) )    
            paddedPrimeBitsSecretInBinary = zerosToAddToPrimeBitsSecret*"0" + primeBitsSecretInBinary
        print "i:", i
        print "coefficients for bits:", coefficients
        print "primeBitsSecret:", primeBitsSecret
        print "primeBitsSecretInBinary:", primeBitsSecretInBinary
        print "paddedPrimeBitsSecretInBinary:", paddedPrimeBitsSecretInBinary
        
        print "#########################"
        prependedCodepoints = prependedCodepoints + paddedPrimeBitsSecretInBinary
    print "prependedCodepoints:", prependedCodepoints
    
    padLength = int(prependedCodepoints[0:11], 2)
    paddedCodepoints = prependedCodepoints[11:]
    #binaryCodepoints = paddedCodepoints[padLength:]
    print "padLength:", padLength
    print "paddedCodepoints:", paddedCodepoints
    #print "binaryCodepoints:", binaryCodepoints
    
    #return
    
    #Converts binary codepoints to unicode codepoints to UTF-8 string
    secret = ""
    for i in range(0, len(paddedCodepoints), 16):
        binaryChars = paddedCodepoints[i:i+16]
        unicodeCodepoint = int(binaryChars, 2)
        strChar = unichr(unicodeCodepoint).encode("utf-8")
        if (len(strChar) != 1):
            strChar = strChar[len(strChar)-1]
        secret = secret + strChar
    print "secret:", secret  
    print "#####"  
    
    return
    #Converts binary codepoints to decimal, uses sections of _primeBits_ length as secrets
    #and converts them to polynomial to points in polynomial to individual shares,
    #pads share y-value to _primeBits_ length, combines into y-value, converts to decimal,
    #to make overall shares of the form primeBits-x- collection of individual shares     
    
    # codePoints = coefficients[len(coefficients)-1]
    # codepointsInBinary = bin(codepointsInDecimal)[2:]
    # print ""
    # print "polynomial:", polynomial
    # print "coefficients:", coefficients
    # print "codepointsInDecimal:", codepointsInDecimal
    # print "codepointsInBinary:", codepointsInBinary
    
    # #Pads binary codepoints to required length - next multiple of 16
    # length = len(codepointsInBinary)
    # zerosToAdd = 0
    # if (length%16) != 0:
        # zerosToAdd = ( 16 - (length%16) )    
    # paddedCodepoints = zerosToAdd*"0" + str(codepointsInBinary)
    # print "paddedCodepoints:", paddedCodepoints
    
    #return
    
def getChoice():
    print ""
    print "#####"
    print "1). Split secret"
    print "2). Reconstruct secret"
    print "q). Quit"
    print ""
    choice = raw_input("Choice? ")
    return choice
    
def menu():
    choice = getChoice()
    while (choice != "q"):
        if (choice == "1"):
            splitSecret()
        elif (choice == "2"):
            reconstructSecret()
        else:
            print "Not a valid choice. Try again"

        choice = getChoice()
        print "#####"
        print ""
        
menu()