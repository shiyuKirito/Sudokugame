import MySQL
import wx,login,suduku
import playuser,suduku

class peoFrame(wx.Frame):

    def __init__(self, parent, title, user):
        wx.Frame.__init__(self, parent, title=title, size=(600, 400))
        panel = wx.Panel(self)
        self.Center()
        self.user= user
        s = MySQL.mysql()
        list_peo = list()
        list_peo.append('名称:')
        list_peo.append('胜场:')
        list_peo.append('总场:')
        list_peo.append('分数:')
        list_peo.append('段位:')
        self.font1 = wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.font2 = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        wx.StaticText(panel, label='单机模式',pos=(0,50)).SetFont(self.font2)
        wx.StaticText(panel, label='匹配模式',pos=(0,150)).SetFont(self.font2)
        self.b3x3start = wx.Button(panel, pos=(110, 30), size=(60,60), label='3x3').Bind(wx.EVT_BUTTON, self.b3x3do)
        self.b9x9start = wx.Button(panel, pos=(200, 30), size=(60,60), label='9x9').Bind(wx.EVT_BUTTON, self.b9x9do)
        self.a9x9start = wx.Button(panel, pos=(110, 130), size=(60,60), label='9x9').Bind(wx.EVT_BUTTON, self.a9x9do)
        # self.Textreadly = wx.StaticText(panel, pos=(110, 130), size=(60,60), label='')
        wx.Button(panel, pos=(0, 330), size=(70,30), label='返回').Bind(wx.EVT_BUTTON, self.onback)
        # self.font1 = wx.Font(, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
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
            wx.StaticText(panel, label=list_peo[i],pos=(450,i*20)).SetFont(self.font1)
            wx.StaticText(panel, label=str(results[i][0]),pos=(500,i*20)).SetFont(self.font1)
            print(results[i][0])
    
    def a9x9do(self,event):
        self.Close()
        s1 = playuser.MainFrame(parent=None,title='匹配界面',user=self.user)
        s1.Show()

    def b3x3do(self,event):
        self.Close()
        s1 = suduku.MainWindow(parent=None, title='主界面',nlist=3,user=self.user)
        s1.Show()
    
    def b9x9do(self,event):
        self.Close()
        s1 = suduku.MainWindow(parent=None, title='主界面',nlist=9,user=self.user)
        s1.Show()
    
    def onback(self,event):
        self.Close()
        s1 = login.loginFrame(parent=None, title='主界面')
        s1.Show()

# if __name__ == '__main__':
#     app = wx.App()
#     peoFrame = peoFrame(parent=None, title='个人信息',user='text')
#     peoFrame.Show()
#     app.MainLoop()