import sqlite3
import re
import datetime
import tkinter as tk
import os
import traceback
class DB:
    def __init__(self):
        self.id = 0
        self.dbname = ("eldb.db")
        self.conn = sqlite3.connect(self.dbname, isolation_level=None)
        self.ResetDB()#test用
        self.cursor = self.conn.cursor()
        sql = """CREATE TABLE IF NOT EXISTS text(id, name, text)"""
        self.cursor.execute(sql)
        self.conn.commit()
    def Text2DB(self,dir):
        files = os.listdir(dir)
        for file in files:
            with open(os.path.join(dir,file),"rt",encoding="shift-jis") as f:
                texts = []
                count = 0
                text = ""
                #contents = []
                texts = []
                for t in f:
                    if t == "" or t=="\n":
                        if text != "":
                            text = text.replace("Title\n","") if count == 0 else text 
                            texts.append(text)
                            text = ""
                            count+=1
                    else:
                        text += t
                if text != "":
                            texts.append(text)
                            text = ""
                #contents.append(texts)

                #print("-"*10,[texts[0],texts[2]])
                inp = [texts[0],texts[2]]
                self.InsertDB([inp]) 
    
        """
        print(file)
        print(texts[0])
        print("-"*40,"*0")
        print(texts[1])
        print("-"*4,"*1")
        print(texts[2])
        print("-"*40)
        """
                    
        #print(file)
    def InsertDB(self,datas):#data:=[(),(),()]
        sql = """INSERT INTO text VALUES(?, ?, ?)"""
        for data in datas:
            data.insert(0,self.id)
            self.cursor.execute(sql, tuple(data))
            self.conn.commit()
            self.id += 1

    def FetchDB(self):
        sql = """SELECT * FROM text"""#条件を変える
        self.cursor.execute(sql)
        return self.cursor.fetchall()

            
    def DeleteDB(self):
        sql = """delete from test where id=?', ({},)""".format(id) #idと一致するものを消す。
        self.conn.execute(sql)
        self.conn.commit()
        self.id += 1
    
    def RenameDB(self,id,name):
        sql = """UPDATE text SET name = "{}" WHERE id = {};""".format(name,id)
        self.conn.execute(sql) 
        self.conn.commit()

    def ResetDB(self):
        sql = """DROP TABLE if exists text""" 
        self.conn.execute(sql)
        self.conn.commit()


    def CloseDB(self):
        self.conn.close()

