import tkinter as tk
import tkinter.messagebox as tkmes
import tkinter.filedialog as tkdilg
import socket
import base64
import os
import shutil as sm

root = tk.Tk()
root.title("Client")

root.minsize(340, 250)
connected = False


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
    port = 65432
    server_address = (host, port)
    print("Client connect to server with port: " + str(port))
    global client
    client.connect(server_address)
    client.sendall(bytes("-hello-", "utf8"))
    data = client.recv(1024).decode("utf8")
    try:
        if data == "-connected-":
            print("connected")
            tkmes.showinfo(title="Success",
                           message="Kết nối thành công")
            global connected
            connected = True
    except:
        tkmes.showerror(tittle="Error", message="Kết nối thất bại")


def takeScreen():
    global client
    client.sendall(bytes("*snap*", "utf8"))
    data = client.recv(1024*1024)
    image = base64.b64decode(data)
    f = open('snapshot.png', 'wb')
    f.write(image)
    f.close()


def saveImg():
    filename = tkdilg.asksaveasfilename()
    #sm.move("snapshot.png", filename)
    print(filename)
    sm.move("snapshot.png", filename)


def takeScreenshotRequest():
    global connected
    if connected:
        print("take screen")
        newWindow = tk.Toplevel(root)
        createNewWindow(newWindow, "Screenshot")
        snapBtn = tk.Button(newWindow, text="Chụp",
                            command=takeScreen)
        snapBtn.grid(row=0, column=0, sticky=tk.W+tk.N +
                     tk.S+tk.E, pady=(0, 20), padx=(0, 10))
        saveImgBtn = tk.Button(newWindow, text="Lưu",
                               command=saveImg)
        saveImgBtn.grid(row=0, column=1, sticky=tk.W+tk.N +
                        tk.S+tk.E, pady=(0, 20), padx=(0, 10))
    else:
        showConnectionError()


def processRunningRequest():
    global connected
    if connected:
        print("process running")
        newWindow = tk.Toplevel(root)
        createNewWindow(newWindow, "Process Running")
        global client
        client.sendall(bytes("process", "utf8"))
        data = client.recv(1024).decode("utf8")
        print(data)
        filename = tkdilg.askopenfilename()
        print(filename)  # test
    else:
        showConnectionError()


def appRunningRequest():
    global connected
    if connected:
        print("app running")
        newWindow = tk.Toplevel(root)
        createNewWindow(newWindow, "App Running")
    else:
        showConnectionError()


def closeRequest():
    global connected
    if connected:
        print("close")
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
    global connected
    if connected:
        print("registry")
        newWindow = tk.Toplevel(root)
        createNewWindow(newWindow, "Registry")
    else:
        showConnectionError()


def exitRequest():
    global connected
    if connected:
        global client
        client.sendall(bytes("-exit-", "utf8"))
        client.close()
    root.destroy()


labelIP = tk.Label(root, text="Nhập IP:")
labelIP.grid(row=0, column=0, pady=20, sticky=tk.W +
             tk.S+tk.N+tk.E, padx=(20, 10))

entryIP = tk.Entry(root)
entryIP.grid(row=0, column=1, pady=20, sticky=tk.W +
             tk.S+tk.N+tk.E, padx=(0, 10))

ipBtn = tk.Button(root, text="Nhập", command=submitIP)
ipBtn.grid(row=0, column=2, sticky=tk.W+tk.S +
           tk.N+tk.E+tk.E, pady=20, padx=(0, 10))

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
