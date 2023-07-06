# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 23:03:43 2023
Bellman-fest algoritması 
"""

###TÜMÜ GÖRSELLİK İÇİN KULLANILAN KÜTÜPHANELER
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import QPixmap
from threading import Thread

import cv2
import time

#GÖRSELLEŞTİRME İÇİN KULLANILCAK CLASSLAR(GÖRSELLİK)
class node():
    def __init__(self,isim,x,y,renk,uzaklik=0):
        self.isim = isim
        self.konum = (x,y)
        self.renk = renk
        self.uzaklik = uzaklik

class kenar():
    def __init__(self,isim,x1,y1,x2,y2,renk,agirlik,agirlik_renk):
        self.isim = isim
        self.baslangic = (x1,y1)
        self.bitis = (x2,y2)
        self.renk = renk
        self.agirlik = agirlik
        agirlik_x = int((x2-x1)/2 + x1) 
        agirlik_y = int((y2-y1)/2 + y1) 
        self.agirlik_konum = (agirlik_x,agirlik_y)
        self.agirlik_renk = agirlik_renk
        

class BellmanFest_gui(QWidget):
    
    def __init__(self,edges,nodes,kenarlar,renk_kirmizi,renk_siyah,renk_yesil,renk_gri,renk_mavi):
        QWidget.__init__(self)
        
        self.renk_kirmizi = renk_kirmizi
        self.renk_yesil = renk_yesil
        self.renk_siyah = renk_siyah
        self.renk_gri = renk_gri
        self.renk_mavi = renk_mavi
        self.nodes = nodes
        self.kenarlar = kenarlar
        self.edges = edges
        
        self.olustur_ekran()
        self.ciz_baglantilar()
        
        self.arama_thread()
        
    ##pyqt5 EKRANI OLUŞTUR
    def olustur_ekran(self):
        pixmap = QPixmap("harita.jpg")
        self.ekran = QLabel()
        self.ekran.setPixmap(pixmap)
        
        layout = QGridLayout()
        layout.addWidget(self.ekran)
        self.setLayout(layout)
        self.setWindowTitle("Harita")
        self.resize(1200,700)
        
    ##KENAR VE DÜĞÜMLERİ ÇİZ
    def ciz_baglantilar(self):
        time.sleep(0.4)
        image = cv2.imread("harita.jpg") 
        image = self.ciz_dugumler(image) 
        image = self.ciz_kenarlar(image)
        
        cv2.imwrite("guncel_harita.jpg",image)
        image = QPixmap("guncel_harita.jpg")
        self.ekran.setPixmap(image)
        
    def ciz_kenarlar(self,image):
        
        for item in self.kenarlar.items():
            kenar = item[1]
            cv2.arrowedLine(image, kenar.baslangic, kenar.bitis , kenar.renk , 3) 
            cv2.putText(image,str(kenar.agirlik),kenar.agirlik_konum,cv2.FONT_HERSHEY_SIMPLEX,0.8,kenar.agirlik_renk,1,cv2.LINE_AA) 
            
        return image
    
    def ciz_dugumler(self,image):

        yaricap_1 = 40
        yaricap_2 = 25
        for item in self.nodes.items():
            dugum = item[1]
            #cv2.circle(image, dugum.konum, yaricap_1, self.renk_mavi,-1)
            cv2.circle(image, dugum.konum, yaricap_2, dugum.renk,-1)
            cv2.putText(image,f"{dugum.isim}:{dugum.uzaklik}",(dugum.konum[0]-20,dugum.konum[1]-40),cv2.FONT_HERSHEY_SIMPLEX,1,dugum.renk,2,cv2.LINE_AA) 
            
        return image

    def arama_thread(self):
        t1 = Thread(target=self.arama)
        t1.start()

    def arama(self):
        
        ##DÜĞÜMLERİN UZAKLIKLARINI TUTACAK OLAN SÖZLÜK (ARAMA)
        uzakliklar = {}
        uzakliklar["A"] = (0,None) #uzaklık , onceki_node
        
        
        
        ##UZAKLIKLARI BUL
        for edge in self.edges.items():
            rotation= edge[0]
            pre_node = rotation.split("-")[0]
            post_node = rotation.split("-")[1]
            
            weight = edge[1]
            
            ##print(pre_node," ",post_node," ",weight) 
            
            distance = int(uzakliklar[pre_node][0]) + weight
            
            if post_node in uzakliklar.keys() and uzakliklar[post_node][0] <= distance:     
                pass
            else:
                self.nodes[post_node].uzaklik = distance                
                uzakliklar[post_node] = (distance,pre_node)
                
                
            self.kenarlar[rotation].renk = self.renk_yesil

            self.ciz_baglantilar()
                
            print(uzakliklar)
            
        #HEDEF DÜĞÜMÜ EN KISA YOLU GÖSTER
        baslangic_node = "A"
        hedef_node = "N"
        yol = []  ##geriye doğru en kısa yolu sırasıyla nodelar olarak tutan dizi
        
        
        ##yolu bulan rekürsif fonksiyon
        def rotasyon(son_node):
            onceki_node = uzakliklar[son_node][1]
            yol.append(son_node)    
            
            if onceki_node == None: #geriye doğru ilerlerken son düğümün önceki dğüümü None oldugunda dur
                pass
            else:
                return rotasyon(onceki_node)
        
        rotasyon(hedef_node)
        
        print(yol)
        for i in range(len(yol)-1):
            kenar = f"{yol[i+1]}-{yol[i]}"
            self.kenarlar[kenar].renk = self.renk_kirmizi
            self.ciz_baglantilar()



#RENKLER (GÖRSELLİK)
renk_siyah = (0,0,0)
renk_yesil = (80,255,50)
renk_kirmizi = (49,49,255)
renk_gri = (130,130,130)
renk_mavi = (255,255,40)
"""GRAF1
#KENARLAR = {} -> GÖRSEL OLARAK TUTMAK , EDGES = {} ARAMA YAPARKEN KULLANILMAK İÇİN TUTULUYOR
##KENARLARI VE AĞRILIKLARI TUTAN SÖZLÜK (ARAMA VE GÖRSELLİK)
edges = {}
edges["A-B"] = 2
edges["A-C"] = 3
edges["B-E"] = 4
edges["C-D"] = 5
edges["C-F"] = 4
edges["E-G"] = 1
edges["F-G"] = 3
edges["F-D"] = 1
edges["D-G"] = 4


