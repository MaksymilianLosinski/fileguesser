from tkinter import *
import os
from tkinter import filedialog
from tkinter.filedialog import askdirectory
import random

PATH = "C:/Program Files (x86)"
HINTS = 3
MODE = "standard"
path = PATH

def setMode(name):
    global MODE
    MODE = name
    currentMode.config(text=f"Current mode: {MODE}")
    currentMode.update()

def Choose():
    global PATH
    PATH = askdirectory()
    currentPath.config(text=f"Current path: {PATH}")
    currentPath.update()

def ChooseFile():
    global guess
    resultEntry.delete(0, END)
    resultEntry.update()
    if add != "":
        guess = askdirectory()
    else:
        guess = filedialog.askopenfilename()
    resultEntry.insert(0,guess)
    resultEntry.update()
    

def updateHints():
    global HINTS
    HINTS = hintsVariable.get()

def Findfile():
    global path
    path = PATH
    listed = os.listdir(path)
    global add
    add = ""

    while True:
        
        length = len(listed)
        #check if not empty directory
        if length == 0:
            add = "Disclaimer: It's an empty folder and not a file"
            break
        rand = random.randint(0,length-1)
        newpath = path + f"/{listed[rand]}"

        #if deep mode enabled try until hits directory
        if MODE == "deep":
            #check if there are any directories left
            for i in listed:
                if os.path.isdir(f"{path}/{i}"):
                    check = True
                    break
                else:
                    check = False

            if check == True and not os.path.isdir(newpath):
                continue
        
        #if new path is directory continue
        if os.path.isdir(f"{newpath}"):
            if(os.path.isdir(newpath)):
                path = newpath
                listed = os.listdir(path)
            continue
        #else stop the loop
        else:
            break

    pathList = newpath.split("/")
    if HINTS < len(pathList):
        hints = HINTS
    else:
        hints = len(pathList)

    output = ""

    output += f"You're looking for ..."
    for i in range(hints, 0,-1):
        output += f"/{pathList[-i]}"

    if add !="":
        output += "\n"+add+""
    output += "\nGood luck!"

    
    outputlabel.config(text=output)
    outputlabel.update()
    path = newpath


def Checkguess():
    global path
    global window_already
    guess = resultEntry.get()
    if path == guess or guess == path.replace("/","\\"):
        result.config(text="That's the correct path")
        window_already = False
    else:
        result.config(text=f"Better luck next time \nThe correct path is: {path}")


window = Tk()
window.title("File guesser")
window.resizable(True, False)
window.geometry("500x500")

window.update()

hintsVariable = IntVar(window)
hintsVariable.set(HINTS)

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))


window.geometry(f"{window_width}x{window_height}+{x}+{y}")

label = Label(window, text="Choose a starting path", font=('consolas',20))
label.pack()

label2 = Label(window, text="C:/Program Files (x86) by default", font=('consolas',10))
label2.pack()

frame = Frame(window)
frame.pack()

modeStandard = Button(frame, text="Standard mode", command= lambda: setMode("standard"))
modeStandard.pack(side=LEFT)

modeDeep = Button(frame, text="Deep mode", command= lambda: setMode("deep"))
modeDeep.pack(side=RIGHT)

currentMode = Label(window, text=f"Current mode: {MODE}")
currentMode.pack()

frame2 = Frame(window)
frame2.pack()

hints = Label(frame2, text="Choose how many folders to hint: ")
hints.pack(side=LEFT)

hintsNumber = Spinbox(frame2, from_=1, to=100, textvariable=hintsVariable, wrap=True, command=updateHints)
hintsNumber.pack()

pathChoose = Button(window, text="Select starting path", command=Choose)
pathChoose.pack()

currentPath = Label(window, text=f"Current path: {PATH}")
currentPath.pack()

roll = Button( text="Find a random file down this path", command=Findfile)
roll.pack()

outputlabel = Label(window, text="This is where the file name will be shown")
outputlabel.pack()

label4 = Label(window, text="Input your guessed path below")
label4.pack()

resultEntry = Entry(window)
resultEntry.pack()

submit_choose = Button(window, text="Choose a file/folder", command=ChooseFile)
submit_choose.pack()

submit = Button(window, text="Submit your guess", command=Checkguess)
submit.pack()


result = Label(window)
result.pack()



window.mainloop()