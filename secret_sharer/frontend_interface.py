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
            getCombinedShares()
        elif (choice == "2"):
            readShares()
        else:
            print "Not a valid choice. Try again"

        choice = getChoice()
        print "#####"
        print ""

def getCombinedShares():
    #Reads in secret and gets shares

    print ""
    print "#####"
    secret = raw_input("Secret: ")
    totalParts = input("Total number of parts: ")
    
    thresholdBoolean = False
    thresholdParts = 0
    while not thresholdBoolean:
        thresholdParts = input("Threshold number of parts: ")
        thresholdBoolean = insistentFunction(totalParts, thresholdParts)

    combinedShares = formatAndConvertSecret(secret, totalParts, thresholdParts)

    print ""
    print "Combined shares:"
    for share in combinedShares:
        print str(share)#[2:][:-2]
    print "#####"

def readShares():
    #Reads in shares from user and prints out secret

    print ""
    print "#####"
    combinedShares = []
    share = raw_input("Share (q to finish): ")
    while (share != "q"):
        combinedShares = combinedShares + [[share]]
        share = raw_input("Share (q to finish): ")
    print ""
    print "combinedShares:", combinedShares

    secret = reconstructSecretFromShares(combinedShares)
    print "secret:", secret
    print "#####"

if __name__ == "__main__":
    menu()