##DÜĞÜMLERİ OLUŞTURUYORUZ(GÖRSEL)
nodes = {}
nodes["A"] = node("A",300,300,renk_siyah,0)    
nodes["B"] = node("B",400,250,renk_siyah,0)    
nodes["C"] = node("C",350,400,renk_siyah,0)    
nodes["D"] = node("D",450,275,renk_siyah,0)    
nodes["E"] = node("E",600,200,renk_siyah,0)    
nodes["F"] = node("F",500,450,renk_siyah,0)    
nodes["G"] = node("G",650,275,renk_siyah,0)        
"""
###GRAF2
#KENARLAR = {} -> GÖRSEL OLARAK TUTMAK , EDGES = {} ARAMA YAPARKEN KULLANILMAK İÇİN TUTULUYOR
##KENARLARI VE AĞRILIKLARI TUTAN SÖZLÜK (ARAMA VE GÖRSELLİK)
edges = {}#22
edges["A-B"] = 1 
edges["A-E"] = 3
edges["A-F"] = 2
edges["A-G"] = 2
edges["B-D"] = 2 
edges["E-D"] = 3
edges["D-E"] = 4
edges["D-C"] = 1
edges["B-G"] = 4 
edges["E-F"] = 3
edges["F-L"] = 2
edges["L-M"] = 3 
edges["L-N"] = 4
edges["M-O"] = 1
edges["O-M"] = 2
edges["N-O"] = 2
edges["G-H"] = 5
edges["H-I"] = 1
edges["I-J"] = 1
edges["J-N"] = 3
edges["I-K"] = 2
edges["J-K"] = 1
edges["M-L"] = 3 



##DÜĞÜMLERİ OLUŞTURUYORUZ(GÖRSEL)
nodes = {}
nodes["A"] = node("A",600,350,renk_siyah,0) 
nodes["B"] = node("B",525,300,renk_siyah,0) 
nodes["C"] = node("C",475,200,renk_siyah,0) 
nodes["D"] = node("D",425,325,renk_siyah,0) 
nodes["E"] = node("E",475,425,renk_siyah,0) 
nodes["F"] = node("F",625,425,renk_siyah,0) 
nodes["G"] = node("G",625,275,renk_siyah,0)
nodes["H"] = node("H",650,175,renk_siyah,0) 
nodes["I"] = node("I",750,225,renk_siyah,0) 
nodes["J"] = node("J",750,300,renk_siyah,0) 
nodes["K"] = node("K",1000,250,renk_siyah,0) 
nodes["L"] = node("L",700,350,renk_siyah,0) 
nodes["M"] = node("M",750,400,renk_siyah,0) 
nodes["N"] = node("N",1025,325,renk_siyah,0) 
nodes["O"] = node("O",825,375,renk_siyah,0) 







##KENARLARI OLUŞTURUYORUZ ,  düğümleri kullanarak otomatik olarak oluşturuyoruz (GÖRSEL)   
kenarlar = {}

for edge in edges.items():
    rotasyon = edge[0]
    baslangic_node = rotasyon.split("-")[0]
    bitis_node = rotasyon.split("-")[1]
    
    weight = edge[1]
    
    kenarlar[rotasyon] = kenar(rotasyon , nodes[baslangic_node].konum[0],nodes[baslangic_node].konum[1] , nodes[bitis_node].konum[0],nodes[bitis_node].konum[1] , renk_gri , weight,renk_gri)

#print(kenarlar,"\n \n",nodes)


app = QApplication([])
widget = BellmanFest_gui(edges,nodes,kenarlar,renk_kirmizi,renk_siyah,renk_yesil,renk_gri,renk_mavi)
widget.show()
app.exec_()



























"""ARAMA ALGORİTMALARININ SADE HALİ 


