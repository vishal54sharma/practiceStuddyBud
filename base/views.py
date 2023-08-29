from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpResponse
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,MyUserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
rooms=[
    {'id':1,
     'name':'Lets learn Python'},
     {'id':2,
     'name':'Design With Me'},
     {'id':3,
     'name':'Frontend Developers'}
]


def loginPage(request):
    context={'type':'login'}
    print(context) 
    if(request.method=='POST'):
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:

            user = User.objects.get(email=email)
        except:
            messages.error(request,"User does not exist")

        user = authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username or Password does not exist")
     
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('loginPage')

def registerUser(request):
    form=MyUserCreationForm()
    context={'type':'register','form':form}

    if request.method=='POST':
        form= MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occured during registration")

    return render(request,'base/login_register.html',context)

def home(request):
    if request.GET.get('q')!=None:
        q=request.GET.get('q')  
    else:
        q=''

    rooms = Room.objects.filter(Q(topic__name__icontains=q)|Q(name__icontains=q)|Q(description__icontains=q))
    rooms_count=rooms.count()
    topics = Topic.objects.all()[0:3]
    room_messages = Message.objects.all()
    # for room in rooms:
    #     print(room.host.username)
    context = {'rooms':rooms,'topics':topics,'rooms_count':rooms_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all()


    
    context = {'user': user,'rooms':rooms,'topics':topics,'room_messages':room_messages}
    return render(request,'base/profile.html',context)

@login_required(login_url='/login')
def room(request,pk):
    room=Room.objects.get(id=pk)
    
    participants = room.participants.all()
    
    room_messages = room.message_set.all().order_by('-created')
    if request.method=='POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    


    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)

@login_required(login_url='/login')
def room_form(request):

    form = RoomForm()
    if(request.method=='POST'):
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host= request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        # form=RoomForm(request.POST)
        # if(form.is_valid()):
        #     form.save()
        return redirect('home')
    context = {'form':form, 'topics':Topic.objects.all()}
    return render(request,'base/room_form.html',context)

@login_required(login_url='/login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if(request.method=='POST'):
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()


        return redirect('home')
    context = {'form':form,'topics':Topic.objects.all(),'room':room}
    return render(request,'base/room_form.html',context)


@login_required(login_url='/login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method=="POST":
        room.delete()
        return redirect('home')
    return render(request,'base/delete_room.html',{"obj":room})

@login_required(login_url='/login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    #room = Room.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed here")

    
    if request.method=="POST":
        message.delete()
        return redirect('home')
    
    return render(request,'base/delete_room.html',{"obj":message})

@login_required(login_url='/login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('userProfile',pk=user.id)

    return render(request,'base/update-user.html',{'form':form})



def topicPage(request):
    if request.GET.get('q')!=None:
        q=request.GET.get('q')  
    else:
        q=''

   
    topic = Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics':topic})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request,'base/activity.html',{"room_messages":room_messages})




    


    