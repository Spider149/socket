from tkinter import ttk
import tkinter as tk
import os
currentPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
nextStep = ""


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        if level >= 1:
            return
        for d in dirs:
            tree.insert("", "end", text='D'+d,
                        values=('[FOLDER] %s' % d,))
        for f in files:
            tree.insert("", "end", text='F'+f, values=('[FILE] %s' % f,))


def onDoubleClick(event):
    try:
        item = tree.selection()[0]
        global currentPath
        currentPath = currentPath + "\\" + tree.item(item, "text")[1:]
        tree.heading("1", text=currentPath)
        tree.delete(*tree.get_children())
        list_files(currentPath)
    except:
        return


def goPrevious():
    global currentPath
    try:
        slicePoint = currentPath.rindex("\\")
        slicePointFromLeft = currentPath.index("\\")
        if(slicePoint == slicePointFromLeft):
            return
    except:
        return
    global nextStep
    nextStep = currentPath[slicePoint+1:]
    currentPath = currentPath[0:slicePoint]
    tree.heading("1", text=currentPath)
    tree.delete(*tree.get_children())
    list_files(currentPath)


def goNext():
    global currentPath
    global nextStep
    if nextStep == "":
        return
    currentPath = currentPath + "\\" + nextStep
    nextStep = ""
    tree.heading("1", text=currentPath)
    tree.delete(*tree.get_children())
    list_files(currentPath)
    return


root = tk.Tk()

tree = ttk.Treeview(root, selectmode='browse')
previousBtn = tk.Button(root, height=3, width=10,
                        text="Previous", command=goPrevious)
previousBtn.grid(row=0, column=0, sticky=tk.W+tk.N +
                 tk.S+tk.E, pady=(20, 0), padx=(20, 0))
nextBtn = tk.Button(root, height=3, width=10,
                    text="Next", command=goNext)
nextBtn.grid(row=0, column=1, sticky=tk.W+tk.N +
             tk.S+tk.E, pady=(20, 0), padx=(20, 0))
tree.grid(row=1, column=0, sticky=tk.W+tk.N +
          tk.S+tk.E, padx=(20, 0), pady=20, columnspan=2)

vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
vsb.grid(row=1, column=2, sticky=tk.W+tk.N +
         tk.S, padx=(0, 20), pady=20)
tree.configure(yscrollcommand=vsb.set)
tree["columns"] = ("1")
tree['show'] = 'headings'
tree.column("1", width=400, anchor='w')
tree.heading("1", text=currentPath)
tree.bind("<Double-1>", onDoubleClick)
list_files(currentPath)
root.mainloop()
