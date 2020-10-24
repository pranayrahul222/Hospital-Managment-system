from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from datetime import timedelta

from .models import *
from .forms import *
# Create your views here.
"""import cv2
import numpy as np
import pickle
from tensorflow.python.keras.models import load_model,Model
base_model = load_model('E:/Django_projects/HospitalMgmt/weights_v5_final_2cls.13.hdf5')
embedding_predictor = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)
sc = pickle.load(open('E:/Django_projects/HospitalMgmt/svm_classifier.sav', 'rb'))
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


def Index(request):
    return render(request,'index.html')
"""
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
	#if not request.user.is_staff:
	#	return redirect('login')

	doctors=Doctor.objects.all().count()
	patients=Patient.objects.all().count()
	appointments=Appointment.objects.filter(doctor__isnull = False).count()

	ap = Appointment.objects.filter(date__range=[timezone.now().date()-timedelta(days=3), timezone.now()], doctor__isnull=False)
	doc = Doctor.objects.all()

	ctx = {'d': doctors, 'p': patients, 'a': appointments, 'appointments': ap, 'doctors': doc}

	return render(request, 'index.html', ctx)


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
	return redirect('home')
	

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
			Patient.objects.create(name=n, gender=g, mobile=m, address=a)
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
	appoint = Appointment.objects.filter(doctor__isnull=False)
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


def Book_Appointment(request):
	if request.method == 'POST':
		form = AppointmentForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Appointment Request Submitted Successfully")
	else:
		form = AppointmentForm()
	return render(request, 'book_appointment.html', {'form': form})
