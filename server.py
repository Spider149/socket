import socket
from PIL import ImageGrab
import base64
import os

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
        else:
            print(encodedData)
            # chỉ để test các request chưa code :v
            conn.sendall(bytes(encodedData+"ed", "utf8"))
except KeyboardInterrupt:
    conn.close()
finally:
    conn.close()
