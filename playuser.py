import MySQL,time
import wx,login,suduku
import socket,peo
from threading import Thread

class MainFrame(wx.Frame):
    def __init__(self, parent, title, user):
        wx.Frame.__init__(self, parent, title = title, size = (600, 600))
        s = MySQL.mysql()
        self.panel = wx.Panel(self)
        self.user= user
        self.Center()
        self.buttonReady = wx.Button(self.panel, pos=(110, 30),label='准备',size=(60,60)).Bind(wx.EVT_BUTTON,self.buttonReadyOnclik1)
        self.font1 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.Bind(wx.EVT_CLOSE, self.Onclose)
        self.flag = 0
        self.startgame = 0
        list_peo = list()
        list_peo.append('名称:')
        list_peo.append('胜场:')
        list_peo.append('总场:')
        list_peo.append('分数:')
        list_peo.append('段位:')
        self.font2 = wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        results = list()
        sql = "select uname from user where uid = '" +user+ "'"
        results.append(s.newselect(sql)[0])
        sql = "select Wincnt from user where uid = '" +user+ "'"
        results.append(s.newselect(sql)[0])
        sql = "select ALLcnt from user where uid = '" +user+ "'"
        results.append(s.newselect(sql)[0])
        sql = "select rankcnt from user where uid = '" +user+ "'"
        results.append(s.newselect(sql)[0])
        sql = "select rankValue from user,user_rank where user.uid = '"+user+"' and user.rankID = user_rank.rankID"
        results.append(s.newselect(sql)[0])
        for i in range(0,5):
            wx.StaticText(self.panel, label=list_peo[i],pos=(450,i*20)).SetFont(self.font2)
            wx.StaticText(self.panel, label=str(results[i][0]),pos=(500,i*20)).SetFont(self.font2)
            print(results[i][0])
    
    def init0(self):
        s = MySQL.mysql()
        self.font1 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.Bind(wx.EVT_CLOSE, self.Onclose)
        self.flag = 0
        self.startgame = 0
        list_peo = list()
        list_peo.append('名称:')
        list_peo.append('胜场:')
        list_peo.append('总场:')
        list_peo.append('分数:')
        list_peo.append('段位:')
        self.font2 = wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        results = list()
        sql = "select uname from user where uid = '" +self.user+ "'"
        results.append(s.newselect(sql)[0])
        sql = "select Wincnt from user where uid = '" +self.user+ "'"
        results.append(s.newselect(sql)[0])
        sql = "select ALLcnt from user where uid = '" +self.user+ "'"
        results.append(s.newselect(sql)[0])
        sql = "select rankcnt from user where uid = '" +self.user+ "'"
        results.append(s.newselect(sql)[0])
        sql = "select rankValue from user,user_rank where user.uid = '"+self.user+"' and user.rankID = user_rank.rankID"
        results.append(s.newselect(sql)[0])
        for i in range(0,5):
            wx.StaticText(self.panel, label=list_peo[i],pos=(450,i*20)).SetFont(self.font2)
            wx.StaticText(self.panel, label=str(results[i][0]),pos=(500,i*20)).SetFont(self.font2)
            print(results[i][0])

    def ingame(self):
        while True:
            if self.flag == 0:
                break
            sql = 'select * from userplay'
            mysql = MySQL.mysql()
            res = mysql.newselect(sql)
            for i in res:
                if self.flag == 0:
                    break
                if i[0]==self.user or i[1]==self.user:
                    self.flag = 0
                    self.startgame = 1
                
    def GetLocalIPByPrefix(self,prefix):
        localIP = ''
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if ip.startswith(prefix):
                localIP = ip
        return localIP

    def buttonReadyOnclik1(self, event):
        self.init0()
        self.flag = 1
        self.panel.DestroyChildren()
        self.buttonReady = wx.Button(self.panel, pos=(110, 30),label='取消准备',size=(60,60)).Bind(wx.EVT_BUTTON,self.buttonReadyOnclik2)
        s = MySQL.mysql()
        addr = self.GetLocalIPByPrefix('192.168.43')
        sql = "insert into usertmp values('"+self.user+"','"+addr+"')"
        print(sql)
        s.newupdate(sql)
        self.thread_OnlyNum= Thread(target=self.ingame)
        self.thread_OnlyNum.start()
        while self.flag != 0:
            if self.startgame == 1:
                self.startgame = 0
                s1 = suduku.MainWindow(parent=None,title='匹配模式',nlist=90,user=self.user)
                s1.Show()
                self.Destroy()
                break


    def Onclose(self, event):
        self.flag = 0
        print("close")
        try:
            s = MySQL.mysql()
            sql = "delete from usertmp where user_ready='"+self.user+"'"
            s.newupdate(sql)
        except expression as  e:
            print('1111')
            print(e)
        finally:
            s1 = peo.peoFrame(parent=None, title='个人信息',user=self.user)
            s1.Show()
            self.Destroy()

    def buttonReadyOnclik2(self, event):
        self.startgame = 0
        self.falg = 0
        self.panel.DestroyChildren()
        self.buttonReady = wx.Button(self.panel, pos=(110, 30), size=(60,60), label='准备').Bind(wx.EVT_BUTTON,self.buttonReadyOnclik1)
        try:
            s = MySQL.mysql()
            sql = "delete from usertmp where user_ready='"+self.user+"'"
            s.newupdate(sql)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app= wx.App()
    MainFrame = MainFrame(parent=None, user='123',title='匹配模式')
    MainFrame.Show()
    app.MainLoop()
