import tkinter as tk
import tkinter.messagebox as tkmes
import tkinter.filedialog as tkdilg
import tkinter.ttk as ttk
import tkinter.font as font
from PIL import ImageTk, Image
import socket
import base64
import os
import shutil


root = tk.Tk()
root.title("Client")

root.minsize(340, 250)
connected = False
check_see = False
hooking = False
unhooked = False
myFont = font.Font(family="VnArial", size=9)


def onClosing2(parent, current):
    parent.grab_set()
    current.destroy()


def createNewWindow(newWindow, name):
    newWindow.minsize(340, 250)
    newWindow.title(name)


def showConnectionError():
    tkmes.showerror(
        title="Error", message="Chưa kết nối đến server")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def submitIP():
    host = entryIP.get()
    port = 54321
    server_address = (host, port)
    global client
    try:
        client.connect(server_address)
        client.sendall(bytes("-hello-", "utf8"))
        data = client.recv(1024).decode("utf8")
        if data == "-connected-":
            tkmes.showinfo(title="Success",
                           message="Kết nối thành công")
            global connected
            connected = True
    except socket.error:
        tkmes.showerror(title="Error", message="Kết nối thất bại")


def takeScreenshotRequest():

    def takeScreenFirst():
        global client
        client.sendall(bytes("*snap*", "utf8"))
        data = client.recv(1024*1024)
        image = base64.b64decode(data)
        f = open('snapshot.png', 'wb')
        f.write(image)
        f.close()

    def takeScreen():
        takeScreenFirst()
        resizedImg = resizeImg()
        lb.configure(image=resizedImg)
        lb.image = resizedImg

    def saveImg():
        filename = tkdilg.asksaveasfilename(defaultextension=".png", filetypes=(
            ("PNG file", "*.png"), ("All Files", "*.*")))
        if filename != "":
            shutil.move("snapshot.png", filename)

    def resizeImg():
        img = Image.open('snapshot.png')
        newWidth = 360
        ratioScale = img.width/newWidth
        newHeight = int(img.height/ratioScale)
        resized = img.resize((newWidth, newHeight), Image.ANTIALIAS)
        newImg = ImageTk.PhotoImage(resized)
        return newImg

    global connected
    if connected:
        newWindow = tk.Toplevel(root)
        createNewWindow(newWindow, "Screenshot")
        snapBtn = tk.Button(newWindow, text="Chụp",
                            command=takeScreen)
        snapBtn.grid(row=0, column=0, sticky=tk.W+tk.N +
                     tk.S+tk.E, pady=20, padx=20)
        saveImgBtn = tk.Button(newWindow, text="Lưu",
                               command=saveImg)
        saveImgBtn.grid(row=0, column=1, sticky=tk.W+tk.N +
                        tk.S+tk.E, pady=20, padx=(0, 20))
        takeScreenFirst()
        resizedImg = resizeImg()
        lb = tk.Label(newWindow, image=resizedImg)
        lb.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.N +
                tk.S+tk.E, pady=(20, 20), padx=(20, 20))
        newWindow.grab_set()
        newWindow.mainloop()
    else:
        showConnectionError()


def Show_Error():
    tkmes.showerror(
        title="Error", message="Lỗi")


def Show_Kill_Process_Comp():
    tkmes.showinfo(title="Kill Complete", message="Đã diệt process")


def Show_Start_Process_Comp():
    tkmes.showinfo(title="Kill Complete", message="Process đã được bật")


