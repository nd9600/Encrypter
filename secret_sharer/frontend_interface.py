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
    #Reads in secret and gets shares

    print ""
    print "#####"
    secret = raw_input("Secret: ")

    print ""

    numberOfParts = input("Total number of parts: ")
    thresholdBooleanValue = False
    threshold = 0
    while not thresholdBooleanValue:
        threshold = input("Threshold number of parts: ")
        thresholdBooleanValue = insistentFunction(numberOfParts, threshold)

    overallSharesCombined = splitSecret(secret, numberOfParts, threshold)

    print ""
    print "Overall shares:"
    for i in overallSharesCombined:
        print str(i)[2:][:-2]
    print "#####"

def readShares():
    #Reads in shares from user and prints out secret
    
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
