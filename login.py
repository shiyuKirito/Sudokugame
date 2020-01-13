import wx
import suduku,register,index,peo,time
import pymysql

class loginFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(600, 400))
        panel = wx.Panel(self)
        self.Center()
        wx.Button(panel, pos=(0,0),label='返回').Bind(wx.EVT_BUTTON, self.Onclickback)
        self.login_user = wx.StaticText(panel, label='用户名', pos=(100, 95))
        self.login_password = wx.StaticText(panel, label='密  码', pos=(100, 135))
        wx.StaticText(panel, label='还没有账户，赶紧来注册一个->',pos=(100,300))
        wx.Button(panel, pos=(300, 300), label='这就去注册').Bind(wx.EVT_BUTTON, self.Onclickregister)
        self.user = wx.TextCtrl(panel, pos=(150, 90), size=(300, 25), style=wx.TE_LEFT)
        self.password = wx.TextCtrl(panel, pos=(150, 130), size=(300, 25), style=wx.TE_PASSWORD)  # 控制TextCtrl
       # self.CreateStatusBar()    # 创建位于窗口的底部的状态栏
        self.login_bt = wx.Button(panel, pos=(170, 200), label='确定')
        self.cancel_bt = wx.Button(panel, pos=(270, 200), label='清空')
        self.login_bt.Bind(wx.EVT_BUTTON, self.Onclicklogin)
        self.cancel_bt.Bind(wx.EVT_BUTTON, self.Onclickcancel)
        self.falg = 1
        try:
            f2 = open("relogin.txt", "r")
            s1 = f2.read()
            self.user.SetValue(s1)
        except Exception as  e:
            pass
    
    def Onclicklogin(self, event):
        user = self.user.GetValue()
        password = self.password.GetValue()
        try:
            conn = pymysql.connect(host = '192.168.43.213', user = 'root', password = 'root', database = 's1', port = 3306, charset='utf8')
            cur = conn.cursor()
            print(conn)
            sql = "select password from user where uid = '"+user+"'"
            print(sql)
            cur.execute(sql)
            results = cur.fetchall()
            print(password)
            if not results:
                wx.MessageBox("账号或者密码错误", "提示",wx.YES_NO | wx.ICON_QUESTION)
            elif results[0][0] == password:
                self.Close()
                s1 = peo.peoFrame(parent=None, title='个人信息',user=self.user.GetValue())
                s1.Show()
                f1 = open("loginlog.txt", "a")
                f1.write(time.strftime("%Y:%m:%d:%H:%M:%S")+" 账户： "+user+'登陆成功')
                f1.write('\r\n')
                f1.close()
                f2 = open("relogin.txt", "w")
                f2.write(user)
                f2.close()
                print("登录成功")
            else:
                f1 = open("loginlog.txt", "a")
                wx.MessageBox("账号或者密码错误", "提示",wx.YES_NO | wx.ICON_QUESTION)
                f1.write(time.strftime("%H:%M:%S")+user+'登陆失败')
                f1.write('\r\n')
                f1.close()
        except Exception as e:
            print(e) 
        finally:
            conn.close()

    def Onclickcancel(self, event):
        self.user.SetValue('')
        self.password.SetValue('')
    
    def Onclickregister(self, event):
        self.Close()
        registerFrame = register.registerFrame(parent=None, title='注册')
        registerFrame.Show()
        # indexFrame.Show()
    def Onclickback(self, event):
        self.Close()
        indexFrame = index.indexFrame(parent=None, title='欢迎')
        indexFrame.Show()
    

if __name__ == '__main__':
    app = wx.App()
    login_frame = loginFrame(parent=None, title='登录')
    login_frame.Show()
    app.MainLoop()