def processRunningRequest():
    global connected

    def Kill():
        killWindow = tk.Toplevel(newWindow)
        createNewWindow(killWindow, "Kill")
        killWindow.minsize(30, 50)

        def kill_final():
            ID = IDkill.get("1.0", tk.END)[:-1]
            if (ID.isnumeric()):
                client.sendall(bytes("kill_process", "utf8"))
                client.sendall(bytes(ID, "utf8"))
                kill_comp = client.recv(1024).decode("utf8")
                if (kill_comp == "kill_success"):
                    Show_Kill_Process_Comp()
                else:
                    Show_Error()
            else:
                Show_Error()

        IDkill = tk.Text(killWindow, height=1, width=50, font=myFont)
        IDkill.grid(row=0, column=0, pady=10,
                    padx=(20, 20), sticky=tk.W+tk.S +
                    tk.N+tk.E)
        IDkill.insert(tk.END, 'Nhập ID')
        killbtn_final = tk.Button(
            killWindow, height=1, width=12, text="Kill", command=kill_final)
        killbtn_final.grid(row=0, column=1, sticky=tk.W+tk.N +
                           tk.S+tk.E, pady=10, padx=(20, 20))
        killWindow.protocol("WM_DELETE_WINDOW",
                            lambda: onClosing2(newWindow, killWindow))
        killWindow.grab_set()
        killWindow.mainloop()

    def See():
        global check_see
        if (check_see):
            return
        i = 0
        client.sendall(bytes("see_process", "utf8"))
        data_see = client.recv(1024*1024).decode("utf8")

        str_recv = data_see.split("_a_")
        for line in str_recv:
            i += 1
            value = line.split("__")
            name = value[0]
            pid = value[1]
            num_thread = value[2]
            tree.insert("", 'end', text="L"+str(i),
                        values=(name, pid, num_thread))
        check_see = True

    def Del():
        global check_see
        if (not check_see):
            return
        child = tree.get_children()
        for item in child:
            tree.delete(item)
        check_see = False

    def Start():
        startwindow = tk.Toplevel(newWindow)
        createNewWindow(startwindow, "Start")
        startwindow.minsize(30, 50)

        def Start_btn():
            ID = NameStart.get("1.0", tk.END)[:-1]
            client.sendall(bytes("start_process", "utf8"))
            client.sendall(bytes(ID, "utf8"))
            start_comp = client.recv(1024).decode("utf8")
            if (start_comp == "success"):
                Show_Start_Process_Comp()
            else:
                Show_Error()

        NameStart = tk.Text(startwindow, height=1, width=50, font=myFont)
        NameStart.grid(row=0, column=0, pady=10,
                       padx=(20, 20), sticky=tk.W+tk.S +
                       tk.N+tk.E)
        NameStart.insert(tk.END, 'Nhập tên')
        Startbtn_final = tk.Button(
            startwindow, height=1, width=12, text="Start", command=Start_btn)
        Startbtn_final.grid(row=0, column=1, sticky=tk.W+tk.N +
                            tk.S+tk.E, pady=10, padx=(20, 20))
        startwindow.protocol("WM_DELETE_WINDOW",
                             lambda: onClosing2(newWindow, startwindow))
        startwindow.grab_set()
        startwindow.mainloop()
    if connected:
        global check_see
        check_see = False
        newWindow = tk.Toplevel(root)
        createNewWindow(newWindow, "Process Running")
        newWindow.minsize(340, 360)
        global client

        killBtn = tk.Button(newWindow, height=3, width=10,
                            text="Kill", command=Kill)
        killBtn.grid(row=0, column=0, sticky=tk.W+tk.N +
                     tk.S+tk.E, pady=20, padx=20)
        SeeBtn = tk.Button(newWindow, height=3, width=10,
                           text="Xem", command=See)
        SeeBtn.grid(row=0, column=1, sticky=tk.W+tk.N +
                    tk.S+tk.E, pady=20, padx=(0, 20))
        DelBtn = tk.Button(newWindow, height=3, width=10,
                           text="Xóa", command=Del)
        DelBtn.grid(row=0, column=2, sticky=tk.W+tk.N +
                    tk.S+tk.E, pady=20, padx=(0, 20))
        StartBtn = tk.Button(newWindow, height=3, width=10,
                             text="Start", command=Start)
        StartBtn.grid(row=0, column=3, sticky=tk.W+tk.N +
                      tk.S+tk.E, pady=20, padx=(0))
        tree = ttk.Treeview(newWindow, selectmode='browse')
        tree.grid(row=1, column=0, columnspan=4, sticky=tk.W+tk.N +
                  tk.S+tk.E, padx=(20, 0))

        vsb = ttk.Scrollbar(newWindow, orient="vertical", command=tree.yview)
        vsb.grid(row=1, column=4, sticky=tk.W+tk.N +
                 tk.S, padx=(0, 20))
        tree.configure(yscrollcommand=vsb.set)
        tree["columns"] = ("1", "2", "3")
        tree['show'] = 'headings'
        tree.column("1", width=200, anchor='c')
        tree.column("2", width=120, anchor='c')
        tree.column("3", width=120, anchor='c')
        tree.heading("1", text="Name Application")
        tree.heading("2", text="ID Application")
        tree.heading("3", text="Count Thread")
        newWindow.grab_set()
        newWindow.mainloop()

    else:
        showConnectionError()


