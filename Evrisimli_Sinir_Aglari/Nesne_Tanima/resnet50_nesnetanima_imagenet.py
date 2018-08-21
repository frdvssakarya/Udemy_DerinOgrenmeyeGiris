# -*- coding: utf-8 -*-
"""ResNet50_NesneTanima_ImageNet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i2zBJLv9wQtzKirSu2JUgQ6AkrHMsV_5

# **IMAGENET - ResNet50  - NESNE TANIMA**


---
[<img align="left" width="100" height="100" src="http://www.i2symbol.com/images/symbols/style-letters/circled_latin_capital_letter_a_u24B6_icon_128x128.png">](https://www.ayyucekizrak.com/)
[<img align="right" width="200" height="50"  src="https://raw.githubusercontent.com/deeplearningturkiye/pratik-derin-ogrenme-uygulamalari/944a247d404741ba37b9ef74de0716acff6fd4f9/images/dltr_logo.png">](https://deeplearningturkiye.com/)

**Gerekli paketler yükleniyor...**
"""

from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
from io import BytesIO
import os
import requests

"""**ImageNet veriseti ile eğitilmiş model ve ağırlıkları yükleniyor...**"""

model = ResNet50(weights="imagenet")

"""**Resmi girişe uygun formata getirmek için yeniden boyutlandırma fonksiyonu tanımlanıyor**"""

def prepare_image(image, target):
	# giriş görüntüsünü yeniden boyutlandırma ve ön işlemerin yapılması
	image = image.resize(target)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image = imagenet_utils.preprocess_input(image)

	# işlenmiş görüntüyü alma
	return image

"""## **Sınıflandırma istediğiniz resmin web adresini aşağıdaki giirş alanına giriniz**"""

#@title Default title text { vertical-output: true }
ImageURL = "https://i.cnnturk.com/ps/cnnturk/75/650x0/57ad7dd9a781b6264026292d.jpg" #@param {type:"string"}

"""**Girilen web adresinden resim indiriliyor**"""

#ImageURL = "https://i.cnnturk.com/ps/cnnturk/75/650x0/57ad7dd9a781b6264026292d.jpg"
response = requests.get(ImageURL)
image = Image.open(BytesIO(response.content))
image

"""**Eğitilmiş model ile sınıflandırma yapılıyor.**"""

data = {"success": False}

pre_image = prepare_image(image, target=(224, 224)) # 224 x 224 boyutlu hale getir

preds = model.predict(pre_image) # Kesirim modeline ön işlemden geçmiş görüntüyü uygula

results = imagenet_utils.decode_predictions(preds) #kestirim
data["predictions"] = []


for (imagenetID, label, prob) in results[0]: # ImageNet veri kümseinden etiket, olasılık ve kestrim sonucunu al
  r = {"label": label, "probability": float(prob)}
  data["predictions"].append(r)
  
data["success"] = True

print(data)



print("Sınıflandırma tahmini en yüksek olan {0} oranıyla {1}'dır.".format(data["predictions"][0]["probability"],data["predictions"][0]["label"])) 
# En yüksek olasılıklı sonucu ekrana yazdır

