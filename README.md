# bellman-ford-gorselli
### Bellman-Ford algoritmasının implemantasoynu ve görselleştirilmesi
### Dosya İçeriği
#### bellman-ford-gorselli.py --> görselleştirilmiş versiyon
#### bellman-ford-sade.py --> bellman-ford algoritmasının normal implemantasyonu
#### gif_olusturucu.py --> gif oluşturmak için kod
#### harita.jpg ve güncel_harita.jpg --> görselleştirirken kullanılan resimler
### Nasıl Çalışır?
Bellman-ford algoritmasıni vermek için A nın komşularından başlayarak , her düğümde ve komşu düğüm arasındaki kenarları bir python sözlüğünün içine atıyoruz.Algoritma bu sözlüğü sıradan tarayarak ilerliyor ve uzakliklar adlı python sözlüğünü sürekli güncelleştiriyor.Tüm kenarlar dolaşıldığında mantıken A'da tüm düğümlere gidilebilecek en kısa yollar uzakliklar sözlüğünde tanımlanmış olacak.
### Örnek
<img src="https://github.com/rag0nn/bellman-ford-gorselli/blob/main/gifs_and_images/ornekler.gif?raw=true">