def Show_Start_App_Comp():
    tkmes.showinfo(title="Start Complete", message="App đã được bật")


def Show_Kill_App_Comp():
    tkmes.showinfo(title="Kill Complete", message="App đã đươc diệt")


def appRunningRequest():
    global connected

    def Kill():
        killWindow = tk.Toplevel(newWindow)
        createNewWindow(killWindow, "Kill")
        killWindow.minsize(30, 50)

        def kill_final():
            ID = IDkill.get("1.0", tk.END)[:-1]
            if (ID.isnumeric()):
                client.sendall(bytes("kill_app", "utf8"))
                client.sendall(bytes(ID, "utf8"))
                kill_comp = client.recv(1024).decode("utf8")
                if (kill_comp == "kill_success"):
                    Show_Kill_App_Comp()
                else:
                    Show_Error()
            else:
                Show_Error()

        IDkill = tk.Text(killWindow, height=1, width=50, font=myFont)
        IDkill.grid(row=0, column=0, pady=10,
                    padx=(20, 20), sticky=tk.W+tk.S +
                    tk.N+tk.E)
        IDkill.insert(tk.END, 'Nhập ID')
        killbtn_final = tk.Button(
            killWindow, height=1, width=12, text="Kill", command=kill_final)
        killbtn_final.grid(row=0, column=1, sticky=tk.W+tk.N +
                           tk.S+tk.E, pady=10, padx=(20, 20))
        killWindow.protocol("WM_DELETE_WINDOW",
                            lambda: onClosing2(newWindow, killWindow))
        killWindow.grab_set()
        killWindow.mainloop()

    def See():
        global check_see
        if (check_see):
            return
        i = 0
        client.sendall(bytes("see_app", "utf8"))
        data_see = client.recv(1024*1024).decode("utf8")

        str_recv = data_see.split("_a_")
        for line in str_recv:
            i += 1
            value = line.split("__")
            name = value[0]
            pid = value[1]
            num_thread = value[2]
            tree.insert("", 'end', text="L"+str(i),
                        values=(name, pid, num_thread))
        check_see = True

    def Del():
        global check_see
        if (not check_see):
            return
        child = tree.get_children()
        for item in child:
            tree.delete(item)
        check_see = False

    def Start():
        startwindow = tk.Toplevel(newWindow)
        createNewWindow(startwindow, "Start")
        startwindow.minsize(30, 50)

        def Start_btn():
            ID = NameStart.get("1.0", tk.END)[:-1]
            client.sendall(bytes("start_app", "utf8"))
            client.sendall(bytes(ID, "utf8"))
            start_comp = client.recv(1024).decode("utf8")
            if (start_comp == "success"):
                Show_Start_App_Comp()
            else:
                Show_Error()
        NameStart = tk.Text(startwindow, height=1, width=50, font=myFont)
        NameStart.grid(row=0, column=0, pady=10,
                       padx=(20, 20), sticky=tk.W+tk.S +
                       tk.N+tk.E)
        NameStart.insert(tk.END, 'Nhập tên')
        Startbtn_final = tk.Button(
            startwindow, height=1, width=12, text="Start", command=Start_btn)
        Startbtn_final.grid(row=0, column=1, sticky=tk.W+tk.N +
                            tk.S+tk.E, pady=10, padx=(20, 20))
        startwindow.protocol("WM_DELETE_WINDOW",
                             lambda: onClosing2(newWindow, startwindow))
        startwindow.grab_set()
        startwindow.mainloop()
    if connected:
        global check_see
        check_see = False
        newWindow = tk.Toplevel(root)
        createNewWindow(newWindow, "App Running")
        newWindow.minsize(340, 360)
        global client

        killBtn = tk.Button(newWindow, height=3, width=10,
                            text="Kill", command=Kill)
        killBtn.grid(row=0, column=0, sticky=tk.W+tk.N +
                     tk.S+tk.E, pady=20, padx=20)
        SeeBtn = tk.Button(newWindow, height=3, width=10,
                           text="Xem", command=See)
        SeeBtn.grid(row=0, column=1, sticky=tk.W+tk.N +
                    tk.S+tk.E, pady=20, padx=(0, 20))
        DelBtn = tk.Button(newWindow, height=3, width=10,
                           text="Xóa", command=Del)
        DelBtn.grid(row=0, column=2, sticky=tk.W+tk.N +
                    tk.S+tk.E, pady=20, padx=(0, 20))
        StartBtn = tk.Button(newWindow, height=3, width=10,
                             text="Start", command=Start)
        StartBtn.grid(row=0, column=3, sticky=tk.W+tk.N +
                      tk.S+tk.E, pady=20, padx=(0))

        tree = ttk.Treeview(newWindow, selectmode='browse')
        tree.grid(row=1, column=0, columnspan=4, sticky=tk.W+tk.N +
                  tk.S+tk.E, padx=(20, 0))

        vsb = ttk.Scrollbar(newWindow, orient="vertical", command=tree.yview)
        vsb.grid(row=1, column=4, sticky=tk.W+tk.N +
                 tk.S, padx=(0, 20))
        tree.configure(yscrollcommand=vsb.set)
        tree["columns"] = ("1", "2", "3")
        tree['show'] = 'headings'
        tree.column("1", width=200, anchor='c')
        tree.column("2", width=120, anchor='c')
        tree.column("3", width=120, anchor='c')
        tree.heading("1", text="Name Application")
        tree.heading("2", text="ID Application")
        tree.heading("3", text="Count Thread")
        newWindow.grab_set()
        newWindow.mainloop()
    else:
        showConnectionError()


