# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 02:53:51 2023
Tamamen kendim yaptıgım bellman-fast algoritmasının kod implemantasyonu
@author: Asus
"""
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
print("en kısa yol : ",yol)






