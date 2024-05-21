import sqlite3
import re
import datetime
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

        self.removePunctuation = [".",",","(",")","\s"]
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
        for i in range(self.length):
            for j in range(len(self.texts[i])):
                w = self.texts[i][j]
                if w == word:
                    self.result.append([i,j])

    def Print_Level_1(self):
        c = 0
        for r in self.result:
            t = r[0]
            w = r[1]
            text = []
            dist = []

            print(c,"-",datetime.datetime.now(),"-",self.texts[t][0],"-",t)

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
                print(i, end=" ")
            print(dist)
            print("\n")        
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

    def compare(self,Qi,Ki):
        Q = self.texts[Qi]
        K = self.texts[Ki]

        Qf = self.frequency(Q)
        Kf = self.frequency(K)

        Qc,Qw = self.mergesort(Qf["count"],Qf["word"])
        Kc,Kw = self.mergesort(Kf["count"],Kf["word"])

        k = 0
        f1 = 0
        f2 = 0
        while True:
            print("\n","-"*30,"Text1","-"*30)
            for i in range(k,k+20):
                if i < len(Qc):
                    print(Qw[i],Qc[i],"|",end=" ")
                else:
                    f1 = 1
            print("\n","-"*30,"Text2","-"*30)
            for i in range(k,k+20):
                if i < len(Kc):
                    print(Kw[i],Kc[i],"|",end=" ")
                else:
                    f2 = 1
            if f1*f2 == 1: break
            
            inp = input("\ncontinue(yes or no): ")
            if inp == "no": break 
            k+=20

    def Similarity(self):
        wrr = {}
        texts = self.texts

        for text in texts:
            txt = self.frequency(text)["word"]

            for i in txt:#textごとに抽出
                if i in wrr:
                    wrr[i] += 1
                else:
                    wrr[i] = 1
        
        arr1 = list(wrr.keys())
        arr2 = list(wrr.values())

        arr2,arr1 = self.mergesort(arr2,arr1)

        return {"count":arr2,"word":arr1,"label":"simirality","element":["count","word"]}
    
    def DictPrint(self,dic):
        for element in dic["element"]:
            print("*"*30,dic["label"]+"["+element+"]","*"*30)
            print(dic[element])


    
#========Test=========#
db = DB()
db.InsertDB([
    ["aa","Once I arrived in Japan, I didn't have much of an opportunity to do much cooking due to living in an apartment with my wife's mother and sister. Once we finally moved out into a house of our own, I started to cook again, but had trouble sourcing ingredients for western style recipes (I'm not good at cooking Japanese food). Eventually, I ended up finding a few places that had the ingredients I needed, which was a relief as I was missing western food, but in Japan it is pretty expensive to purchase. It eing expensive didn't deter my want to start cooking again. After finally finding places to get ingredients, such as Seijo Ishii, Amica, Gyomu Super and the online store The Meat Guy, which supplies meat from Australia, New Zealand and other countries I started a cooking frenzy. I have cooked things like steak wrapped in bacon with garlic herb mashed potato, pasta bake, curry sausage pie, salmon steamed in lemon/lime juice with chilli, risotto and many others.  I have added some pictures of just some of things that I have cooked."],
    ["aa","After finally finding places to get ingredients, such as Seijo Ishii, Amica, Gyomu Super and the online store The Meat Guy, which supplies meat from Australia, New Zealand and other countries I started a cooking frenzy. I have cooked things like steak wrapped in bacon with garlic herb mashed potato, pasta bake, curry sausage pie, salmon steamed in lemon/lime juice with chilli, risotto and many others.  I have added some pictures of just some of things that I have cooked."],
    ["aa","One problem though is that I tend to be a bit overzealous with presentation, which was because of a chef friend of mine that wouldn't try my food unless it looked well presented. I was always perplexed by this because I wasn't working for a restaurant as a chef."]
             ]) 
#print(db.FetchDB())
anl = Analysis(db)
anl.split_space()
anl.search_word("mashed")
print("-"*10)
anl.Print_Level_1()
#anl.compare(0,1)
anl.DictPrint(anl.Similarity())