def closeRequest():
    global connected
    if connected:
        global client
        client.sendall(bytes("*close*", "utf8"))
    else:
        showConnectionError()


def keystrokeRequest():
    global connected

    def disableWindow():
        pass

    def enableWindow():
        newWindow.destroy()
        f = open("keylog.txt", "w")
        f.truncate(0)
        f.close()

    def Hook():
        global hooking
        if hooking:
            return
        client.sendall(bytes("hook", "utf8"))
        hooking = True
        newWindow.protocol("WM_DELETE_WINDOW", disableWindow)

    def UnHook():
        global hooking
        if not hooking:
            return
        client.sendall(bytes("unhook", "utf8"))
        global unhooked
        unhooked = True
        hooking = False
        newWindow.protocol("WM_DELETE_WINDOW", enableWindow)

    def PrintKeyBoard():
        global unhooked
        global hooking
        if unhooked and not hooking:
            client.sendall(bytes("printkey", "utf8"))
            content = client.recv(1024*1024).decode("utf8")
            Text_box.configure(state="normal")
            Text_box.delete(1.0, tk.END)
            Text_box.insert(tk.END, content)
            Text_box.configure(state="disabled")

    def Del():
        Text_box.configure(state="normal")
        Text_box.delete(1.0, tk.END)
        Text_box.configure(state="disabled")

    if connected:
        global hooking
        global unhooked
        hooking = False
        unhooked = False
        newWindow = tk.Toplevel(root)
        createNewWindow(newWindow, "Keystroke")
        newWindow.minsize(340, 360)
        global client
        client.sendall(bytes("app running", "utf8"))

        HookBtn = tk.Button(newWindow, height=3, width=10,
                            text="Hook", command=Hook)
        HookBtn.grid(row=0, column=0, sticky=tk.W+tk.N +
                     tk.S+tk.E, pady=20, padx=20)
        UnHookBtn = tk.Button(newWindow, height=3, width=10,
                              text="Unhook", command=UnHook)
        UnHookBtn.grid(row=0, column=1, sticky=tk.W+tk.N +
                       tk.S+tk.E, pady=20, padx=(0, 20))
        PrintBtn = tk.Button(newWindow, height=3, width=10,
                             text="In phím", command=PrintKeyBoard)
        PrintBtn.grid(row=0, column=2, sticky=tk.W+tk.N +
                      tk.S+tk.E, pady=20, padx=(0, 20))
        DelBtn = tk.Button(newWindow, height=3, width=10,
                           text="Xóa", command=Del)
        DelBtn.grid(row=0, column=3, sticky=tk.W+tk.N +
                    tk.S+tk.E, pady=20, padx=(0, 20))
        Text_box = tk.Text(newWindow, height=15, width=41)
        Text_box.grid(row=1, column=0, sticky=tk.W+tk.N +
                      tk.S+tk.E, padx=20, columnspan=4)
        Text_box.configure(state="disabled")
        newWindow.grab_set()
        newWindow.mainloop()
    else:
        showConnectionError()


