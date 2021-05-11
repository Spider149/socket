import socket
from PIL import ImageGrab
import base64
import os
import winreg
import psutil
import subprocess

HOST = "127.0.0.1"
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print("Waiting for Client")
conn, addr = s.accept()

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

try:
    print("Connected by ", addr)
    while True:
        data = conn.recv(1024)
        encodedData = data.decode("utf8")
        if encodedData == "*snap*":
            snapshot = ImageGrab.grab()  # Take snap
            file = "scr.jpg"
            snapshot.save(file)
            f = open('scr.jpg', 'rb')  # Open file in binary mode
            dataImg = f.read()
            dataImg = base64.b64encode(dataImg)  # Convert binary to base 64
            f.close()
            os.remove(file)  # Remove the snap
            conn.sendall(dataImg)
        elif encodedData == "-hello-":
            # khi client bắt đầu connect gửi qua, nhận đc cái này thì trả về để client biết đã connect
            conn.sendall(bytes("-connected-", "utf8"))
        elif encodedData == "-exit-":  # nhận cái này thì đóng sv luôn
            conn.close()
            break
        elif encodedData == "*close*":
            os.system("shutdown /s /t 1")
        elif encodedData[0] == "1":
            splitPoint = encodedData.index("***")
            rootSplit = encodedData.index("\\")
            rootKey = encodedData[1:rootSplit]
            subKey = encodedData[rootSplit+1:splitPoint]
            value = encodedData[splitPoint+3:]
            try:
                accessKey = winreg.OpenKey(keyDic.get(rootKey), subKey)
                result = winreg.QueryValueEx(accessKey, value)
                if result[1] == 1 or result[1] == 2:
                    conn.sendall(bytes(result[0], "utf8"))
                elif result[1] == 4 or result[1] == 11:
                    conn.sendall(bytes(str(result[0]), "utf8"))
                elif result[1] == 3:
                    data = ""
                    for byte in result[0]:
                        data = data+str(byte)+" "
                    conn.sendall(bytes(data, "utf8"))
                elif result[1] == 7:
                    data = ""
                    for string in result[0]:
                        data = data+string+"\n"
                    conn.sendall(bytes(data, "utf8"))
            except:
                conn.sendall(bytes("Lỗi", "utf8"))
        elif encodedData[0] == "2":
            splitPoint1 = encodedData.index("**")
            splitPoint2 = encodedData.index("***")
            splitPoint3 = encodedData.index("****")
            rootSplit = encodedData.index("\\")
            rootKey = encodedData[1:rootSplit]
            subKey = encodedData[rootSplit+1:splitPoint1]
            nameValue = encodedData[splitPoint1+2:splitPoint2]
            newValue = encodedData[splitPoint2+3:splitPoint3]
            typeValue = encodedData[splitPoint3+4:]
            try:
                accessKey = winreg.OpenKey(
                    keyDic.get(rootKey), subKey, 0, winreg.KEY_SET_VALUE)
                if typeValue == "Binary":
                    newValue = bytearray(newValue, "utf8")
                elif typeValue == "DWORD" or typeValue == "QWORD":
                    newValue = int(newValue)
                elif typeValue == "Multi-String":
                    newValue = newValue.split("\n")
                winreg.SetValueEx(accessKey, nameValue, 0,
                                  typeDic.get(typeValue), newValue)
                conn.sendall(bytes("Đã sửa giá trị thành công", "utf8"))
            except:
                conn.sendall(bytes("Lỗi", "utf8"))
        elif encodedData[0] == "3":
            splitPoint = encodedData.index("***")
            rootSplit = encodedData.index("\\")
            rootKey = encodedData[1:rootSplit]
            subKey = encodedData[rootSplit+1:splitPoint]
            value = encodedData[splitPoint+3:]
            try:
                accessKey = winreg.OpenKey(
                    keyDic.get(rootKey), subKey, 0, winreg.KEY_WRITE)
                winreg.DeleteValue(accessKey, value)
                conn.sendall(bytes("Xóa value thành công", "utf8"))
            except:
                conn.sendall(bytes("Lỗi", "utf8"))
        elif encodedData[0] == "4":
            rootSplit = encodedData.index("\\")
            rootKey = encodedData[1:rootSplit]
            subKey = encodedData[rootSplit+1:]
            try:
                winreg.CreateKey(keyDic.get(rootKey), subKey)
                conn.sendall(bytes("Tạo key thành công", "utf8"))
            except:
                conn.sendall(bytes("Lỗi", "utf8"))
        elif encodedData[0] == "5":
            rootSplit = encodedData.index("\\")
            rootKey = encodedData[1:rootSplit]
            subKey = encodedData[rootSplit+1:]
            try:
                winreg.DeleteKey(keyDic.get(rootKey), subKey)
                conn.sendall(bytes("Xóa key thành công", "utf8"))
            except:
                conn.sendall(bytes("Lỗi", "utf8"))
        elif encodedData[0] == "6":
            fileContent = encodedData[1:]
            f = open("xyzijk.reg", "w")
            f.seek(0)
            f.write(fileContent)
            f.truncate()
            f.close()
            if os.system("reg import xyzijk.reg") == 0:
                os.remove("xyzijk.reg")
                conn.sendall(bytes("s", "utf8"))
            else:
                conn.sendall(bytes("f", "utf8"))

        elif encodedData == "see_process":
            res_final = []
            for pro in psutil.process_iter():
                # conn.sendall(bytes("during","utf8"))
                res = str(pro.name().replace('.exe', '')) + "__" + \
                    str(pro.pid) + "__" + str(pro.num_threads())
                res_final.append(res)
                #check_recv = conn.recv(1024)
            str_send = "_a_".join(res_final)
            conn.sendall(bytes(str_send, "utf8"))
        elif encodedData == "kill_process":
            ID_str = conn.recv(1024).decode("utf8")
            ID_kill = int(ID_str)
            #print(ID_kill, " da chuyen")
            check_kill_comp = False
            for pro in psutil.process_iter():
                if pro.pid == ID_kill:
                    pro.kill()
                    print(pro.pid)
                    conn.sendall(bytes("kill_success", "utf8"))
                    check_kill_comp = True
                    break
            if not check_kill_comp:
                conn.sendall(bytes("kill_fail", "utf8"))

        elif encodedData == "start_process" or encodedData == "start_app":
            Name_start = conn.recv(1024).decode("utf8")
            try:
                subprocess.Popen(Name_start)
                conn.sendall(bytes("success", "utf8"))
            except:
                conn.sendall(bytes("error", "utf8"))

        elif encodedData == "see_app":
            cmd = 'powershell "gps | where {$_.MainWindowTitle } | select ProcessName,Id'
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            res = []
            for line in proc.stdout:
                if line.rstrip():
                    # only print lines that are not empty
                    # decode() is necessary to get rid of the binary string (b')
                    # rstrip() to remove `\r\n`
                    name = line.decode().rstrip()
                    res.append(name)
            res = res[2:]
            ID_res = []
            for text in res:
                #print(text[0:text.find(" ",0,len(text))])
                ID_res.append(
                    int(text[text.find(" ", 0, len(text)):len(text)].strip(" ")))
            res_final = []
            for pro in psutil.process_iter():
                # conn.sendall(bytes("during","utf8"))
                if pro.pid in ID_res:
                    res = str(pro.name().replace('.exe', '')) + "__" + \
                        str(pro.pid) + "__" + str(pro.num_threads())
                    res_final.append(res)
                #check_recv = conn.recv(1024)
            str_send = "_a_".join(res_final)
            conn.sendall(bytes(str_send, "utf8"))
        elif encodedData == "kill_app":
            cmd = 'powershell "gps | where {$_.MainWindowTitle } | select ProcessName,Id'
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            res = []
            for line in proc.stdout:
                if line.rstrip():
                    # only print lines that are not empty
                    # decode() is necessary to get rid of the binary string (b')
                    # rstrip() to remove `\r\n`
                    name = line.decode().rstrip()
                    res.append(name)
            res = res[2:]
            ID_res = []
            for text in res:
                #print(text[0:text.find(" ",0,len(text))])
                ID_res.append(
                    int(text[text.find(" ", 0, len(text)):len(text)].strip(" ")))
            ID_str = conn.recv(1024).decode("utf8")
            ID_kill = int(ID_str)
            #print(ID_kill, " da chuyen")
            if ID_kill in ID_res:
                check_kill_comp = False
                for pro in psutil.process_iter():
                    if pro.pid == ID_kill:
                        pro.kill()
                        print(pro.pid)
                        conn.sendall(bytes("kill_success", "utf8"))
                        check_kill_comp = True
                        break
                if not check_kill_comp:
                    conn.sendall(bytes("kill_fail", "utf8"))
            else:
                conn.sendall(bytes("kill_fail", "utf8"))

        elif encodedData == "hook":
            continue
        elif encodedData == "unhook":
            continue
        elif encodedData == "printkey":
            continue

except KeyboardInterrupt:
    conn.close()
finally:
    conn.close()
