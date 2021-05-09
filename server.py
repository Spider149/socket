import socket
from PIL import ImageGrab
import base64
import os
import winreg
import psutil

HOST = "127.0.0.1"
PORT = 54321

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print("Waiting for Client")
conn, addr = s.accept()
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
            # khi clientbắt đầu connect gửi qua,nhận đc cái này thì trả về để client biết đã connect
            conn.sendall(bytes("-connected-", "utf8"))
        elif encodedData == "-exit-":  # nhận cái này thì đóng sv luôn
            conn.close()
            print("Close server")
            break
        elif encodedData == "*close*":
            print("Shutdown")
            os.system("shutdown /s /t 1")
        elif encodedData[0] == "1":
            splitPoint = encodedData.index("***")
            rootSplit = encodedData.index("\\")
            rootKey = encodedData[1:rootSplit]
            subKey = encodedData[rootSplit+1:splitPoint]
            value = encodedData[splitPoint+3:]
            accessKey = None
            try:
                if rootKey == "HKEY_CURRENT_CONFIG":
                    accessKey = winreg.OpenKey(
                        winreg.HKEY_CURRENT_CONFIG, subKey)

                elif rootKey == "HKEY_CLASSES_ROOT":
                    accessKey = winreg.OpenKey(
                        winreg.HKEY_CLASSES_ROOT, subKey)
                elif rootKey == "HKEY_CURRENT_USER":
                    accessKey = winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER, subKey)

                elif rootKey == "HKEY_DYN_DATA":
                    accessKey = winreg.OpenKey(
                        winreg.HKEY_DYN_DATA, subKey)

                elif rootKey == "HKEY_LOCAL_MACHINE":
                    accessKey = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE, subKey)

                elif rootKey == "HKEY_PERFORMANCE_DATA":
                    accessKey = winreg.OpenKey(
                        winreg.HKEY_PERFORMANCE_DATA, subKey)

                elif rootKey == "HKEY_USERS":
                    accessKey = winreg.OpenKey(
                        winreg.HKEY_USERS, subKey)
                result = winreg.QueryValueEx(accessKey, value)
                if result[1] == 1 or result[1] == 2:
                    conn.sendall(bytes(result[0], "utf8"))
                elif result[1] == 4 or result[1] == 11:
                    conn.sendall(bytes(str(result[0]), "utf8"))
                elif result[1] == 3:
                    conn.sendall(result[0])
                elif result[1] == 7:
                    conn.sendall(bytes(result[0][0], "utf8"))
            except:
                conn.sendall(bytes("Lỗi\n", "utf8"))
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
                    winreg.HKEY_CURRENT_CONFIG, subKey, 0, winreg.KEY_SET_VALUE)
                typeArg = None
                if typeValue == "String":
                    typeArg = winreg.REG_SZ
                elif typeValue == "Binary":
                    typeArg = winreg.REG_BINARY
                elif typeValue == "DWORD":
                    typeArg = winreg.REG_DWORD
                elif typeValue == "QWORD":
                    typeArg = winreg.REG_QWORD
                elif typeValue == "Multi-String":
                    typeArg = winreg.REG_MULTI_SZ
                elif typeValue == "Extendable String":
                    typeArg = winreg.REG_EXPAND_SZ
                winreg.SetValueEx(accessKey, nameValue, 0,
                                  typeArg, newValue)
                conn.sendall(bytes("Đã sửa giá trị thành công", "utf8"))
            except:
                conn.sendall(bytes("Lỗi\n", "utf8"))

        else:
            print(encodedData)
            # chỉ để test các request chưa code :v
            conn.sendall(bytes(encodedData+"ed", "utf8"))
except KeyboardInterrupt:
    conn.close()
finally:
    conn.close()
