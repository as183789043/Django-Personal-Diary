from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.sessions.models import Session  ##Sesion清除使用
from django.contrib import messages ## 類似flash訊息
from mysite import forms
from mysite import models
#使用Django 內建Auth機制
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
##plotly繪圖
from plotly.offline import plot
import plotly.graph_objs as go
import numpy as np
import os
from django.conf import settings
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
        try:
            user = User.objects.get(username=username)
            diaries = models.Diary.objects.filter(user=user).order_by('-ddate')
        except Exception as e :
            print(e)
            pass
    messages.get_messages(request)
    return render(request,"index.html",locals())

def login(request):
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_username = request.POST['username'].strip()
            login_password = request.POST['password']
            user = authenticate(username=login_username,password=login_password)
            if user is not None :
                if user.is_active:
                    auth.login(request,user)
                    messages.add_message(request,messages.SUCCESS,'成功登入了')
                    return redirect("/")
                else:
                    messages.add_message(request,messages.WARNING,'帳號尚未啟用')
            else:
                messages.add_message(request,messages.WARNING,'登入失敗')
        else:
            messages.add_message(request,messages.INFO,'請檢查輸入的欄位內容')
    else:
        login_form = forms.LoginForm()
    return render(request,'login.html',locals())

def logout(request):
    auth.logout(request)
    messages.add_message(request,messages.INFO,'成功登出了')
    return redirect('/')

@login_required(login_url='/login/')
def userinfo(request):
    if request.user.is_authenticated:
        username = request.user.username
    try:
        user = User.objects.get(username=username)
        userinfo = models.Profile.objects.get(user=user)
    except:
        pass
    return render(request,'userinfo.html',locals())


@login_required(login_url='/login/')
def posting(request):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)

    if request.method == 'POST':
        user = User.objects.get(username=username)
        diary = models.Diary(user=user)
        post_form = forms.DiaryForm(request.POST,instance=diary)
        if post_form.is_valid():
            messages.add_message(request,messages.INFO,'日記已儲存')
            post_form.save()
            return HttpResponseRedirect("/")
        else:
            messages.add_message(request.messages.INFO,'要張貼日記，每一個欄位都要填寫')
    else:
        post_form = forms.DiaryForm()
        messages.add_message(request,messages.INFO,'要張貼日記，每一個欄位都要填寫')
    return render(request,'posting.html',locals())

def votes(request):
    data = models.Vote.objects.all().order_by("-votes")
    return render(request,"votes.html",locals())

def plotly(request):
    data = models.Vote.objects.all().order_by("-votes")

    labels = [d.name for d in data]
    values = [d.votes for d in data]

    plot_div = plot(
        [go.Bar(x=values,y=labels,orientation='h')],output_type='div'
        )
    return render(request,'plotly.html',locals())

def chart3d(request):
    filename = os.path.join(settings.BASE_DIR,"3d.csv")
    with open(filename,'r',encoding='utf-8') as fp:
        rawdata = fp.readlines()
    rawdata = [
        (float(d.split(",")[0]),
        float(d.split(",")[1]),
        float(d.split(",")[2]),
        float(d.split(",")[3])) for d in rawdata]
    chart_data = np.array(rawdata).T
    plot_div = plot([go.Scatter3d(
                        x=chart_data[0],
                        y=chart_data[1],
                        z=chart_data[3],
                        mode='markers',
                        marker=dict(size=2 ,symbol ='circle'))],
                    output_type='div')
    return render(request,'chart3d.html',locals())

