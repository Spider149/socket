import tkinter as tk
import tkinter.messagebox as tkmes
import tkinter.filedialog as tkdilg
from PIL import ImageTk, Image
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
            sm.move("snapshot.png", filename)

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
    # global connected
    # if connected:
    print("registry")
    newWindow = tk.Toplevel(root)
    createNewWindow(newWindow, "Registry")
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