##DÜĞÜMLERİN UZAKLIKLARINI TUTACAK OLAN SÖZLÜK (ARAMA)
uzakliklar = {}
uzakliklar["A"] = (0,None) #uzaklık , onceki_node



##UZAKLIKLARI BUL
for edge in edges.items():
    
    rotation= edge[0]
    pre_node = rotation.split("-")[0]
    post_node = rotation.split("-")[1]
    
    weight = edge[1]
    
    ##print(pre_node," ",post_node," ",weight) 
    
    distance = int(uzakliklar[pre_node][0]) + weight
    
    if post_node in uzakliklar.keys() and uzakliklar[post_node][0] <= distance:
        pass
    else:
        uzakliklar[post_node] = (distance,pre_node)
        
    print(uzakliklar)
    
#HEDEF DÜĞÜMÜ EN KISA YOLU GÖSTER
baslangic_node = "A"
hedef_node = "D"
yol = []  ##geriye doğru en kısa yolu sırasıyla nodelar olarak tutan dizi

##yolu bulan rekürsif fonksiyon
def rotasyon(son_node):
    onceki_node = uzakliklar[son_node][1]
    yol.append(son_node)    
    
    if onceki_node == None: #geriye doğru ilerlerken son düğümün önceki dğüümü None oldugunda dur
        pass
    else:
        return rotasyon(onceki_node)

rotasyon(hedef_node)
print(yol)



"""


    