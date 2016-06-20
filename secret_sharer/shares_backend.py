import sympy
import math

import polynomial_backend

def splitSecret(secret, numberOfParts, threshold):

    #Gets an array of the bytes of the secret, in decimal
    secretInDecimalBytes = list(bytearray(secret))#, "utf-8"))
    #secretInDecimalBytes = map(ord,secret.encode('utf8'))

    #Makes a list that individual shares are appended to
    listOfShares = [(str(i) + "-") for i in range(1, numberOfParts+1)]

    #Uses the byte form of the secret
    #Gets 'numberOfParts' shares for each byte in the secret
    for byte in secretInDecimalBytes:

        #Gets the shares for this portion of the secret
        individualShare = polynomial_backend.getShares(byte, numberOfParts, threshold)

        for i in range(0, numberOfParts):

            #Gets the number from the individual share and makes it 3 digits long
            decimalShare = individualShare[i].split("-")[1].zfill(3)

            #Appends to the list of shares
            listOfShares[i]= listOfShares[i] + decimalShare

    return listOfShares

def reconstructSecretFromShares(combinedShares):

    print ""

    unmatchedCoordinatesList = []

    for share in combinedShares:
        splitShare = share.split("-")
        xValue = int(splitShare[0])
        yValues = []

        yValuesString = splitShare[1]
        for i in range(0, len(yValuesString), 3):
            yValues.append(int(yValuesString[i:i+3]))

        coordinates = [[xValue, yValue] for yValue in yValues]
        unmatchedCoordinatesList.append(coordinates)

    numberOfPolysNeeded = len(unmatchedCoordinatesList[0])
    matchedCoordinatesList = [[]] * numberOfPolysNeeded

    for i in unmatchedCoordinatesList:
        count = 0
        for j in i:
            matchedCoordinatesList[count] = matchedCoordinatesList[count] + [j]
            count = count + 1

    constantsList = []
    for coordinateSet in matchedCoordinatesList:
        x = sympy.symbols('x')
        constant = polynomial_backend.getPolynomialCoefficient(coordinateSet)
        constantsList.append(constant)

    conArr = bytearray(constantsList)
    secret = conArr.decode('utf8')
    return secret

def getSharesFromFrontendSecret(secret, numberOfParts, threshold):

    formattedSecret = secret

    combinedShares = splitSecret(formattedSecret, numberOfParts, threshold)

    return combinedShares