class Analysis:
    def __init__(self, db):
        self.db = db
        self.contents = db.FetchDB()
        self.texts = []
        self.length = len(self.contents)
        self.result = []
        self.colors = []

        self.removePunctuation = [".",",","(",")","\s","\n"]
        self.remainPunctuation = []

    def split_space(self):
           for i in range(self.length):
            s = self.contents[i][2]

            #pは残す文字列のパターン
            for p in self.remainPunctuation:
                p_next = " " + p + " "
                s = s.replace(p,p_next)

            #pは削除する文字のパターン
            p = "["
            for i in self.removePunctuation:
                p += i
            p += "]+"

            self.texts.append([word for word in re.split(p, s) if word != ""])#self.contents[i][2]は文字列

    def search_word(self,word):#[index in contents, index in text]
        self.result=[]
        for i in range(self.length):
            for j in range(len(self.texts[i])):
                w = self.texts[i][j]
                if w == word:
                    self.result.append([i,j])
    def getColor(self):
        self.colors = []
        for i,j in self.result:
            now = j
            dis = 0
            color = []

            for k in range(5):
                now -=1
                if now >= 0:
                    dis += 1
                else:
                    break
            color.append(dis) 
            
            now = j
            dis = 0
            for k in range(5):
                now +=1
                if now < len(self.texts[i]):
                    dis += 1
                else: 
                    break
            color.append(dis)
            self.colors.append(color)





    def Print_Level_1(self):
        p = ""
        c = 0
        for r in self.result:
            t = r[0]
            w = r[1]
            text = []
            dist = []


            #print(c,"-",datetime.datetime.now(),"-",self.texts[t][0],"-",t)
            #p = str(c)+"-"+str(datetime.datetime.now())+"-"+self.texts[t][0]+"-"+str(t)

            i = 0
            while i <= 6 :
                if w - i >= 0:
                    text.insert(0,self.texts[t][w-i])
                    dist.insert(0,i)
                i += 1

            i = 1
            while i <= 5 :
                if w + i <= len(self.texts[t])-1:
                    text.append(self.texts[t][w+i])
                    dist.append(i)
                i += 1

            for i in text:
                pass
                #print(i, end=" ")
            #print(dist)
            #print("\n")        
            c+=1

    def frequency(self,text):
        wrr = {}
        for w in text:
            if w not in wrr:
                wrr[w] = 1
            else:
                wrr[w] += 1
        
        cnt = list(wrr.values())
        words = list(wrr.keys())
        
        f = {"count":cnt,"word":words,"label":"frequency","element":["count","word"]}
        return  f
    def max(self,array):
        max = 0
        for i in range(1,len(array)):
            if array[max] < array[i]:
                max = i
        
        return max

    def partition(self,array,array2):
        m = int( len(array) / 2 )
        arr1 = array[:m]
        arr2 = array[m:]
        arr21 = array2[:m]
        arr22 = array2[m:]

        return arr1,arr2,arr21,arr22

    def merge(self,left,right,left2,right2):
        array = []
        array2 = []
        i = 0
        j = 0
        while i < len(left) and j < len(right):
            if left[i] >= right[j]:
                array.append(left[i])
                array2.append(left2[i])
                i+=1
            else:
                array.append(right[j])
                array2.append(right2[j])
                j+=1

        if i == len(left):
            array += right[j:]
            array2 += right2[j:]
        else:
            array += left[i:]
            array2 += left2[i:]
        
        return array,array2
        

    def mergesort(self,array,array2):
        if len(array) == 1:
            return array,array2
        
        l,r,l2,r2 = self.partition(array,array2)

        l,l2 = self.mergesort(l,l2)
        r,r2 = self.mergesort(r,r2)

        m,m2 = self.merge(l,r,l2,r2)

        return m,m2

    def compare(self,Qi,Ki,k):
        Q = self.texts[Qi]
        K = self.texts[Ki]

        Qf = self.frequency(Q)
        Kf = self.frequency(K)

        Qc,Qw = self.mergesort(Qf["count"],Qf["word"])
        Kc,Kw = self.mergesort(Kf["count"],Kf["word"])

        f1 = 0
        f2 = 0

        dic = {"Qw":[],"Qc":[],"Kw":[],"Kc":[]}

        #print("\n","-"*30,"Text1","-"*30)
        for i in range(k,k+20):
            if i < len(Qc):
                dic["Qw"].append(Qw[i])
                dic["Qc"].append(Qc[i])
            else:
                f1 = 1
        #print("\n","-"*30,"Text2","-"*30)
        for i in range(k,k+20):
            if i < len(Kc):
                dic["Kw"].append(Kw[i])
                dic["Kc"].append(Kc[i])
            else:
                f2 = 1
        if f1*f2 == 1: return dic

        return dic
        

    def Similarity(self):
        wrr = {}
        texts = self.texts

        for text in texts:
            txt = self.frequency(text)["word"]

            for w in txt:#textごとに抽出
                if w in wrr:
                    wrr[w] += 1
                else:
                    wrr[w] = 1
        
        arr1 = list(wrr.keys())
        arr2 = list(wrr.values())

        arr2,arr1 = self.mergesort(arr2,arr1)

        return {"count":arr2,"word":arr1,"label":"simirality","element":["count","word"]}
    
    def DictPrint(self,dic):
        for element in dic["element"]:
            pass
            #print("*"*30,dic["label"]+"["+element+"]","*"*30)
            #print(dic[element])
    
class main:
    def __init__(self) -> None:
        self.STOP = False
        self.c = ["red","orange","yellow","lightblue","lightgreen","pink",None]
        self.db = DB()
    
        self.db.Text2DB("AA dataset")
      
        self.anl = Analysis(self.db)
        self.anl.split_space()
        
        self.root = tk.Tk()
        #root.minsize(640,480)
        self.root.geometry("800x480")  
        self.cv = tk.Canvas(self.root)
        self.frame = tk.Frame(self.cv)
        self.yscrollbar = tk.Scrollbar(
            self.cv, orient=tk.VERTICAL, command=self.cv.yview
        )
        self.xscrollbar = tk.Scrollbar(
            self.cv, orient=tk.HORIZONTAL, command=self.cv.xview
        )
        self.Wiget = {
            "Button":[],
            "Entry":[],
            "Label":[]
        }

