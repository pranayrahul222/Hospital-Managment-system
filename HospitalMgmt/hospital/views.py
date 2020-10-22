from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from .models import *
# Create your views here.


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


def About(request):
	return render(request,'about.html')

def Contact(request):
	return render(request,'contact.html')


def Index(request):
    return render(request,'index.html')

# def Index(request):
# 	if not request.user.is_staff:
# 		return redirect('login')
#
# 	doctors=Doctor.objects.all()
# 	patients=Patient.objects.all()
# 	appointments=Appointment.objects.all()
#
# 	d=0
# 	p=0
# 	a=0
# 	for i in doctors:
# 		d+=1
# 	for i in patients:
# 		p+=1
# 	for i in appointments:
# 		a+=1
# 	d1={'d':d,'p':p,'a':a}
# 	return render(request,'index.html',d1)

def Login(request):
	error=""
	if request.method=='POST':
		u=request.POST['uname']
		p=request.POST['pwd']
		user=authenticate(username=u,password=p)
		try:
			if user.is_staff:
				login(request,user)
				error="no"
			else:
				error="yes"
		except:
			error="yes"
	d={'error':error}
	return render(request,'login.html',d)

def Logout_admin(request):
	if not request.user.is_staff:
		return redirect('login')
	logout(request)
	return redirect('login')

def View_Doctor(request):
	if not request.user.is_staff:
		return redirect('login')
	doc = Doctor.objects.all()
	d={'doc':doc}
	return render(request,'view_doctor.html',d)


def Add_Doctor(request):
	error=""
	if not request.user.is_staff:
		return redirect('login')
	if request.method=='POST':
		n=request.POST['name']
		c=request.POST['contact']
		sp=request.POST['special']
		try:
			Doctor.objects.create(name=n,mobile=c,special=sp)
			error="no"
		except:
			error="yes"
	d={'error':error}
	return render(request,'add_doctor.html',d)


def Delete_Doctor(request,pid):
	if not request.user.is_staff:
		return redirect('login')
	doctor=Doctor.objects.get(id=pid)
	doctor.delete()
	return redirect('view_doctor')

def View_Patient(request):
	if not request.user.is_staff:
		return redirect('login')
	pat = Patient.objects.all()
	d={'pat':pat}
	return render(request,'view_patient.html',d)


def Add_Patient(request):
	error=""
	if not request.user.is_staff:
		return redirect('login')
	if request.method=='POST':
		n=request.POST['name']
		g=request.POST['gender']
		m=request.POST['mobile']
		a=request.POST['address']
		try:
			Patient.objects.create(name=n,gender=g,mobile=m,address=a)
			error="no"
		except:
			error="yes"
	d={'error':error}
	return render(request,'add_patient.html',d)


def Delete_Patient(request,pid):
	if not request.user.is_staff:
		return redirect('login')
	patient=Patient.objects.get(id=pid)
	patient.delete()
	return redirect('view_patient')

def View_Appointment(request):
	if not request.user.is_staff:
		return redirect('login')
	appoint = Appointment.objects.all()
	d={'appoint':appoint}
	return render(request,'view_appointment.html',d)


def Add_Appointment(request):
	error=""
	if not request.user.is_staff:
		return redirect('login')
	doctor1=Doctor.objects.all()
	patient1=Patient.objects.all()
	if request.method=='POST':
		d=request.POST['doctor']
		p=request.POST['patient']
		d1=request.POST['date']
		t=request.POST['time']
		doctor=Doctor.objects.filter(name=d).first()
		patient=Patient.objects.filter(name=p).first()
		try:
			Appointment.objects.create(doctor=doctor,patient=patient,date1=d1,time1=t)
			error="no"
		except:
			error="yes"
	d={'doctor':doctor1,'patient':patient1,'error':error}
	return render(request,'add_appointment.html',d)


def Delete_Appointment(request,pid):
	if not request.user.is_staff:
		return redirect('login')
	appoint=Appointment.objects.get(id=pid)
	appoint.delete()
	return redirect('view_appointment')
