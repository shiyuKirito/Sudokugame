import wx
import createsudu,random,peo
import MySQL,socket
import server
from threading import Thread


class MainWindow(wx.Frame):
    """We simply derive a new class of Frame."""
    cnt_num = 0
    row_list = list()
    row = list()
    ans = set()
    nsize = 3 
    toip = 0
    resnum = 0
    def __init__(self, parent, title, nlist,user):
        self.user = user
        if nlist == 3:
            self.nsize = nlist
            wx.Frame.__init__(self, parent, title = title, size = (600, 600))
            self.font1 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
            panel = wx.Panel(self, -1) # 布局
            # self.control = wx.TextCtrl(panel, pos =(20,20), size=(50,50),style = wx.TE_CENTER)  # 控制TextCtrl
            self.list_text_id = list()
            list_tmp_num = self.Num(3)
            rnum = random.randint(3,5)
            # print(rnum)
            cntnum = 0
            stmp = 0
            for i in range(0,3): #  0 1 2 
                for j in range(0,3): # 0 1 2
                    s = random.randint(stmp,5)
                    if s > 2 and rnum>0:
                        stmp=0
                        rnum -=1
                        text = wx.TextCtrl(panel, wx.ID_ANY, pos=(90+i*120,50+j*120), size =(50, 50), style = wx.TE_READONLY|wx.TE_CENTER)
                        text.SetValue(str(list_tmp_num[int(i*3+j)]))
                        text.SetFont(self.font1)
                        text.SetMaxLength(1)
                        self.list_text_id.append(text.GetId())                   
                    else:
                        stmp+=1
                        text = wx.TextCtrl(panel, wx.ID_ANY, pos=(90+i*120,50+j*120), size =(50, 50), style = wx.TE_CENTER)
                        text.SetFont(self.font1)
                        text.SetMaxLength(1)
                        self.list_text_id.append(text.GetId())
                    self.row.append(text.GetId())
                self.row_list.append(self.row)
        elif nlist == 9:
            self.nsize = nlist
            wx.Frame.__init__(self, parent, title = title, size = (1000, 700))
            self.font1 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
            panel = wx.Panel(self, -1) 
            self.list_text_id = list()
            list_tmp_num = self.Num(9)
            rnum = random.randint(20,60)
            cntnum = 0
            stmp = 0
            for i in range(0,9):
                for j in range(0,9): 
                    s = random.randint(stmp,stmp+3)
                    if s > 2 and rnum>0:
                        stmp=0
                        rnum -=1
                        text = wx.TextCtrl(panel, wx.ID_ANY, pos=(30+i*50,30+j*50), size =(50, 50), style = wx.TE_READONLY|wx.TE_CENTER)
                        text.SetValue(str(list_tmp_num[i][j]))
                        text.SetFont(self.font1)
                        text.SetMaxLength(1)
                        self.list_text_id.append(text.GetId())                   
                    else:
                        stmp+=1
                        text = wx.TextCtrl(panel, wx.ID_ANY, pos=(30+i*50,30+j*50), size =(50, 50), style = wx.TE_CENTER)
                        text.SetFont(self.font1)
                        text.SetMaxLength(1)
                        self.list_text_id.append(text.GetId())
                    self.row.append(text.GetId())
                self.row_list.append(self.row)
        else:
            self.nsize = nlist
            wx.Frame.__init__(self, parent, title = title, size = (1000, 700))
            self.font1 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
            panel = wx.Panel(self, -1) # 布局
            self.list_text_id = list()
            list_tmp_num = self.Num(9)
            rnum = random.randint(20,60)
            mysql = MySQL.mysql()
            sql = "select * from userplay where usera = '"+self.user+"' or userb = '"+self.user+"'"
            res = mysql.newselect(sql)
            touser = 0
            if res[0][0] == self.user:
                touser = res[0][1]
                addr = res[0][3]
                self.toip=res[0][4]
            else:
                touser = res[0][0] 
                addr = res[0][4]
                self.toip=res[0][3]
            # self.toip='192.168.43.213'
            self.myip = addr
            s = MySQL.mysql()
            print('self.toip::'+self.toip)
            wx.StaticText(panel, label='名称', pos=(700,0)).SetFont(self.font1)
            sql = "select uname from user where uid = '" +user+ "'"
            wx.StaticText(panel, label=s.newselect(sql)[0][0], pos=(800,0)).SetFont(self.font1)
            wx.StaticText(panel, label='分数', pos=(700,30)).SetFont(self.font1)
            sql = "select rankcnt from user where uid = '" +user+ "'"
            wx.StaticText(panel, label=s.newselect(sql)[0][0], pos=(800,30)).SetFont(self.font1)
            wx.StaticText(panel, label='段位', pos=(700,60)).SetFont(self.font1)
            sql = "select rankValue from user,user_rank where user.uid = '"+self.user+"' and user.rankID = user_rank.rankID"
            wx.StaticText(panel, label=s.newselect(sql)[0][0], pos=(800,60)).SetFont(self.font1)
            self.thread_rev = Thread(target=self.Tcp_Rev,args=(self.toip,))
            self.thread_rev.start()
            self.mycnt = wx.TextCtrl(panel, wx.ID_ANY, pos=(700,100), size =(50, 50), style = wx.TE_READONLY|wx.TE_CENTER)
            self.mycnt.SetValue('0')
            self.mycnt.SetFont(self.font1)
            self.tocnt = wx.TextCtrl(panel, wx.ID_ANY, pos=(700,300), size =(50, 50), style = wx.TE_READONLY|wx.TE_CENTER)
            self.tocnt.SetValue('0')
            self.tocnt.SetFont(self.font1)
            wx.StaticText(panel, label='名称', pos=(700,200)).SetFont(self.font1)
            sql = "select uname from user where uid = '" +touser+ "'"
            wx.StaticText(panel, label=s.newselect(sql)[0][0], pos=(800,200)).SetFont(self.font1)
            wx.StaticText(panel, label='分数', pos=(700,230)).SetFont(self.font1)
            sql = "select rankcnt from user where uid = '" +touser+ "'"
            wx.StaticText(panel, label=s.newselect(sql)[0][0], pos=(800,230)).SetFont(self.font1)
            wx.StaticText(panel, label='段位', pos=(700,260)).SetFont(self.font1)
            sql = "select rankValue from user,user_rank where user.uid = '"+touser+"' and user.rankID = user_rank.rankID"
            wx.StaticText(panel, label=s.newselect(sql)[0][0], pos=(800,260)).SetFont(self.font1)
            cntnum = 0
            stmp = 0
            for i in range(0,9): #  0 1 2 
                for j in range(0,9): # 0 1 2
                    s = random.randint(stmp,stmp+3)
                    if s > 2 and rnum>0:
                        stmp=0
                        rnum -=1
                        text = wx.TextCtrl(panel, wx.ID_ANY, pos=(30+i*50,30+j*50), size =(50, 50), style = wx.TE_READONLY|wx.TE_CENTER)
                        text.SetValue(str(list_tmp_num[i][j]))
                        text.SetFont(self.font1)
                        text.SetMaxLength(1)
                        self.list_text_id.append(text.GetId())                   
                    else:
                        stmp+=1
                        text = wx.TextCtrl(panel, wx.ID_ANY, pos=(30+i*50,30+j*50), size =(50, 50), style = wx.TE_CENTER)
                        text.SetFont(self.font1)
                        text.SetMaxLength(1)
                        self.list_text_id.append(text.GetId())
                    self.row.append(text.GetId())
                self.row_list.append(self.row)
        self.Center()
        filemenu = wx.Menu()

        menuAbout = filemenu.Append(wx.ID_ABOUT, "About", " Information about this program")    
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "Exit", " Terminate the program")    

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "File")    
        self.SetMenuBar(menuBar)    

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        for i in self.list_text_id:
            objControl = self.FindWindowById(i)
            self.Bind(wx.EVT_TEXT, self.listennum, objControl) 

        self.Show(True)

    def Tcp_Rev(self, adip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        addr = (self.myip,5010)
        print(addr)
        s.bind(addr)
        s.listen(1)
        try:
            while True:
                conn,addr=s.accept()
                c = conn.recv(1024)
                if c == 'close':
                    break
                self.resnum = c.decode('utf8')
                print(self.resnum)
                self.tocnt.SetValue(self.resnum)
                conn.close()
        except Exception as e:
            print(e)

    def listennum(self,e):
        thread_Sucessjudge = Thread(target=self.Sucessjudge,args=(self.nsize,)) 
        thread_Sucessjudge.start()
        thread_OnlyNum= Thread(target=self.OnlyNum)
        thread_OnlyNum.start()
        self.cnt_num = 0
        for i in self.list_text_id:
            objControl = self.FindWindowById(i)    
            if objControl.GetValue() != '':
                self.cnt_num+=1
        self.mycnt.SetValue(str(self.cnt_num))
        server.Tcp_Send(str(self.cnt_num),self.toip)
    def OnlyNum(self):
        for i in self.list_text_id:
            objControl = self.FindWindowById(i)     
            if objControl.GetValue().isdigit() or objControl.GetValue() == "":
                print(objControl.GetValue())
            else:
                objControl.SetValue('')

    def Sucessjudge(self,n):
        self.ans.clear()
        if n == 3:
            for i in self.list_text_id:
                objControl = self.FindWindowById(i)     
                if objControl.GetValue() !='':
                    self.ans.add(objControl.GetValue())
            if len(self.ans) == n*n:
                print('Sucess')
                dlg = wx.MessageDialog(self,"Sucess")
                dlg.ShowModal()
                dlg.Destroy()
        else:
            cnt_cur = 0
            cnt_row = 0
            ans_tmp = set()
            text_numcur = list()
            text_numrow = list()
            for i in self.list_text_id:
                objControl = self.FindWindowById(i)     
                if objControl.GetValue() == '':
                    return
            for i in self.list_text_id:
                cnt_cur+=1
                objControl = self.FindWindowById(i)    
                text_numcur.append(objControl.GetValue())
                ans_tmp.add(objControl.GetValue())
                if cnt_cur == 9:
                    cnt_cur = 0
                    if len(ans_tmp)!=9:
                        return
                    text_numrow.append(text_numcur)
                    text_numcur.clear()
            for i in text_numrow: 
                for j in range(0,9):
                    self.ans.add(i[j])
                if len(self.ans)!=9:
                    self.ans.clear()
                    return
            cnt_cur = 0
            cnt_row = 0   
            self.ans.clear()
            set1 = set()
            set2 = set()
            set3 = set()
            for i in text_numrow:
                cnt_row += 1
                for j in i:
                    if cnt_cur %3 == 0:
                        set1.add(j)
                    elif cnt_cur %3 == 1:
                        set2.add(j)
                    elif cnt_cur %3 == 2:
                        set3.add(j)
                    cnt_cur+=1
            if cnt_row == 3:
                cnt_row = 0
                if len(set1)!=9 or len(set2)!=9  or len(set3)!=9:
                    return
                set1.clear()
                set2.clear()
                set3.clear()
            print('Sucess')
            if nlist == 90:
                server.Tcp_Send('close',self.toip)
                mysql = MySQL.mysql()
                sql = "update user set rankcnt = rankcnt+100 where uid = ' "+self.user+"'"
                mysql.newupdate(sql)
            dlg = wx.MessageDialog(self,"Sucess")
            dlg.ShowModal()
            dlg.Destroy()
    
    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "shiyuKirito","作者",wx.OK)    
        dlg.ShowModal()    
        dlg.Destroy()    

    def OnExit(self, e):
        self.Close(True)    
        peoFrame = peo.peoFrame(parent=None, title='个人信息', user=self.user)
        peoFrame.Show()
    def Num(self,n):
        sudunum = createsudu.main(n)
        return sudunum

if __name__ == '__main__':
    app = wx.App(False)
    s = input()
    frame = MainWindow(None, title = "hello", nlist=90,user=s)
    frame.Num(9)
    app.MainLoop()