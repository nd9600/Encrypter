from sympy import symbols, Eq, Basic, solve, expand, Poly#, GF
from sys import maxint
from random import SystemRandom

def insistentFunction(numberOfParts, threshold):
    booleanValue = True
    try:
        if ((type(threshold) is not int) or (threshold > numberOfParts)):
            raise Exception, "%s is not a valid integer" % (threshold)
    except Exception as e:
        print e
        booleanValue = False
        
    return booleanValue
    
def getShares(secret, numberOfParts, threshold):
    rng = SystemRandom()
    randomNumbers = {}
    
    #Picks _threshold-1_ random numbers
    for i in range(1, threshold):
        randomNumbers[i] = rng.randint(0, maxint)  
    print "randomNumbers:", randomNumbers
    
    #Creates a polynomial of degree _threshold-1_, where x0 = secret and every other x is a term with a random coefficient
    #and increasing power of x
    x, y = symbols('x, y')
    polynomial = secret
    for i in range(1, threshold):
        polynomial = polynomial + (randomNumbers[i])*x**i   
    print "polynomial:", polynomial
    
    #Picks _threshold_ number of points in order of x-value from the polynomial, and returns them
    shares = []
    for i in range(1, numberOfParts+1):
        yValue = polynomial.subs(x, i)
        shares.append(["%s-%s" % (str(i), str(yValue))])
        
    return shares
    
def splitSecret():
    print ""
    print "#####"
    secret = raw_input("Secret: ")
    codepointsInBinary = ""
    
    #Converts secret to unicode codepoints to binary to decimal secret
    for c in secret:
        unicodeCodepoint = ord(c)
        codepointInBinary = bin(unicodeCodepoint)[2:]
        paddedCodepointInBinary = (16-len(codepointInBinary))*"0" + codepointInBinary
        codepointsInBinary = codepointsInBinary + paddedCodepointInBinary
    codepointsInDecimal = int(codepointsInBinary, 2)
    print "codepointsInBinary:", codepointsInBinary
    print "codepointsInDecimal:", codepointsInDecimal
    
    numberOfParts = input("Number of parts: ")
    thresholdBooleanValue = False
    threshold = 0
    while not thresholdBooleanValue:
        threshold = input("Threshold: ")
        thresholdBooleanValue = insistentFunction(numberOfParts, threshold)
    
    #Converts decimal to polynomial to points in polynomial to shares
    print ""
    shares = getShares(codepointsInDecimal, numberOfParts, threshold)
    print "shares:", shares
    print "#####"
    
def getPolynomial(coordinates):
    x, y, a = symbols('x, y, a')

    numberOfPoints = len(coordinates)
    setOfPoints = {}

    #Creates a dictionary setOfPoints of the form
    #  {0: [[1,1], [2,0], [3,0], [4,0]], 1: [[1,0], [2,8], [3,0], [4,0]], 2: ...}
    #for i in range(0,numberOfPoints):
    #	setOfPoints[i] = [ [coordinates[i][0], coordinates[i][1]] ]
    #	for j in range(0,numberOfPoints):
    #		if (j != i):
    #			setOfPoints[i].append([coordinates[j][0], 0])	
    #	setOfPoints[i] = sorted(setOfPoints[i], key=lambda x: x[0])
    for i in range(0,numberOfPoints):
        for j in range(0,numberOfPoints):
            if (j == i):
                if i in setOfPoints:
                    setOfPoints[i].append( [coordinates[i][0], coordinates[i][1]] )
                else:
                    setOfPoints[i] = [ [coordinates[i][0], coordinates[i][1]] ]
            elif (j != i):
                if i in setOfPoints:
                    setOfPoints[i].append([coordinates[j][0], 0])
                else:
                    setOfPoints[i] = [ [coordinates[j][0], 0] ]

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
        
        print ""
        print "setOfPoints[{0}]: {1}".format(i, setOfPoints[i])
        
        #Subs in the non-zero coordinates
        unSubbedEquation = Eq(y, setOfEquations[i])
        subbedEquation = unSubbedEquation.subs([ (y, setOfPoints[i][i][1]), (x, setOfPoints[i][i][0]) ] )
        #Solves each polynomial to find the constant a, and subs into the final set
        solutionForA = solve(subbedEquation, a)[0]
        setOfSubbedEquations[i] = setOfEquations[i].subs(a, solutionForA)
        print "setOfEquations[{0}]: {1}".format(i, setOfEquations[i]) 
        
        print "setOfSubbedEquations[{0}]: {1}".format(i, setOfSubbedEquations[i])

    summedEquations = sum(setOfSubbedEquations.itervalues())
    print ""
    print "setOfSubbedEquations:", setOfSubbedEquations
    print "summedEquations:", summedEquations
    
    #Sums each polynomial and expands it into a simpler form
    finalPolynomial = expand(summedEquations) 
    return finalPolynomial

def reconstructSecret():   
    coordinates = []
    
    #Converts shares to coordinates
    print ""
    print "#####"
    share = raw_input("Share (-1 to finish): ")
    while (share != "-1"):
        splitShare = share.split("-")
        coordinateX = int(splitShare[0])
        coordinateY = int(splitShare[1])        
        coordinates.append([coordinateX, coordinateY])
        share = raw_input("Share (-1 to finish): ")
    print "coordinates:", coordinates
    
    #Converts coordinates to points to polynomial to decimal codepoints (from constant coefficient) to binary codepoints
    x = symbols('x')
    polynomial = getPolynomial(coordinates)
    coefficients = Poly(polynomial, x).coeffs()
    
    codepointsInDecimal = coefficients[len(coefficients)-1]
    codepointsInBinary = bin(codepointsInDecimal)[2:]
    print ""
    print "polynomial:", polynomial
    print "coefficients:", coefficients
    print "codepointsInDecimal:", codepointsInDecimal
    print "codepointsInBinary:", codepointsInBinary
    
    #Pads binary codepoints to required length - next multiple of 16
    length = len(codepointsInBinary)
    zerosToAdd = ( 16 - (length%16) )
    paddedCodepoints = zerosToAdd*"0" + str(codepointsInBinary)
    print "paddedCodepoints:", paddedCodepoints
    
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