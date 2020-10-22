
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np
import pickle
from tensorflow.python.keras.models import load_model,Model
base_model = load_model('/home/ayush/Desktop/addverb/django_project/covid/weights_v5_final_2cls.13.hdf5')
embedding_predictor = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)
sc = pickle.load(open('/home/ayush/Desktop/addverb/django_project/covid/svm_classifier.sav', 'rb'))
def predict(img):

    base_pred = base_model.predict(img)[0][0]

    if base_pred < 0.5:
        return "Normal"
    else:

        emb = embedding_predictor.predict(img)
        final_pred = sc.predict(emb)[0]
        if(final_pred == 0):
            return 'Normal'
        if(final_pred == 1):
            return 'Bacterial Pneumonia'
        if(final_pred == 2):
            return 'Viral Pneumonia'
        if(final_pred == 3):
            return 'Covid-19'

def index(request):
    return render(request,'index.html')

def result(request):
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)
    testimage = '.' + filePathName
    img = cv2.imread(testimage)
    img = cv2.resize(img, (224,224))
    img = np.array(img).astype('float32') / 255.
    img = np.expand_dims(img, axis = 0)
    pred = predict(img)
    return render(request,'result.html',{'pred':pred})