def registryRequest():
    def submitAddress():
        value = registryContent.get("1.0", tk.END)
        global client
        client.sendall(bytes("6"+value, "utf8"))
        data = client.recv(1024).decode("utf8")
        if data == "s":
            tkmes.showinfo(title="Thành công",
                           message="Import registry thành công!")
        else:
            tkmes.showerror(title="Thất bại",
                            message="Import registry thất bại!")

    def browseAddress():
        filename = tkdilg.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Registry Files",
                                                      "*.reg*"),))
        f = open(filename, encoding="utf_16")
        address.delete(0, tk.END)
        address.insert(0, filename)
        value = f.read()
        f.close()
        registryContent.delete(1.0, tk.END)
        registryContent.insert(tk.END, value)

    def deleteShowResultContent():
        showResult.configure(state="normal")
        showResult.delete(1.0, tk.END)
        showResult.configure(state="disabled")

    def showResultContent(data):
        showResult.configure(state="normal")
        showResult.insert(tk.END, data)
        showResult.configure(state="disabled")

    def sendRegistryRequest():
        global client
        currentSelect = dropdown.current()
        if currentSelect == 0:
            client.sendall(bytes("1"+pathContent.get("1.0", tk.END)[:-1] +
                           "***"+nameValueContent.get("1.0", tk.END)[:-1], "utf8"))
        elif currentSelect == 1:
            client.sendall(bytes("2"+pathContent.get("1.0", tk.END)
                           [:-1]+"**"+nameValueContent.get("1.0", tk.END)[:-1]+"***"+valueContent.get("1.0", tk.END)[:-1]+"****"+typeContent.get(), "utf8"))
        elif currentSelect == 2:
            client.sendall(bytes("3"+pathContent.get("1.0", tk.END)[:-1] +
                           "***"+nameValueContent.get("1.0", tk.END)[:-1], "utf8"))
        elif currentSelect == 3:
            client.sendall(
                bytes("4"+pathContent.get("1.0", tk.END)[:-1], "utf8"))
        elif currentSelect == 4:
            client.sendall(
                bytes("5"+pathContent.get("1.0", tk.END)[:-1], "utf8"))
        else:
            return
        data = client.recv(1024).decode("utf8")+"\n"
        showResultContent(data)

    def updateUI(self):
        currentValue = dropdown.current()
        if currentValue == 0:  # get value
            nameValueContent.grid(row=5, column=0, pady=(0, 10),
                                  padx=(20, 20), sticky=tk.W+tk.S +
                                  tk.N+tk.E, columnspan=2)
            valueContent.grid_remove()
            typeContent.grid_remove()
        elif currentValue == 1:  # set value
            nameValueContent.grid(row=5, column=0, pady=(0, 10),
                                  padx=(20, 20), sticky=tk.W+tk.S +
                                  tk.N+tk.E, columnspan=2)
            valueContent.grid(row=6, column=0, pady=(0, 10),
                              padx=(20, 20), sticky=tk.W+tk.S +
                              tk.N+tk.E, columnspan=2)
            typeContent.grid(row=7, column=0, sticky=tk.W+tk.S +
                             tk.N+tk.E, padx=(20), columnspan=2)
        elif currentValue == 2:  # delete value
            nameValueContent.grid(row=5, column=0, pady=(0, 10),
                                  padx=(20, 20), sticky=tk.W+tk.S +
                                  tk.N+tk.E, columnspan=2)
            valueContent.grid_remove()
            typeContent.grid_remove()
        elif currentValue == 3 or currentValue == 4:  # create key and #delete key
            nameValueContent.grid_remove()
            valueContent.grid_remove()
            typeContent.grid_remove()

    global connected
    if connected:
        newWindow = tk.Toplevel(root)
        createNewWindow(newWindow, "Registry")
        newWindow.minsize(485, 300)
        address = tk.Entry(newWindow, font=myFont)

        address.grid(row=0, column=0, pady=10, sticky=tk.W +
                     tk.S+tk.N+tk.E, padx=(20, 10))
        browseBtn = tk.Button(newWindow, text="Browse...",
                              command=browseAddress)
        browseBtn.grid(row=0, column=1, sticky=tk.W+tk.S +
                       tk.N+tk.E, pady=10, padx=(0, 20))
        registryContent = tk.Text(newWindow, height=6, width=50, font=myFont)
        registryContent.grid(row=1, column=0, pady=0,
                             padx=(20, 10), sticky=tk.W+tk.S +
                             tk.N+tk.E)
        registrySubmitBtn = tk.Button(
            newWindow, text="Gửi nội dung", command=submitAddress)
        registrySubmitBtn.grid(row=1, column=1, sticky=tk.W+tk.S +
                               tk.N+tk.E, pady=0, padx=(0, 20))
        labelFix = tk.Label(newWindow, text="Sửa giá trị trực tiếp")
        labelFix.grid(row=2, column=0, sticky=tk.W,  pady=(3, 3), padx=20)

        dropdown = ttk.Combobox(newWindow, width=27,
                                textvariable=tk.StringVar())
        dropdown['values'] = ("Get value", "Set value",
                              "Delete value", "Create key", "Delete key")
        dropdown.grid(row=3, column=0, sticky=tk.W+tk.S +
                      tk.N+tk.E, padx=(20, 20), columnspan=2)
        dropdown.set("Chọn chức năng")
        dropdown.bind("<<ComboboxSelected>>", updateUI)
        pathContent = tk.Text(newWindow, height=1, width=35, font=myFont)
        pathContent.grid(row=4, column=0, pady=10,
                         padx=(20, 20), sticky=tk.W+tk.S +
                         tk.N+tk.E, columnspan=2)
        pathContent.insert(
            tk.END, "Đường dẫn")
        nameValueContent = tk.Text(newWindow, height=1, width=35, font=myFont)
        nameValueContent.grid(row=5, column=0, pady=(0, 10),
                              padx=(20, 20), sticky=tk.W+tk.S +
                              tk.N+tk.E, columnspan=2)
        nameValueContent.insert(tk.END, 'Name value')
        valueContent = tk.Text(newWindow, height=1, width=35, font=myFont)
        valueContent.grid(row=6, column=0, pady=(0, 10),
                          padx=(20, 20), sticky=tk.W+tk.S +
                          tk.N+tk.E, columnspan=2)
        valueContent.insert(tk.END, 'Value')
        typeContent = ttk.Combobox(newWindow, width=15,
                                   textvariable=tk.StringVar())
        typeContent['values'] = (
            "String", "Binary", "DWORD", "QWORD", "Multi-String", "Extendable String")
        typeContent.set("Kiểu dữ liệu")
        typeContent.grid(row=7, column=0, sticky=tk.W+tk.S +
                         tk.N+tk.E, padx=(20), columnspan=2)
        showResult = tk.Text(newWindow, height=6, width=1,
                             font=myFont, state="disabled")
        showResult.grid(row=8, column=0, pady=(10, 0),
                        padx=(20, 20), sticky=tk.W+tk.S +
                        tk.N+tk.E, columnspan=2)
        sendBtn = tk.Button(newWindow, text="Gửi", command=sendRegistryRequest)
        sendBtn.grid(row=9, column=0, pady=10, padx=(20, 10), sticky=tk.W+tk.E)
        deleteBtn = tk.Button(newWindow, text="Xóa",
                              command=deleteShowResultContent)
        deleteBtn.grid(row=9, column=1, pady=10,
                       padx=(0, 20), sticky=tk.W+tk.E)
        newWindow.mainloop()
        newWindow.grab_set()
    else:
        showConnectionError()


