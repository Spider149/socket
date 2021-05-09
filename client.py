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
import psutil
import codecs
import winreg

root = tk.Tk()
root.title("Client")

root.minsize(340, 250)
connected = False
myFont = font.Font(family="VnArial", size=9)


def createNewWindow(newWindow, name):
    newWindow.minsize(340, 250)
    newWindow.title(name)
    newWindow.grab_set()


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
            print("connected")
            tkmes.showinfo(title="Success",
                           message="Kết nối thành công")
            global connected
            connected = True
    except socket.error:
        tkmes.showerror(title="Error", message="Kết nối thất bại")


def takeScreenshotRequest():

    def takeScreenFirst():  # lúc mở lên là chụp luôn, không cần update
        global client
        client.sendall(bytes("*snap*", "utf8"))
        data = client.recv(1024*1024)
        image = base64.b64decode(data)
        f = open('snapshot.png', 'wb')
        f.write(image)
        f.close()

    def takeScreen():  # các lần chụp sau, chụp xong update vô GUI
        takeScreenFirst()
        resizedImg = resizeImg()
        lb.configure(image=resizedImg)
        lb.image = resizedImg

    def saveImg():  # lưu hình, nếu không lưu thì tí nữa sẽ bị xóa khi đóng app
        filename = tkdilg.asksaveasfilename(defaultextension=".png", filetypes=(
            ("PNG file", "*.png"), ("All Files", "*.*")))
        if filename != "":
            shutil.move("snapshot.png", filename)

    def resizeImg():  # scale hình cho vừa khung
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
        newWindow.protocol("WM_DELETE_WINDOW", on_closing1)
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
        newWindow.mainloop()
    else:
        showConnectionError()


def Show_Error():
    tkmes.showerror(
        title="Error", message="Lỗi")


def processRunningRequest():
    global connected

    def Kill():
        killWindow = tk.Toplevel(newWindow)
        createNewWindow(killWindow, "Kill")
        killWindow.minsize(30, 50)

        def kill_final():
            ID = IDkill.get("1.0", tk.END)
            if (True):
                pass
            else:
                Show_Error()
            return
            # Dò id để kill
        IDkill = tk.Text(killWindow, height=1, width=50, font=myFont)
        IDkill.grid(row=0, column=0, pady=10,
                    padx=(20, 20), sticky=tk.W+tk.S +
                    tk.N+tk.E)
        IDkill.insert(tk.END, 'Nhập ID')
        killbtn_final = tk.Button(
            killWindow, height=1, width=12, text="Kill", command=kill_final)
        killbtn_final.grid(row=0, column=1, sticky=tk.W+tk.N +
                           tk.S+tk.E, pady=10, padx=(20, 20))
        killWindow.mainloop()

    def See():
        return

    def Del():
        return

    def Start():
        startwindow = tk.Toplevel(newWindow)
        createNewWindow(startwindow, "Start")
        startwindow.minsize(30, 50)

        def Start_btn():
            ID = NameStart.get("1.0", tk.END)
            if (True):
                pass
            else:
                Show_Error()
            return
            # Dò id để kill
        NameStart = tk.Text(startwindow, height=1, width=50, font=myFont)
        NameStart.grid(row=0, column=0, pady=10,
                       padx=(20, 20), sticky=tk.W+tk.S +
                       tk.N+tk.E)
        NameStart.insert(tk.END, 'Nhập tên')
        Startbtn_final = tk.Button(
            startwindow, height=1, width=12, text="Start", command=Start_btn)
        Startbtn_final.grid(row=0, column=1, sticky=tk.W+tk.N +
                            tk.S+tk.E, pady=10, padx=(20, 20))
        startwindow.mainloop()
    if connected:
        print("process running")
        newWindow = tk.Toplevel(root)
        createNewWindow(newWindow, "Process Running")
        newWindow.minsize(340, 360)
        global client
        client.sendall(bytes("process", "utf8"))
        data = client.recv(1024).decode("utf8")
        print(data)
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
                      tk.S+tk.E, pady=20, padx=(0, 20))
        tree = ttk.Treeview(newWindow, selectmode='browse')
        tree.grid(row=1, column=0, columnspan=4, sticky=tk.W+tk.N +
                  tk.S+tk.E, padx=20)

        vsb = ttk.Scrollbar(newWindow, orient="vertical", command=tree.yview)
        vsb.place(x=445, y=98, height=200+20)
        tree.configure(yscrollcommand=vsb.set)
        tree["columns"] = ("1", "2", "3")
        tree['show'] = 'headings'
        tree.column("1", width=120, anchor='c')
        tree.column("2", width=120, anchor='c')
        tree.column("3", width=200, anchor='c')
        tree.heading("1", text="Name Application")
        tree.heading("2", text="ID Application")
        tree.heading("3", text="Count Thread")
        tree.insert("", 'end', text="L1", values=("Big1", "Best"))
        tree.insert("", 'end', text="L2", values=("Big2", "Best"))
        tree.insert("", 'end', text="L3", values=("Big3", "Best"))
        tree.insert("", 'end', text="L4", values=("Big4", "Best"))
        tree.insert("", 'end', text="L5", values=("Big5", "Best"))
        tree.insert("", 'end', text="L6", values=("Big6", "Best"))
        tree.insert("", 'end', text="L7", values=("Big7", "Best"))
        tree.insert("", 'end', text="L8", values=("Big8", "Best"))
        tree.insert("", 'end', text="L9", values=("Big9", "Best"))
        tree.insert("", 'end', text="L10", values=("Big10", "Best"))
        tree.insert("", 'end', text="L11", values=("Big11", "Best"))
        tree.insert("", 'end', text="L12", values=("Big12", "Best"))
        newWindow.mainloop()
        #filename = tkdilg.askopenfilename()
        # print(filename)  # test
    else:
        showConnectionError()


