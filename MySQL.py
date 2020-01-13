import pymysql
class mysql:
    def __init__(self):
        self.hhost = '192.168.43.213'
        try:
            self.conn = pymysql.connect(host = self.hhost, user = 'root', password = 'root', database = 's1', port = 3306, charset='utf8')
            self.conn = pymysql.connect(host = self.hhost, user = 'root', password = 'root', database = 's1', port = 3306, charset='utf8')
            self.cur = self.conn.cursor()
            print(self.conn)
        except Exception as e:
            pass
            # print(e)
        finally:
            self.conn.close()
    def newselect(self, sql):
        try:
            self.conn = pymysql.connect(host = self.hhost, user = 'root', password = 'root', database = 's1', port = 3306, charset='utf8')
            self.cur = self.conn.cursor()
            self.cur.execute(sql)
            return  self.cur.fetchall()
        except Exception as e:
            pass
            # print(e)
        finally:
            self.conn.close()

    def newupdate(self, sql):
        try:
            self.conn = pymysql.connect(host = self.hhost, user = 'root', password = 'root', database = 's1', port = 3306, charset='utf8')
            self.cur = self.conn.cursor()        
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            pass
            # print(e)
        finally:
            self.conn.close()
# if __name__ == "__main__":
#     # s = mysql()
#     # print(s.newselect("select uname from user where uid = 'text'"))
    