def exitRequest():
    global connected
    if connected:
        global client
        if os.path.exists("snapshot.png"):
            os.remove("snapshot.png")
        try:
            client.sendall(bytes("-exit-", "utf8"))
        except:
            pass
        client.close()

    root.destroy()


labelIP = tk.Label(root, text="Nhập IP:")
labelIP.grid(row=0, column=0, pady=20, sticky=tk.W +
             tk.S+tk.N+tk.E, padx=(20, 10))

entryIP = tk.Entry(root)
entryIP.grid(row=0, column=1, pady=20, sticky=tk.W +
             tk.S+tk.N+tk.E, padx=(0, 10))

entryIP.insert(tk.END, '127.0.0.1')

ipBtn = tk.Button(root, text="Nhập", command=submitIP)
ipBtn.grid(row=0, column=2, sticky=tk.W+tk.S +
           tk.N+tk.E, pady=20, padx=(0, 10))

processBtn = tk.Button(root, text="Process running",
                       command=processRunningRequest)
processBtn.grid(row=1, column=2, sticky=tk.W+tk.N +
                tk.S+tk.E, pady=(0, 20), padx=(0, 10))

screenshotBtn = tk.Button(root, text="Chụp màn hình",
                          command=takeScreenshotRequest)
screenshotBtn.grid(row=1, column=1, sticky=tk.W+tk.N +
                   tk.S+tk.E, pady=(0, 20), padx=(0, 10))

