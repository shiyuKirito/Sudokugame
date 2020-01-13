import wx
import suduku,register,login
import pymysql

class indexFrame(wx.Frame):
    def __init__(self, parent, title):
        Fshow  = wx.Frame.__init__(self, parent, title=title, size=(600, 400))
        panel = wx.Panel(self)
        self.Center()
        a = wx.Button(panel, pos=(200, 200), size=(75,75), label='注册').Bind(wx.EVT_BUTTON, self.Onclickregister)
        b = wx.Button(panel, pos=(300, 200), size=(75,75), label='登陆').Bind(wx.EVT_BUTTON, self.Onclicklogin)
        x = wx.BoxSizer(wx.VERTICAL)
        # boxsize.Add(a,0,wx.EXPAND)
        # boxsize.Add(b,0,wx.EXPAND)

    def Onclicklogin(self, event):
        self.Close()
        login_frame = login.loginFrame(parent=None, title='登录')
        login_frame.Show()
    
    def Onclickregister(self, event):
        self.Close()
        registerFrame = register.registerFrame(parent=None, title='注册')
        registerFrame.Show()

if __name__ == '__main__':
    app = wx.App()
    indexFrame = indexFrame(parent=None, title='欢迎')
    indexFrame.Show()
    app.MainLoop()
