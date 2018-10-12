from tkinter import *
from tkinter import messagebox
# from tkinter.ttk import *
import os.path

def update():
    global noteButtons
    global empty
    for i in noteButtons:
        i.destroy()
    empty.destroy()
    global c
    noteButtons = list()
    if not os.path.exists('notes'):
        os.makedirs('notes')
    for a,b,c in os.walk('notes'):
        for i in c:
            noteButton = Button(buttons,text=i.split(".txt")[0],command=lambda i=i:edit(i))
            noteButtons.append(noteButton)
            noteButton.pack(side=TOP,fill=X)
        if len(c) == 0:
            empty = Label(buttons,text="No notes yet!")
            empty.pack(side=TOP)

def updateStatus(event):
    global statusText
    global note
    #if statusText.get() == "" or statusText.get() == "Saved!":
    if note.edit_modified():
        statusText.set("UNSAVED")
    else:
        statusText.set("")

def save(event,i,file):
    global unsaved
    global statusText
    a = title.get()
    b = note.get(1.0,END)
    if os.path.exists("notes/"+a+".txt") == True and file == "new":
        if messagebox.askyesno("Replace existing file?","Overwrite existing file with that name?"):
            p = open("notes/"+a+".txt","w")
            p.write(b)
            p.close()
         #   windows[i].title(a)
            unsaved = 0
            update()
            statusText.set("")
            note.edit_modified(False)
            #title.edit_modified(False)
    else:
        p = open("notes/"+a+".txt","w")
        p.write(b)
        p.close()
        #windows[i].title(a)
        unsaved = 0
        update()
        file = "not new"
        statusText.set("")
        note.edit_modified(False)

def edit(file):
    global title
    global note
    title.destroy()
    note.destroy()
    # global windows
    notesOpen = len(c)
    # window = Toplevel(root)
    # window.geometry("300x300")
    # windows.append(window)
    global titleText
    global statusText
    statusText.set("")
    titleText = StringVar()
    title = Entry(noteFrame,font=("Segoe UI Bold",14),textvariable=titleText)
    title.pack(side=TOP,fill=X)
    titles.append(title)
   # global note
    note = Text(noteFrame,font=("Segoe UI",11))
    note.pack(side=TOP,fill=BOTH,expand=True)
    notes.append(note)
    #title.edit_modified()
    #note.edit_modified()
    title.bind("<Control-s>",lambda e,c=notesOpen-1,file=file:save(e,c,file))
    note.bind("<Control-s>",lambda e,c=notesOpen-1:save(e,c,file))
    title.bind("<Key>",updateStatus)
    note.bind("<Key>",updateStatus)
    if file == "new":
        # window.title("New note")
        titleText.set("New note")
        title.focus_set()
        title.select_range(0, END)
    else:
        p = open("notes/"+file,"r")
        load = p.read()
        p.close()
        note.insert(1.0,load)
        theTitle = file.split(".txt")[0]
        titleText.set(theTitle)
        # window.title(theTitle)
        
def cancel():
    # global instructionLabel
    # instructionLabel.pack_forget()
    deleteButton.config(text="Delete",command=remove)
    update()
    global statusText
    statusText.set("")

def removeNote(i):
    if messagebox.askyesno("Delete note?","Are you sure?"):
        os.remove('notes/'+c[i])
        noteButtons[i].destroy()
        cancel()

def remove():
    # global instructionLabel
    # instructionLabel.pack(side=TOP,anchor=W)
    deleteButton.config(text="Cancel",command=cancel)
    for i in range(len(noteButtons)):
        noteButtons[i].config(command=lambda i=i:removeNote(i))
    global statusText
    statusText.set("Click a note to delete.")

windows = list()
titles = list()
notes = list()
noteButtons = list()
global unsaved
unsaved = 0
root = Tk()
#root.geometry("200x400")
root.title("Note-oriety")
global statusText
statusText = StringVar()
status = Label(root,relief=GROOVE,textvariable=statusText)
status.pack(side=BOTTOM,fill=X)
Label(root,text="Note-oriety",font=("Segoe UI",18)).pack(side=TOP)
toolbar = Frame(root)
toolbar.pack(side=TOP)
Button(toolbar,text="Add",command=lambda:edit("new")).pack(side=LEFT)
global deleteButton
deleteButton = Button(toolbar,text="Delete",command=remove)
deleteButton.pack(side=LEFT)
# instructionFrame = Frame(root)
# instructionFrame.pack(side=TOP)
# global instruction
# instruction = StringVar()
# global instructionLabel
# instructionLabel = Label(instructionFrame,textvariable=instruction)
# instruction.set("Delete note")
#Separator(root,orient=HORIZONTAL).pack(side=TOP,fill=X)
buttons = Frame(root)
buttons.pack(side=LEFT,anchor=N,padx=5,pady=5)
#Separator(root,orient=VERTICAL).pack(side=LEFT,fill=Y)
noteFrame = Frame(root)
noteFrame.pack(side=LEFT,fill=BOTH,expand=True)
global empty
empty = Label(buttons)
update()
global title
title = Frame(root)
global note
note = Frame(root)
edit("new")
root.mainloop()