def appRunningRequest():
    global connected

    def Kill():
        killWindow = tk.Toplevel(newWindow)
        createNewWindow(killWindow, "Kill")
        killWindow.minsize(30, 50)

        def kill_final():
            ID = IDkill.get("1.0", tk.END)
            if (True):
                pass
            else:
                Show_Error()
            return
            # Dò id để kill
        IDkill = tk.Text(killWindow, height=1, width=50, font=myFont)
        IDkill.grid(row=0, column=0, pady=10,
                    padx=(20, 20), sticky=tk.W+tk.S +
                    tk.N+tk.E)
        IDkill.insert(tk.END, 'Nhập ID')
        killbtn_final = tk.Button(
            killWindow, height=1, width=12, text="Kill", command=kill_final)
        killbtn_final.grid(row=0, column=1, sticky=tk.W+tk.N +
                           tk.S+tk.E, pady=10, padx=(20, 20))
        killWindow.mainloop()

    def See():
        return

    def Del():
        return

    def Start():
        startwindow = tk.Toplevel(newWindow)
        createNewWindow(startwindow, "Start")
        startwindow.minsize(30, 50)

        def Start_btn():
            ID = NameStart.get("1.0", tk.END)
            if (True):
                pass
            else:
                Show_Error()
            return
            # Dò id để kill
        NameStart = tk.Text(startwindow, height=1, width=50, font=myFont)
        NameStart.grid(row=0, column=0, pady=10,
                       padx=(20, 20), sticky=tk.W+tk.S +
                       tk.N+tk.E)
        NameStart.insert(tk.END, 'Nhập tên')
        Startbtn_final = tk.Button(
            startwindow, height=1, width=12, text="Start", command=Start_btn)
        Startbtn_final.grid(row=0, column=1, sticky=tk.W+tk.N +
                            tk.S+tk.E, pady=10, padx=(20, 20))
        startwindow.mainloop()
    if connected:
        print("app running")
        newWindow = tk.Toplevel(root)
        createNewWindow(newWindow, "App Running")
        newWindow.minsize(340, 360)
        global client
        client.sendall(bytes("app running", "utf8"))
        data = client.recv(1024).decode("utf8")
        print(data)
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
                      tk.S+tk.E, pady=20, padx=(0, 20))

        tree = ttk.Treeview(newWindow, selectmode='browse')
        tree.grid(row=1, column=0, columnspan=4, sticky=tk.W+tk.N +
                  tk.S+tk.E, padx=20)

        vsb = ttk.Scrollbar(newWindow, orient="vertical", command=tree.yview)
        vsb.place(x=445, y=98, height=200+20)
        tree.configure(yscrollcommand=vsb.set)
        tree["columns"] = ("1", "2", "3")
        tree['show'] = 'headings'
        tree.column("1", width=120, anchor='c')
        tree.column("2", width=120, anchor='c')
        tree.column("3", width=200, anchor='c')
        tree.heading("1", text="Name Application")
        tree.heading("2", text="ID Application")
        tree.heading("3", text="Count Thread")
        tree.insert("", 'end', text="L1", values=("Big1", "Best"))
        tree.insert("", 'end', text="L2", values=("Big2", "Best"))
        tree.insert("", 'end', text="L3", values=("Big3", "Best"))
        tree.insert("", 'end', text="L4", values=("Big4", "Best"))
        tree.insert("", 'end', text="L5", values=("Big5", "Best"))
        tree.insert("", 'end', text="L6", values=("Big6", "Best"))
        tree.insert("", 'end', text="L7", values=("Big7", "Best"))
        tree.insert("", 'end', text="L8", values=("Big8", "Best"))
        tree.insert("", 'end', text="L9", values=("Big9", "Best"))
        tree.insert("", 'end', text="L10", values=("Big10", "Best"))
        tree.insert("", 'end', text="L11", values=("Big11", "Best"))
        tree.insert("", 'end', text="L12", values=("Big12", "Best"))
        newWindow.mainloop()
    else:
        showConnectionError()


