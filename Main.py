from cgitb import text
from copy import deepcopy
import re
import logging
import pandas as pd
import tkinter as tk
from tkinter import filedialog as FileDialog

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
    global mode
    window = tkinter_SetupWindow()
    mode = selectMode()                                                                         #Selects what mode to use (most likely will be what manifacturer)
    DataArray = txtToArray("Source\DE_36_18v_9NL_24VDC_398x23_Rev005_Partlist_mil.txt", mode)
    DataFrame = arrayToPandasDF(DataArray, mode)
    if DEBUGMODE:
        DataFrame.to_excel(r'test.xlsx', index = False)
    DataFrame = convertUnits(DataFrame, mode)
    #print(DataFrame)
    DataFrame = strippingDF(DataFrame)
    if mode == "DE":
        for i in range(0, len(DataFrame.index)):
            namej = createComponentName(DataFrame.iloc[i,0], DataFrame.iloc[i,2], DataFrame.iloc[i,1], mode)
            #print(namej)
            DataFrame.iloc[i,1] = namej
    if mode == "F1":
        for i in range(0, len(DataFrame.index)):
            namej = createComponentName(DataFrame.iloc[i, 0], DataFrame.iloc[i,1].strip(), DataFrame.iloc[i, 10].strip(), mode)
            #print(namej)
            DataFrame.iloc[i, 10] = namej
    #print(DataFrame)
    DataFrame.to_csv("Exports/data.cvs", index=False)
    
    return

#-------------------------------Main----------------------------------
#-------------------------------SeconderyFunctions--------------------

def selectMode():
    if DEBUGMODE:
        return "DE"
    inputModeCorrect = False
    while not inputModeCorrect:
        inputMode = input("Select the mode you need (DE/AA/AB/AC/AD)").upper()
        print("You have selected: '{}'".format(inputMode))
        if inputMode in ["F1"]:
            inputModeCorrect = True
        else:
            print("Invalid input, try again")

    return inputMode

def tkinter_SetupWindow():
    global importentry, exportentry, deviderlabel
    main_window = tk.Tk()
    main_window.title("Pick & Place - File converter")

    modeframe = tk.Frame(width=50, height=50)
    modeframe.grid(row=0, column=0, padx=5, pady=5, columnspan=4)

    importbutton = tk.Button(text="Import location", command=import_file_CALLBACK)
    importbutton.grid(row=2, column=0, padx=5, pady=5)
    importentry = tk.Entry()
    importentry.grid(row=2, column=1, padx=5, pady=5)

    exportbutton = tk.Button(text="Export location", command=export_file_CALLBACK)
    exportbutton.grid(row=3, column=0, padx=5, pady=5)
    exportentry = tk.Entry()
    exportentry.grid(row=3, column=1, padx=5, pady=5)

    gobutton = tk.Button(text="Go")
    gobutton.grid(row=3, column=3)

    DBmodebutton = tk.Button(text="DB-mode", command=DEmode_CALLBACK)
    DBmodebutton.grid(row=2, column=3)

    DEmodeButton = tk.Button(text="Dutch Electro")
    DEmodeButton.grid(row=0, column=0)

    Fab2Button = tk.Button(text="Fab2")
    Fab2Button.grid(row=0, column=1)

    Fab3Button = tk.Button(text="Fab3")
    Fab3Button.grid(row=0, column=2)

    deviderlabel = tk.Label(text="------------------------------------------------------------")
    deviderlabel.grid(row=1, column=0, columnspan=5)

    main_window.mainloop()
    return


def strippingDF(DF):
    for i in range(0, len(DF.index)):
        for j in range(0, len(DF.columns)):
            DF.iloc[i,j].strip()
    return DF

def convertUnits(DF, mode):
    if mode == "DE":
        for i in range(0, len(DF.index)):
            temphold = DF.iloc[i,4]
            temphold = re.sub(r"[()]", "", temphold)
            newtemp = re.split(" ", temphold)
            #print(newtemp)
            DF.iloc[i,4] = "({:.5f} {:.5f})".format(round(fromMiltoMM(float(newtemp[0])), 5), round(fromMiltoMM(float(newtemp[1])), 5))
    
    
    if mode == "F1":
        for i in range(0, len(DF.index)):
            temphold2, temphold3, temphold4, temphold5, temphold6, temphold7 = DF.iloc[i, 2], DF.iloc[i, 3], DF.iloc[i, 4], DF.iloc[i, 5], DF.iloc[i, 6], DF.iloc[i, 7]
            if not re.search("mm\Z", temphold2):
                #print("{}\n{}\n{}\n\n".format(temphold2, temphold3, temphold4))
                temphold2 = float(re.sub(r'[^0-9.-]+', '', temphold2))
                temphold3 = float(re.sub(r'[^0-9.-]+', '', temphold3))
                temphold4 = float(re.sub(r'[^0-9.-]+', '', temphold4))
                temphold5 = float(re.sub(r'[^0-9.-]+', '', temphold5))
                temphold6 = float(re.sub(r'[^0-9.-]+', '', temphold6))
                temphold7 = float(re.sub(r'[^0-9.-]+', '', temphold7))
                #print("{}\n{}\n{}\n\n".format(temphold2, temphold3, temphold4))
                DF.iloc[i, 2] = "{:.5f}mm".format(round(fromMiltoMM(temphold2), 5))
                DF.iloc[i, 3] = "{:.5f}mm".format(round(fromMiltoMM(temphold3), 5))
                DF.iloc[i, 4] = "{:.5f}mm".format(round(fromMiltoMM(temphold4), 5))
                DF.iloc[i, 5] = "{:.5f}mm".format(round(fromMiltoMM(temphold5), 5))
                DF.iloc[i, 6] = "{:.5f}mm".format(round(fromMiltoMM(temphold6), 5))
                DF.iloc[i, 7] = "{:.5f}mm".format(round(fromMiltoMM(temphold7), 5))
    return DF



