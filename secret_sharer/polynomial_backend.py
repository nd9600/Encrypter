import sympy
import random

#Max value of each secret (since they are bytes is 255)
#269 is prime and bigger than 255, so we can use it
MODULUS = 269

def insistentFunction(numberOfParts, threshold):
    booleanValue = True
    try:
        if ((type(threshold) is not int) or (threshold > numberOfParts)):
            raise Exception, "%s is not a valid integer" % (threshold)
    except Exception as e:
        print e
        booleanValue = False

    return booleanValue

def getPolynomialCoefficient(coordinates):
    x, y, a = sympy.symbols('x, y, a')

    numberOfPoints = len(coordinates)
    setOfPoints = {}

    #Creates a dictionary setOfPoints of the form
    #  {0: [[1,1], [2,0], [3,0], [4,0]], 1: [[1,0], [2,8], [3,0], [4,0]], 2: ...}
    for i in range(0, numberOfPoints):
        for j in range(0, numberOfPoints):
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
        #print "setOfEquations[{0}]: {1}".format(i, setOfEquations[i])

        allZeroBoolean = True
        for j in range(0, len(setOfPoints[i]) ):
            if (setOfPoints[i][j][1] != 0):
                allZeroBoolean = False
                break
            else:
                continue

        if (allZeroBoolean):
            setOfSubbedEquations[i] = 0 * x
        else:
            #Subs in the non-zero coordinates
            unSubbedEquation = sympy.Eq(y, setOfEquations[i])
            subbedEquation = unSubbedEquation.subs([ (y, setOfPoints[i][i][1]), (x, setOfPoints[i][i][0]) ] )
            #Solves each polynomial to find the constant a, and subs into the final set
            solutionForA = sympy.solve(subbedEquation, a)[0]
            setOfSubbedEquations[i] = setOfEquations[i].subs(a, solutionForA)
            #print "solutionForA:", solutionForA

        #print "setOfSubbedEquations[{0}]: {1}".format(i, setOfSubbedEquations[i])

    summedEquations = sum(setOfSubbedEquations.itervalues())
    #print ""
    #print "setOfSubbedEquations:", setOfSubbedEquations
    #print "summedEquations:", summedEquations

    #Sums each polynomial and expands it into a simpler form
    finalPolynomial = sympy.expand(summedEquations)

    coefficients = sympy.Poly(finalPolynomial, x).coeffs()
    constant = coefficients[len(coefficients) - 1]
    moddedConstant = constant % MODULUS

    print "finalPolynomial:", finalPolynomial
    return moddedConstant

def getShares(secret, numberOfParts, threshold):
    rng = random.SystemRandom()
    randomNumbers = {}

    #Picks _threshold-1_ random numbers
    for i in range(1, threshold):
        randomNumbers[i] = rng.randint(1, MODULUS)

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
        x = sympy.symbols('x')
        polynomial = secret
        for i in range(1, threshold):
            polynomial = polynomial + (randomNumbers[i])*x**i

        #Picks _numberOfParts_ number of points in order of x-value from the polynomial, and returns them
        shares = []
        for i in range(1, numberOfParts+1):
            yValue = polynomial.subs(x, i) % MODULUS
            shares.append( "%s-%s" % (str(i), str(yValue)) )

        return shares
