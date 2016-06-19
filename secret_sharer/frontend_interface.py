from shares_backend import *

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
            getOverallShares()
        elif (choice == "2"):
            readShares()
        else:
            print "Not a valid choice. Try again"

        choice = getChoice()
        print "#####"
        print ""

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

def readShares():
    #Reads in shares and puts in a single list
    print ""
    print "#####"
    overallSharesCombined = []
    share = raw_input("Share (q to finish): ")
    while (share != "q"):
        overallSharesCombined = overallSharesCombined + [[share]]
        share = raw_input("Share (q to finish): ")
    print ""
    print "overallSharesCombined:", overallSharesCombined

    secret = reconstructSecretFromShares(overallSharesCombined)
    print "secret:", secret
    print "#####"

if __name__ == "__main__":
    menu()