def closeRequest():
    global connected
    if connected:
        print("close")
        global client
        client.sendall(bytes("*close*", "utf8"))
    else:
        showConnectionError()


def keystrokeRequest():
    global connected
    if connected:
        print("keylog")
        newWindow = tk.Toplevel(root)
        createNewWindow(newWindow, "Keystroke")
    else:
        showConnectionError()


def registryRequest():
    def submitAddress():
        print("Abc")

    def browseAddress():
        filename = tkdilg.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Registry Files",
                                                      "*.reg*"),))
        f = codecs.open(filename, encoding="utf_16")
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
        if currentSelect == 1:
            client.sendall(bytes("1"+pathContent.get("1.0", tk.END)[:-1] +
                           "***"+nameValueContent.get("1.0", tk.END)[:-1], "utf8"))
            rawData = client.recv(1024)
            data = None
            try:
                data = rawData.decode("utf8")+"\n"
            except:
                data = ""
                for byte in rawData:
                    data = data+str(byte)+" "
                data += "\n"
            showResultContent(data)
        elif currentSelect == 2:
            client.sendall(bytes("2"+pathContent.get("1.0", tk.END)
                           [:-1]+"**"+nameValueContent.get("1.0", tk.END)[:-1]+"***"+valueContent.get("1.0", tk.END)[:-1]+"****"+typeContent.get(), "utf8"))
            data = client.recv(1024).decode("utf8")
            showResultContent(data)

    def updateUI(self):
        currentValue = dropdown.current()
        if currentValue == 1:  # get value
            nameValueContent.grid(row=5, column=0, pady=(0, 10),
                                  padx=(20, 20), sticky=tk.W+tk.S +
                                  tk.N+tk.E, columnspan=2)
            valueContent.grid_remove()
            typeContent.grid_remove()
            pass
        elif currentValue == 2:  # set value
            nameValueContent.grid(row=5, column=0, pady=(0, 10),
                                  padx=(20, 20), sticky=tk.W+tk.S +
                                  tk.N+tk.E, columnspan=2)
            valueContent.grid(row=6, column=0, pady=(0, 10),
                              padx=(20, 20), sticky=tk.W+tk.S +
                              tk.N+tk.E, columnspan=2)
            typeContent.grid(row=7, column=0, sticky=tk.W+tk.S +
                             tk.N+tk.E, padx=(20), columnspan=2)
            pass
        elif currentValue == 3:  # delete value
            nameValueContent.grid(row=5, column=0, pady=(0, 10),
                                  padx=(20, 20), sticky=tk.W+tk.S +
                                  tk.N+tk.E, columnspan=2)
            valueContent.grid_remove()
            typeContent.grid_remove()
            pass
        elif currentValue == 4 or currentValue == 5:  # create key and #delete key
            nameValueContent.grid_remove()
            valueContent.grid_remove()
            typeContent.grid_remove()
            pass
        else:
            pass
        print(currentValue)
    # global connected
    # if connected:
    print("registry")
    newWindow = tk.Toplevel(root)
    createNewWindow(newWindow, "Registry")
    newWindow.minsize(485, 460)
    address = tk.Entry(newWindow, font=myFont)

    address.grid(row=0, column=0, pady=10, sticky=tk.W +
                 tk.S+tk.N+tk.E, padx=(20, 10))
    browseBtn = tk.Button(newWindow, text="Browse...", command=browseAddress)
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
    dropdown['values'] = ("Chọn chức năng", "Get value", "Set value",
                          "Delete value", "Create key", "Delete key")
    dropdown.current(0)
    dropdown.grid(row=3, column=0, sticky=tk.W+tk.S +
                  tk.N+tk.E, padx=(20, 20), columnspan=2)
    dropdown.bind("<<ComboboxSelected>>", updateUI)
    pathContent = tk.Text(newWindow, height=1, width=35, font=myFont)
    pathContent.grid(row=4, column=0, pady=10,
                     padx=(20, 20), sticky=tk.W+tk.S +
                     tk.N+tk.E, columnspan=2)
    pathContent.insert(tk.END, 'HKEY_CURRENT_CONFIG\\test\\test-a-2\\test-c-1')
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
    typeContent['values'] = ("Kiểu dữ liệu", "String",
                             "Binary", "DWORD", "QWORD", "Multi-String", "Extendable String")
    typeContent.current(0)
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
    deleteBtn.grid(row=9, column=1, pady=10, padx=(0, 20), sticky=tk.W+tk.E)
    # else:
    #     showConnectionError()


def exitRequest():
    global connected
    if connected:
        global client
        client.sendall(bytes("-exit-", "utf8"))
        client.close()
        if os.path.exists("snapshot.png"):
            os.remove("snapshot.png")
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


def on_closing():
    if tkmes.askokcancel("Quit", "Do you want to quit?"):
        exitRequest()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
