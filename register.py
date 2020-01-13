import wx
import pymysql,index


class registerFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(600, 400))
        self.panel = wx.Panel(self)
        self.Center()
        self.login_user = wx.StaticText(self.panel, label='用户名', pos=(100, 95))
        self.login_password = wx.StaticText(self.panel, label='密  码', pos=(100, 135))
        self.login_repassword = wx.StaticText(self.panel, label='重复输入密码', pos=(70, 175))
        self.login_name = wx.StaticText(self.panel, label='姓 名', pos=(100, 215))
        self.user = wx.TextCtrl(self.panel, pos=(150, 90), size=(300, 25), style=wx.TE_LEFT)
        self.password = wx.TextCtrl(self.panel, pos=(150, 130), size=(300, 25), style=wx.TE_PASSWORD)  # 控制TextCtrl
        self.repassword = wx.TextCtrl(self.panel, pos=(150, 170), size=(300, 25), style=wx.TE_PASSWORD)  # 控制TextCtrl
        self.name = wx.TextCtrl(self.panel, pos=(150, 210), size=(300, 25), style=wx.TE_LEFT)
       # self.CreateStatusBar()    # 创建位于窗口的底部的状态栏
        self.login_bt = wx.Button(self.panel, pos=(170, 240), label='注册')
        self.cancel_bt = wx.Button(self.panel, pos=(270, 240), label='清空')
        self.login_bt.Bind(wx.EVT_BUTTON, self.Onclicklogin)
        self.cancel_bt.Bind(wx.EVT_BUTTON, self.Onclickcancel)
        wx.Button(self.panel, pos=(0,0),label='返回').Bind(wx.EVT_BUTTON, self.Onclickback)

    def Onclicklogin(self, parent):
        user = self.user.GetValue()
        password = self.password.GetValue()
        name = self.name.GetValue()
        if self.check()==0:
            return
        try:
            conn = pymysql.connect(host = '192.168.43.213', user = 'root', password = 'root', database = 's1', port = 3306, charset='utf8')
            cur = conn.cursor()
            sql = "insert into user  values('{}','{}','{}','1','0','0','0')".format(user,password,name)
            print(sql)
            cur.execute(sql)
            conn.commit()
            wx.MessageBox("注册成功", "提示",wx.YES_NO | wx.ICON_QUESTION)
            print(sql)
        except Exception as e:
            wx.MessageBox("账号重复", "提示",wx.YES_NO | wx.ICON_QUESTION)
            print(e)
        finally:
            conn.close()

    def Onclickcancel(self, event):
        self.user.SetValue('')
        self.password.SetValue('')
        self.repassword.SetValue('')
        self.name.SetValue('')
    
    def check(self):
        user = self.user.GetValue()
        password = self.password.GetValue()
        repassword = self.repassword.GetValue()
        name = self.repassword.GetValue()
        if password != repassword:
            wx.MessageBox("俩次密码输入不一致", "提示",wx.YES_NO | wx.ICON_QUESTION)
            self.password.SetValue('')
            self.repassword.SetValue('')
            return 0
        if user == "":
            wx.StaticText(self.panel, label='用户名不能为空', pos=(460, 95))
            return 0
        if password == "":
            wx.StaticText(self.panel, label='密码不能为空', pos=(460, 135))
            return 0
        if name == "":
            wx.StaticText(self.panel, label='姓名不能为空', pos=(460, 215))
            return 0
        return 1
    def Onclickback(self,event):
        self.Close()
        indexFrame = index.indexFrame(parent=None, title='欢迎')
        indexFrame.Show()

# if __name__ == '__main__':
#     app = wx.App()
#     indexFrame = indexFrame(parent=None, title='注册')
#     indexFrame.Show()
#     app.MainLoop()         
