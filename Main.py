import re
import logging
import pandas as pd

#TODO:
#   Tkinter front
#   Fix splitting issue in txttoarray
#   Pandas array

#-------------------------------Imports-------------------------------
#-------------------------------GlobalVars----------------------------
DEBUGMODE = True
#-------------------------------GlobalVars----------------------------
#-------------------------------Logging-------------------------------

def loggingSetup(): #Setup needed logging settings
    if DEBUGMODE:
        logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="a", format='%(asctime)s :: %(name)s :: %(levelname)-8s :: %(message)s')
        logging.critical("\n\n\nNew session, DEBUG=ON")
    elif not DEBUGMODE:
        logging.basicConfig(level=logging.WARNING, filename="log.log", filemode="a", format='%(asctime)s :: %(name)s :: %(levelname)-8s :: %(message)s')
        logging.critical("\n\n\nNew session, DEBUG=OFF".format)
    else:
        logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="a", format='%(asctime)s :: %(name)s :: %(levelname)-8s :: %(message)s')
        logging.critical("\n\n\nNew session, DEBUG=ERROR")
        logging.warning("Logging not correctly initiated via DEBUGMODE variable... Somehow?")
        logging.warning("Restoring default level=DEBUG config")
    return

#-------------------------------Logging-------------------------------
#-------------------------------Main----------------------------------

def main():
    mode = selectMode()                                                                         #Selects what mode to use (most likely will be what manifacturer)
    DataArray = txtToArray("Source\PickPlaceforBasismodule.txt", mode)
    # print(arrayToPandasDF(DataArray, mode))
    return

#-------------------------------Main----------------------------------
#-------------------------------SeconderyFunctions--------------------

def selectMode():
    inputModeCorrect = False
    while not inputModeCorrect:
        inputMode = input("Select the mode you need (DE/AA/AB/AC/AD)").upper()
        print("You have selected: '{}'".format(inputMode))
        if inputMode in ["DE"]:
            inputModeCorrect = True
        else:
            print("Invalid input, try again")

    
    
    return inputMode

def fromMiltoMM(Mil):
    return Mil/39.3700787

def fromMMtoMil(MM):
    return MM*39.3700787

def txtToArray(textfilePath, mode):
    ReturnArray = []
    f = open(textfilePath, "r")

    FRead = f.read().replace("\n", "|").replace("\r", "|")                                      #Replace every newline with a "|" to be split there
    array = FRead.split("|")                                                                    #Splits with every new line

    for i in array:                                                                             #used to strip the trailing whitespaces and sorts them to item level
        i.strip()
        ReturnArray.append(re.split(r'\s{2,}', i))
    
    for i in ReturnArray:                                                                       #remove unneeded additions to array
        while "" in i:
            i.remove("")
        while [] in i:
            i.remove([])

    while [] in ReturnArray:                                                                    #remove unneeded additions to array
        ReturnArray.remove([])

    if mode == "DE":
        for i in ReturnArray[1:]:
            hold = i[-1]
            i.remove(hold)
            holdnew = re.split(r"[0-9]\.[0-9][0-9] ", hold, maxsplit=1)
            print(holdnew)
            print(hold)
    return ReturnArray

def arrayToPandasDF(DataArray, mode):
    headers = DataArray[0]
    data = DataArray[1:]

    if mode == "DE":
        headers = ["Designator", "Footprint", "Mid X", "Mid Y", "Ref X", "Ref Y", "Pad X", "Pad Y", "TB", "Rotation", "Comment"]

    DF = pd.DataFrame(data, columns = headers)
    return DF


#-------------------------------SeconderyFunctions--------------------
#-------------------------------__Main__------------------------------
if __name__ == "__main__":
    loggingSetup()                                                                              #Set up all logging stuff away from the main code for readability
    main()
    exit(0)                                                                                     #When program is done, leave with exitcode 0 (no errors)
else:
    #TODO, log error (can't be run as a module)
    exit(1)