# スクロールの設定
        self.cv.configure(scrollregion=(0, 0, 9000, 24000))
        self.cv.configure(yscrollcommand=self.yscrollbar.set)
        self.cv.configure(xscrollcommand=self.xscrollbar.set)

        # 諸々を配置
        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.cv.pack(expand=True, fill=tk.BOTH)
        # Canvas上の座標(0, 0)に対してFrameの左上（nw=north-west）をあてがうように、Frameを埋め込む
        self.cv.create_window((0, 0), window=self.frame, anchor="nw", width=9000, height=12000)
        self.cv.pack()

        self.StartPanel()


        self.root.mainloop()
    def test(self):
        print("This menu is developing!")

    def DestroyPartOfLabel(self,n):
        for l in self.Wiget["Label"][n:]:
            l.destroy()
        self.Wiget["Label"] = self.Wiget["Label"][:n]
        self.root.update()
    
    def DestroyLabel(self):
        for l in self.Wiget["Label"]:
            l.destroy()
        self.Wiget["Label"] = []
        self.root.update()
    
    def DestroyPanel(self):
        for b in self.Wiget["Button"]:
            b.destroy()
        for e in self.Wiget["Entry"]:
            e.destroy()
        for l in self.Wiget["Label"]:
            l.destroy()
        
        self.Wiget["Button"] = []
        self.Wiget["Label"] = []
        self.Wiget["Entry"] = []
    
    def StartPanel(self):
        self.DestroyPanel()
        self.STOP = True
        self.STOP = False
        
        self.Wiget["Button"]=[
            tk.Button(text="Search Word",command=self.SearchPanel,width=10,height=3),
            tk.Button(text="Rename",command=self.RenamePanel,width=10,height=3),
            tk.Button(text="Fetch",command=self.FetchPanel,width=10,height=3),
            tk.Button(text="Similaryty",command=self.SimilarytyPanel,width=10,height=3),
            tk.Button(text="Compare",command=self.ComparePanel,width=10,height=3),
            tk.Button(text="Developing",command=self.test,width=10,height=3),
            tk.Button(text="Developing",command=self.test,width=10,height=3),
            tk.Button(text="Developing",command=self.test,width=10,height=3),
            tk.Button(text="Developing",command=self.test,width=10,height=3),
            tk.Button(text="Developing",command=self.test,width=10,height=3),
            tk.Button(text="Developing",command=self.test,width=10,height=3),
            tk.Button(text="Developing",command=self.test,width=10,height=3),
            tk.Button(text="Developing",command=self.test,width=10,height=3),
            tk.Button(text="Developing",command=self.test,width=10,height=3),
            tk.Button(text="Developing",command=self.test,width=10,height=3)
        ]
        [self.Wiget["Button"][x].place(x=70+100*(x%5),y=100+int(x/5)*60) for x in range(len(self.Wiget["Button"]))]

    def putLabels(self,text,x,y,n,font_size):
        #i y-line x x-line n color font_size font_size
        label = tk.Label(self.frame,text=text,bg=self.c[n],font=("MSゴシック", font_size, "bold"))

        if x + label.winfo_reqwidth() > 780:
            x = 0
            y += label.winfo_reqheight()
    
        label.place(x=x,y=y)

        x += label.winfo_reqwidth()

        self.Wiget["Label"].append(label) 

        return x,y

    def putLabel(self,text,x,y,n,font_size,xflag,yflag):
        #i y-line x x-line n color font_size font_size
        
        label = tk.Label(self.frame,text=text,bg=self.c[n],font=("MSゴシック", font_size, "bold"))
        label.place(x=x,y=y) 
        self.root.update()

        x += label.winfo_reqwidth() if xflag else -x
        y += label.winfo_reqheight() if yflag else 0
        self.Wiget["Label"].append(label) 

        return x,y
    
    def getEntry(self,i):
        self.DestroyPartOfLabel(4)

        w = self.Wiget["Entry"][i].get()
        self.anl.search_word(w)
        self.anl.getColor()

        texts = self.anl.texts
        sum = 0
        font_size = 10
        y = 70

        
        if self.anl.result == []:
            self.putLabel("Nothing!",200,y,6,30,False,False)

        self.putLabel(":::Hit["+str(len(self.anl.result))+"]:::",450,20,1,15,True,False)
        self.root.update()

        for i in range(len(self.anl.result)):
            if self.STOP: break

            text = ""
            j,k = self.anl.result[i]
            x = 0

            p = str(i)+"-"+str(datetime.datetime.now())+"-"+texts[j][0]+"-"+str(j)
            x,y = self.putLabel(p,x,y,6,font_size,False,True)
            sum += 1

            col = self.anl.colors[i][0]
            for n in range(1,col+1):
                if self.STOP: break
                text = texts[j][k-(6-n)]+" "
                x,y = self.putLabel(text,x,y,6-n,font_size,True,False)

            text = texts[j][k]+" "
            x,y = self.putLabel(text,x,y,0,font_size,True,False)


            col = self.anl.colors[i][1]
            for n in range(1,col+1):
                if self.STOP: break
                text = texts[j][k+n]+" "
                x,y = self.putLabel(text,x,y,n,font_size,True, True if n == col else False)

            #print(j,"<-J",k,"<-K",i,"<-i",p,text)

            self.root.update()

        #print(len(self.Wiget["Label"]),sum)

    
    def SearchPanel(self):
        self.DestroyPanel()
        x0,y=(30,0)
        x,y=self.putLabel("-"*30,x0,y,6,10,False,True)
        x,y=self.putLabel("|     Search     |",x0,y,6,13,False,True)
        x,y=self.putLabel("-"*30,x0,y,6,10,False,True)
        
        x,y = (200,30)
        self.Wiget["Entry"].append(tk.Entry(self.frame, width=20))
        self.Wiget["Entry"][0].place(x=x,y=y)
        self.Wiget["Button"].append(
            tk.Button(self.frame,text="検索", command=lambda:self.getEntry(0))
        )
        self.Wiget["Button"].append(
           tk.Button(self.frame,text="戻る",command=self.StartPanel)
        )
        self.Wiget["Button"][0].place(x=x+150,y=y)
        self.Wiget["Button"][1].place(x=x+200,y=y)
    def rename(self):
        self.DestroyPartOfLabel(2)

        self.Wiget["Button"][1]["state"] = tk.DISABLED
        
        font_size = 13

        try:
            id = self.Wiget["Entry"][0].get()
            name = self.Wiget["Entry"][1].get()

            name0 = self.anl.contents[int(id)][1]

            self.db.RenameDB(id,name)
            self.anl.contents = self.db.FetchDB()
            self.anl.split_space()
        except:
            x,y=self.putLabel("---->{}".format("Error"),0,100,6,15,False,False)

        self.Wiget["Button"][1]["state"] = tk.NORMAL

        x,y=self.putLabel(" -"*60,0,100,6,5,False,True)
        x,y=self.putLabel(name0.replace("\n",""),0,y,6,font_size,True,False)
        x,y=self.putLabel(" ---> "+name,x,y,6,font_size,False,True)
        x,y=self.putLabel(" -"*60,0,y,6,5,False,False)
        
        


    
    def RenamePanel(self):
        self.DestroyPanel()
        x0,y=(30,0)
        x,y=self.putLabel("-"*30,x0,y,6,10,False,True)
        x,y=self.putLabel("|     Rename     |",x0,y,6,13,False,True)
        x,y=self.putLabel("-"*30,x0,y,6,10,False,True)
        x,y = (150,0)
        self.putLabel("id: ",x+30,y,6,10,False,False)
        self.putLabel("name: ",x+30,y+50,6,10,False,False)

        self.Wiget["Entry"].append(tk.Entry(self.frame, width=20))
        self.Wiget["Entry"][0].place(x=x+100,y=0)

        self.Wiget["Entry"].append(tk.Entry(self.frame,width=20))
        self.Wiget["Entry"][1].place(x=x+100,y=50)

        self.Wiget["Button"].append(
           tk.Button(self.frame,text="戻る",command=self.StartPanel)
        )
        self.Wiget["Button"][0].place(x=x+250,y=0)
        self.Wiget["Button"].append(
           tk.Button(self.frame,text="変更",command=self.rename)
        )
        self.Wiget["Button"][1].place(x=x+250,y=50)

    def fetch(self):
        self.DestroyPartOfLabel(7)

        try:
            contents = self.anl.contents

            id   = self.Wiget["Entry"][0].get()
            name = self.Wiget["Entry"][1].get()

            if id != "":
                id = int(id)

            name = contents[id][1] if id != "" else name
            text = contents[id][2] if id != "" else ""


            for i in range(len(contents)):
                if contents[i][1].replace("\n","") == name: 
                    id = contents[i][0]
                    text = contents[i][2]
                    break
            
            if name == ""  or id == "":
                self.DestroyLabel()
                self.FetchPanel()

            else:
                x,y = (0,100)
                x,y=self.putLabel("id -> {}".format(id),x,y,6,10,False,True)
                x,y=self.putLabel("name -> ",x,y,6,10,True,False)
                x,y=self.putLabel("{}".format(name),x,y,6,10,False,True)
                x,y=self.putLabel("text -> ",x,y,6,10,True,False)
                x,y=self.putLabel("{}".format(text),x,y,6,10,False,True)

        except:
            traceback.print_exc()
            self.DestroyLabel()
            self.FetchPanel()
            x,y=self.putLabel("---->{}".format("Error"),0,200,6,15,False,False)
    
    def FetchPanel(self):
        self.DestroyPanel()
        x0,y=(30,0)
        x,y=self.putLabel("-"*30,x0,y,6,10,False,True)
        x,y=self.putLabel("|       Fetch       |",x0,y,6,13,False,True)
        x,y=self.putLabel("-"*30,x0,y,6,10,False,True)

        x,y = (200,0)

        self.putLabel("idまたはnameで検索: ",x,y,6,10,False,False)

        self.putLabel("id: ",x,y+30,6,10,False,False)
        self.putLabel("name: ",x,y+60,6,10,False,False)

        self.Wiget["Entry"].append(tk.Entry(self.frame, width=20))
        self.Wiget["Entry"][0].place(x=x+100,y=y+30)

        self.Wiget["Entry"].append(tk.Entry(self.frame,width=20))
        self.Wiget["Entry"][1].place(x=x+100,y=y+60)

        self.Wiget["Button"].append(
           tk.Button(self.frame,text="実行",command=self.fetch)
        )
        self.Wiget["Button"][0].place(x=x+240,y=y+60)

        self.Wiget["Button"].append(
           tk.Button(self.frame,text="戻る",command=self.StartPanel)
        )
        self.Wiget["Button"][1].place(x=x+240,y=y+30)
        
    def SimilarytyPanel(self):
        self.DestroyPanel()
        
        x,y = (0,0)
        font_size = 12
        dic = self.anl.Similarity()

        x,y = self.putLabel("-"*30,0,y,6,10,False,True)
        x,y = self.putLabel("| Similaryty  |",x,y,6,15,False,True)
        x,y = self.putLabel("-"*30,x,y,6,10,True,True)

        self.Wiget["Button"].append(
           tk.Button(self.frame,text="戻る",command=self.StartPanel)
        )
        self.Wiget["Button"][0].place(x=450,y=0)

        self.Wiget["Entry"].append(tk.Entry(self.frame, width=30))
        self.Wiget["Entry"][0].place(x=200,y=0)
        self.Wiget["Button"].append(
            tk.Button(self.frame,text="実行", command=self.Similarity)
        )
        self.Wiget["Button"][1].place(x=400,y=0)

    def Similarity(self):
        font_size = 12
        dic = self.anl.Similarity()
        x,y = (0,70)
        w = self.Wiget["Entry"][0].get()
        for i in range(len(dic["word"])):
            if (dic["word"][i] == w): color = 0
            else: color = 6
            x,y = self.putLabels(""+dic["word"][i] + "[" + str(dic["count"][i])+"] :::",x,y,color,font_size)
            self.root.update()
    
    def ComparePanel(self):
        self.DestroyPanel()

        self.compare_k = 0
        self.compare_y = 200
        self.compare_id0 = None
        self.compare_id1 = None
        
        x,y = (0,0)
        font_size = 12

        x,y = self.putLabel("-"*30,0,y,6,10,False,True)
        x,y = self.putLabel("| Compare  |",x,y,6,15,False,True)
        x,y = self.putLabel("-"*30,x,y,6,10,True,True)

        x,y = self.putLabel("      id                      name  ",0,y,6,15,False,True)

        T1 = tk.Entry(self.frame,width = 20)
        T1.place(x=0,y=y)

        self.putLabel("or",130,y,6,15,False,True)

        T2 = tk.Entry(self.frame,width = 20)
        T2.place(x=165,y=y)

        T3 = tk.Entry(self.frame,width = 20)
        T3.place(x=0,y=y+40)

        self.putLabel("or",130,y+40,6,15,False,True)

        T4 = tk.Entry(self.frame,width = 20)
        T4.place(x=165,y=y+40)

        x,y = (0,y+40+30)

        self.Wiget["Button"].append(
           tk.Button(self.frame,text="実行",command=lambda:self.compare(),width=20)
        )
        self.Wiget["Button"][0].place(x=x,y=y)

        self.Wiget["Button"].append(
           tk.Button(self.frame,text="戻る",command=self.StartPanel,width=20)
        )
        self.Wiget["Button"][1].place(x=x+160,y=y)

        self.Wiget["Entry"].append(T1)
        self.Wiget["Entry"].append(T2)
        self.Wiget["Entry"].append(T3)
        self.Wiget["Entry"].append(T4)
    
    def compare(self):
        x,y = (0,self.compare_y)
        font_size = 13

        id0   = self.Wiget["Entry"][0].get()
        name0 = self.Wiget["Entry"][1].get()
        id1   = self.Wiget["Entry"][2].get()
        name1 = self.Wiget["Entry"][3].get()

        if id0 == "" or id1 == "":
            for text in self.anl.texts:
                if text[1].replace("\n","") == name0:
                    id0 = text[0]

                    if id1 != "":
                        break
                if text[1].replace("\n","") == name1:
                    id1 = text[0]

                    if id1 != "":
                        break
        if id0 == "":
            self.compare_y = 200            
            self.compare_k = 0
            return
        elif id1 == "":
            self.compare_y = 200
            self.compare_k = 0
            return

        id0 = int(id0)
        id1 = int(id1)

        if id0 != self.compare_id0:
            self.compare_y = 200
            self.compare_k = 0

            self.compare_id0 = id0
            self.compare_id1 = id1

            x,y = (0,self.compare_y)

            self.DestroyPartOfLabel(4)
        if id1 != self.compare_id1:
            self.compare_y = 200
            self.compare_k = 0

            self.compare_id0 = id0
            self.compare_id1 = id1

            x,y = (0,self.compare_y)

            self.DestroyPartOfLabel(4)
        
        dic = self.anl.compare(id0,id1,self.compare_k)

        if self.compare_k == 0:
            x,y = self.putLabel("*"*130,x,y,6,10,False,True)
            self.root.update()

        for i in range(len(dic["Qw"])):
            x,y = self.putLabels(dic["Qw"][i]+"["+str(dic["Qc"][i])+"] :::",x,y,6,font_size)

        x,y = self.putLabel("[end]",x,y,6,font_size,False,True) #改行

        x,y = self.putLabel("-"*200,x,y,6,10,False,True)
        self.root.update()

        for i in range(len(dic["Kw"])):
            x,y = self.putLabels(dic["Kw"][i]+"["+str(dic["Kc"][i])+"] :::",x,y,6,font_size)

        x,y = self.putLabel("[end]",x,y,6,font_size,False,True) #改行
        
        x,y = self.putLabel("*"*130,0,y,6,10,False,True)
        self.root.update()

        self.compare_y = y
        self.compare_k += 20
        

        
        
        
    



main()

a = list(range(0,10))
print(a)
print(a[:3])
print(a[3:])