#sending data

from django.views.decorators.csrf import csrf_exempt # command for csrf exemption
import json
from django.http import JsonResponse,HttpResponseRedirect

from .models import sensorreadings,plant
from django.core import serializers
#login
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm,plantForm,deleteForm


#sending data
data = []
@csrf_exempt #CROSS SITE REQUEST FORGERY
def index(request): #A FUNCTION TO RECIEVE REQUESTS IS CALLED WHEN WEATHER URL IS CALLED
    if request.method == 'POST':
        data.append(json.loads(json.dumps({"temperature": json.loads((request.body).decode('utf-8')).get('temperature'), "humidity": json.loads((request.body).decode('utf-8')).get('humidity'),"moisture": json.loads((request.body).decode('utf-8')).get('moisture'), "date": json.loads((request.body).decode('utf-8')).get('date'),"detect": json.loads((request.body).decode('utf-8')).get('detect'),"level": json.loads((request.body).decode('utf-8')).get('level'),"pid": json.loads((request.body).decode('utf-8')).get('pid')})))
        p=json.loads((request.body).decode('utf-8')).get('pid')
        a = sensorreadings.objects.create(temp=json.loads((request.body).decode('utf-8')).get('temperature'),humd=json.loads((request.body).decode('utf-8')).get('humidity'),moi=json.loads((request.body).decode('utf-8')).get('moisture'),date=json.loads((request.body).decode('utf-8')).get('date'),detect=json.loads((request.body).decode('utf-8')).get('detect'),level=json.loads((request.body).decode('utf-8')).get('level'),pid=plant(p))
        a.save() #WE CREATE A OBJECT TO STORE SENSOR READINGS AND THEN WE STORE THOSE READING INTO THE DATABASE
                 #JSON MEANS JAVA SCRIPT OBJECT NOTATION , WE CONVERTING FROM JSON TO DICTIONERY
        return JsonResponse(data,safe=False) #SENDING DATA TO HTML PAGE
    if request.method == 'GET':
        return JsonResponse(json.loads(json.dumps(data)), safe=False) #WHEN THE BROWSER REQUESTS DATA WE SEND JSON RESPONSE


def plants(requests): #A FUNCTION WHICH RETURNS ALL PLANTS WHEN PLANTS/ URL IS CALLED
    all_p=plant.objects.all() # all the stored plant details are retrived
    arr=[] #an empty array
    for p in all_p: #A FOR LOOP
        arr.append(p.pid1)
        print(arr)
    return JsonResponse({'pids':arr},safe=True)


def pindex(request,pid1): #A FUNCTION TO FETCH THE DETAILS OF A PRATICULAR PLANT WE WANT
    all_plants = plant.objects.all() # all the stored plant details are retrived
    html = []
    for plants in all_plants:
        if(str(plants.pid1)) == str(pid1): #CHECKS IF QUERIED PLANT ID AND PLANT ID IN DATABASE IS SAME
            html = {"pid1":plants.pid1,"latitude":plants.latitude,"longitude":plants.longitude} # DICTIONARY
    html1 = list(map(lambda x: x['fields'],json.loads(serializers.serialize('json',sensorreadings.objects.filter(pid=pid1)))))
    return JsonResponse({"loc":html, "values":html1}, safe=False)

@login_required #these @ are known as decorators .Here they help us to view the graph only if we succesfully furnish our login details
def graph(request): #FUNCTION IS CALLED WHEN graph/ url is called
    p = sensorreadings.objects.filter(pid=1)[::-1][0] #returns the latest sensor reading of the desired plant id
    # print('temp', p.moi)
    return render(request,"index.html",{'k':p}) # data is rendered to index.html in the form of dictionary

@login_required
def maps(request):
    for k in sensorreadings.objects.all():
        print(k.moi)
    return render(request,"maps.html",{'k':k})

#login
@csrf_exempt
def login_user(request):
    if request.method == "POST":#getting user details from the page
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)#check if the user is there in database
        if user is not None:
            if user.is_active:
                login(request, user)#login user and redirect to index page
                flag=1
                #return render(request, 'index.html')
                return HttpResponseRedirect('/weather/graph')
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')

@csrf_exempt
def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #return render(request,'index.html')
                return HttpResponseRedirect('/weather/graph')
    context = {
        "form": form,
    }
    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/weather/login')

#function to add plants
@login_required
def addplants(request):
    form = plantForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            pid1 = form.cleaned_data['pid1']
            longitude = form.cleaned_data['longitude']
            latitude = form.cleaned_data['latitude']
            print(pid1)
            print(longitude)
            foo = plant.objects.create(pid1 = int(pid1),latitude = float(latitude), longitude = float(longitude))
            return HttpResponseRedirect('/weather/graph') #we are redirected to home page
        else:
            form = plantForm()
    return render(request,'addplants.html',{'form':form})

#function to remove plants
def removeplants(request):
    form=deleteForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            pid1= form.cleaned_data['pid1']
            p=plant.objects.filter(pid1=pid1)
            p.delete()
            return HttpResponseRedirect('/weather/graph')
        else:
            form = deleteForm()
    return render(request,'removeplants.html',{'form':form})

#functiom to modify plant details
#def modifyplants(request):