appRunningBtn = tk.Button(root, text="App Running",
                          command=appRunningRequest)
appRunningBtn.grid(row=2, column=1, sticky=tk.W+tk.N +
                   tk.S+tk.E, pady=(0, 20), padx=(0, 10))

keystrokeBtn = tk.Button(root, text="Keystroke",
                         command=keystrokeRequest)
keystrokeBtn.grid(row=2, column=2, sticky=tk.W+tk.N +
                  tk.S+tk.E, pady=(0, 20), padx=(0, 10))

registryBtn = tk.Button(root, text="Sửa registry",
                        command=registryRequest)
registryBtn.grid(row=3, column=1, sticky=tk.W+tk.N +
                 tk.S+tk.E, pady=(0, 20), padx=(0, 10))

closeServerBtn = tk.Button(root, text="Tắt máy",
                           command=closeRequest)
closeServerBtn.grid(row=3, column=2, sticky=tk.W+tk.N +
                    tk.S+tk.E, pady=(0, 20), padx=(0, 10))

exitBtn = tk.Button(root, text="Thoát",
                    command=exitRequest)
exitBtn.grid(row=4, column=2, sticky=tk.W+tk.N +
             tk.S+tk.E, pady=(0, 20), padx=(0, 10))


def onClosing():
    if tkmes.askokcancel("Quit", "Do you want to quit?"):
        exitRequest()


root.protocol("WM_DELETE_WINDOW", onClosing)
root.mainloop()