def txtToArray(textfilePath, mode):
    f = open(textfilePath, "r")
    ReturnArray = txtToArray_BOILERPLATE(f.read())

    if mode == "DE":
        ReturnArray = ReturnArray[3:]
        for i in ReturnArray:
            hold = i[2]
            holdnew = re.split(r"_DE", hold)
            #print(holdnew)
            i[2] = holdnew[0].strip()
            if len(holdnew) == 2:
                i.append(i[4])
                i[4] = i[3]
                i[3] = "_DE"
            if i[2] == "":
                lasthold = i[1].rsplit(" ", 1)
                #print(lasthold)
                i[1] = lasthold[0]
                i[2] = lasthold[1]

    if mode == "F1":
        for i in ReturnArray[1:]:
            hold = i[-1]
            i.remove(hold)
            holdnew = re.split(r"([0-9].00)", hold, maxsplit=1)
            holdnew[1] = holdnew[0] + holdnew[1]
            del holdnew[0]
            #print(holdnew)
            #print(hold)
            for j in holdnew:
                i.append(j)

    return ReturnArray



def arrayToPandasDF(DataArray, mode):
    data = DataArray[1:]

    if mode == "F1":
        headers = ["Designator", "Footprint", "Mid X", "Mid Y", "Ref X", "Ref Y", "Pad X", "Pad Y", "TB", "Rotation", "Comment"]

    if mode == "DE":
            headers = ["Part", "Value", "Package", "Library", "Position (mm)", "Orientation"]

    DF = pd.DataFrame(data, columns= headers)
    return DF

def createComponentName(TypeComponent, FormFactor, Comment, Mode):
    componentname = "UNKNOWN_ERROR_CHECK-PROGRAM"
    if Mode == "DE":
        ComponentIdentifier = (re.sub(r"[^a-zA-Z]", "", TypeComponent)).upper()

        if ComponentIdentifier == "R":
            newcommentP1 = re.sub(r"[Rr]", "E", Comment)
            componentname = "R{}".format(newcommentP1)
            #print(componentname)
            #TODO: Maybe exception for DNA parts?
        
        elif ComponentIdentifier == "C":
            componentname = "C{}".format(Comment.replace("F", ""))
            #print(componentname)
        else:
            componentname = Comment
        return componentname

    if Mode == "F1":
        ComponentIdentifier = (re.sub(r"[^a-zA-Z]", "", TypeComponent)).upper()

        # matchups = {"C": "Capacitor",
        #             "D": "Diode",
        #             "IC": "IC",
        #             "R": "Resistor",
        #             "T": "Transistor",
        #             "REL": "Relay",
        #             "K": "Relay"}
        # if ComponentIdentifier in matchups:
        #     print(f"{ComponentIdentifier} is a { matchups[ComponentIdentifier]}!")
        # else:
        #     print("{} is a UNKNOWN type".format(TypeComponent))

        if ComponentIdentifier == "C":
            componentname = "C{}_{}".format(Comment.replace("F", ""), FormFactor)
        
        elif ComponentIdentifier == "D":
            componentname = Comment

        elif ComponentIdentifier == "IC":
            componentname = "{}_{}".format(Comment, FormFactor)
        
        elif ComponentIdentifier == "K":
            componentname = "K_K_K_K_K_K_K_K_K--{}".format(Comment)

        elif ComponentIdentifier == "R":
            componentname = "R{}_{}".format(Comment, FormFactor)
        
        elif ComponentIdentifier == "T":
            componentname = "{}{}".format(Comment, FormFactor)
        
        elif ComponentIdentifier == "Z":
            componentname = "Z_Z_Z_Z_Z_Z_Z_Z_Z--{}".format(Comment)
    

        return componentname

#-------------------------------SeconderyFunctions--------------------
#-------------------------------TertiaryFunctions---------------------

def txtToArray_BOILERPLATE(inputarray):
    ReturnArray = []

    FRead = inputarray.replace("\n", "|").replace("\r", "|")                                      #Replace every newline with a "|" to be split there
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
    return ReturnArray

def fromMiltoMM(Mil):
    return Mil/39.3700787

def fromMMtoMil(MM):
    return MM*39.3700787

def import_file_CALLBACK():
    global importentry
    filename = FileDialog.askopenfilename(title='Select import file', initialdir='/')
    importentry.insert(0, filename)

def export_file_CALLBACK():
    global exportentry
    foldername = FileDialog.askdirectory(title="Select output location", initialdir='/')
    exportentry.insert(0, foldername)

def DEmode_CALLBACK():
    global deviderlabel
    DEBUGMODE = True
    print("asdfasd")
    deviderlabel.config(text="------------------Debug-mode-updated------------------")

#-------------------------------TertiaryFunctions---------------------
#-------------------------------__Main__------------------------------
if __name__ == "__main__":
    loggingSetup()                                                                              #Set up all logging stuff away from the main code for readability
    main()
    exit(0)                                                                                     #When program is done, leave with exitcode 0 (no errors)
else:
    #TODO, log error (can't be run as a module)
    exit(1)