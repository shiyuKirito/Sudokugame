import MySQL,time
import wx,login,suduku
import socket,peo
import time
# def Tcp_Rev(adip):
#     ip1 = '192.168.43.213'
#     ip2 = '192.168.43.213'
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tcp
#     addr = (adip,5005)
#     s.bind(addr)
#     s.listen()
#     try:
#         while True:
#             c = s.accept()[0].recv(1024)
#             if c == 'close':
#                 break
#             print(c.decode('utf8'))
#         s.close()
#     except Exception as e:
#         print(e)

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tcp
    addr = ('localhost', 5009)
    s.connect(addr)
    return s

def Tcp_Send(s1,adip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tcp
    print("addr"+adip)
    print(adip)
    addr = (adip, 5009)
    s.connect(addr)
    s.send(s1.encode('utf8'))
    s.close()

def Toplay():
    cnt = 0
    sql = 'select * from usertmp'
    mysql = MySQL.mysql()
    res = mysql.newselect(sql)
    print(len(res))
    if len(res) >=2:
        cnt+=1
        sql = "insert into userplay values('" + res[0][0] + "','" + res[1][0] + "','" + str(cnt) + "','"+res[0][1]+ "','"+res[1][1]+"')"
        print(sql)
        mysql.newupdate(sql)
        sql = "delete from usertmp where user_ready='"+res[0][0]+"'"
        print(sql)
        mysql.newupdate(sql)
        sql = "delete from usertmp where user_ready='"+res[1][0]+"'"
        print(sql)
        mysql.newupdate(sql)

def GetLocalIPByPrefix(prefix):
    localIP = ''
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if ip.startswith(prefix):
            localIP = ip
    return localIP
if __name__ == "__main__":
    s = GetLocalIPByPrefix('192.168.43')
    print(s)
    while True:
        Toplay()

    



