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

if __name__ == "__main__":
    menu()
