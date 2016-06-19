import sympy

def insistentFunction(numberOfParts, threshold):
    booleanValue = True
    try:
        if ((type(threshold) is not int) or (threshold > numberOfParts)):
            raise Exception, "%s is not a valid integer" % (threshold)
    except Exception as e:
        print e
        booleanValue = False

    return booleanValue

def getPolynomial(coordinates):
    x, y, a = sympy.symbols('x, y, a')

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
    return finalPolynomial
