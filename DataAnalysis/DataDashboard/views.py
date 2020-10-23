from django.shortcuts import render
from django.http import HttpResponse
from .models import Data
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import io
import urllib, base64




# data_values = Data.objects.values()
#
# df = pd.DataFrame(data_values)
# df['empty_beds'] = df['Beds_Cap'] - df['Beds_occ']
# df['vent_rem'] = df['Max_Vent'] - df['Active_vent']
# df['non_covid'] = df['Beds_occ'] - df['Active_Covid']
# df['ICU_rem']  = df['Max_ICU'] - df['Active_ICU']
#
# new_df = df.loc[:,['Hospital', 'Beds_occ', 'empty_beds']]
# fig, axes = plt.subplots(nrows=1, ncols=2)
# new_df[["Hospital", "Beds_occ", "empty_beds"]].plot(x = "Hospital", title = "Beds Capacity",  kind="bar", rot = 45, color = ["red", "green"],  stacked = True, ax = axes[0, ])
# new_df1 = df.loc[:,['Hospital', 'Active_Covid', 'non_covid']]
# new_df1[["Hospital", "Active_Covid", "non_covid"]].plot(x = "Hospital", title = "Covid patients", kind="bar", rot = 45, color = ["red", "green"], stacked = True, ax = axes[1])


def home(request):
    # context = {
    #     'posts': Data.objects.all()
    # }
    # print(len(posts))
    # n = request.POST['Appollo']
    plt.clf()
    qs = Data.objects.filter(Hospital='Appollo')
    # x = qs[0].Max_Vent

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
    my_labels2 = 'COVID', 'NON-COVD'
    plt.subplot(223)
    plt.pie(data2, labels=my_labels2, autopct='%1.1f%%')
    plt.title("COVID patients")

    data3 = [qs[0].Active_ICU, qs[0].Max_ICU - qs[0].Active_ICU]
    my_labels3 = 'Active ICU', 'Non Active ICU'
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
    new_df[["Hospital", "Beds_occ", "empty_beds"]].plot(x="Hospital", title="Beds Capacity", kind="bar", rot=45,
                                                        color=["red", "green"], stacked=True, ax=axes[0,])
    new_df1 = df.loc[:, ['Hospital', 'Active_Covid', 'non_covid']]
    new_df1[["Hospital", "Active_Covid", "non_covid"]].plot(x="Hospital", title="Covid patients", kind="bar", rot=45,
                                                            color=["red", "green"], stacked=True, ax=axes[1])
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png')
    buf2.seek(0)
    string = base64.b64encode(buf2.read())
    uri2 = urllib.parse.quote(string)

    fig.clf()
    fig, axes = plt.subplots(nrows=1, ncols=2)
    new_df2 = df.loc[:, ['Hospital', 'Active_vent', 'vent_rem', ]]
    new_df2[["Hospital", "Active_vent", "vent_rem"]].plot(x="Hospital", title="Ventillators Usage",
                                                                kind="bar", color=["red", "green"], rot=45,
                                                                stacked=True, ax=axes[0])
    new_df3 = df.loc[:, ['Hospital', 'Active_ICU', 'ICU_rem', ]]
    new_df3[["Hospital", "Active_ICU", "ICU_rem"]].plot(x="Hospital", title="ICU Occupancy", kind="bar",
                                                               color=["red", "green"], rot=45, stacked=True, ax=axes[1])
    buf3 = io.BytesIO()
    plt.savefig(buf3, format='png')
    buf3.seek(0)
    string = base64.b64encode(buf3.read())
    uri3 = urllib.parse.quote(string)

    # plt.show()
    return render(request, 'DataDashboard/home.html', {'data':uri, 'data2':uri2, 'data3':uri3})
    # return HttpResponse('<h1>Home</h1>')
