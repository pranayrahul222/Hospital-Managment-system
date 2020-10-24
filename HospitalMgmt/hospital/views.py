from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from datetime import timedelta
from django.core.files.storage import FileSystemStorage

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import io
import urllib, base64
from .models import *
from .forms import *
# Create your views here.
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


# def Index(request):
#     return render(request,'index.html')

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
    plt.clf()
    qs = Data.objects.filter(Hospital='Apollo')
    #print(type(qs))
    data4 = [qs[0].Beds_occ, qs[0].Beds_Cap - qs[0].Beds_occ]
    my_labels4 = 'Beds Occupied', 'Beds Remaining'
    plt.subplot(221)
    plt.pie(data4, labels=my_labels4, autopct='%1.1f%%')
    plt.title("Beds Availability")

    data1 = [qs[0].Active_vent, qs[0].Max_Vent - qs[0].Active_vent]
    my_labels1 = 'Being Used', 'Remaining'
    plt.subplot(222)
    plt.pie(data1, labels=my_labels1, autopct='%1.1f%%')
    plt.title("Ventillators")

    data2 = [qs[0].Active_Covid, qs[0].Beds_occ - qs[0].Active_Covid]
    my_labels2 = ['COVID', 'NON-COVD']
    plt.subplot(223)
    plt.pie(data2, labels=my_labels2, autopct='%1.1f%%')
    plt.title("COVID patients")

    data3 = [qs[0].Active_ICU, qs[0].Max_ICU - qs[0].Active_ICU]
    my_labels3 = ['Active ICU', 'Non Active ICU']
    plt.subplot(224)
    plt.pie(data3, labels=my_labels3, autopct='%1.1f%%')
    plt.title("ICU DATA")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    plt.clf()
    data_values = Data.objects.values()

    df = pd.DataFrame(data_values)
    df['empty_beds'] = df['Beds_Cap'] - df['Beds_occ']
    df['vent_rem'] = df['Max_Vent'] - df['Active_vent']
    df['non_covid'] = df['Beds_occ'] - df['Active_Covid']
    df['ICU_rem'] = df['Max_ICU'] - df['Active_ICU']

    new_df = df.loc[:, ['Hospital', 'Beds_occ', 'empty_beds']]
    fig, axes = plt.subplots(nrows=1, ncols=2)
    new_df[["Hospital", "Beds_occ", "empty_beds"]].plot(x="Hospital", title="Beds Capacity", kind="bar", rot=45,color=["red", "green"], stacked=True, ax=axes[0,])
    new_df1 = df.loc[:, ['Hospital', 'Active_Covid', 'non_covid']]
    new_df1[["Hospital", "Active_Covid", "non_covid"]].plot(x="Hospital", title="Covid patients", kind="bar", rot=45,color=["red", "green"], stacked=True, ax=axes[1])

    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png')
    buf2.seek(0)
    string = base64.b64encode(buf2.read())
    uri2 = urllib.parse.quote(string)

    fig.clf()
    fig, axes = plt.subplots(nrows=1, ncols=2)
    new_df2 = df.loc[:, ['Hospital', 'Active_vent', 'vent_rem', ]]
    new_df2[["Hospital", "Active_vent", "vent_rem"]].plot(x="Hospital", title="Ventillators Usage",kind="bar", color=["red", "green"], rot=45,stacked=True, ax=axes[0])
    new_df3 = df.loc[:, ['Hospital', 'Active_ICU', 'ICU_rem', ]]
    new_df3[["Hospital", "Active_ICU", "ICU_rem"]].plot(x="Hospital", title="ICU Occupancy", kind="bar",color=["red", "green"], rot=45, stacked=True, ax=axes[1])
    buf3 = io.BytesIO()
    plt.savefig(buf3, format='png')
    buf3.seek(0)
    string = base64.b64encode(buf3.read())
    uri3 = urllib.parse.quote(string)

    doctors=Doctor.objects.all().count()
    patients=Patient.objects.all().count()
    appointments=Appointment.objects.filter(doctor__isnull = False).count()

    ap = Appointment.objects.filter(date__range=[timezone.now().date()-timedelta(days=3), timezone.now()], doctor__isnull=False)
    doc = Doctor.objects.all()

    ctx = {'d': doctors, 'p': patients, 'a': appointments, 'appointments': ap, 'doctors': doc,'data':uri, 'data2':uri2, 'data3':uri3}
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
