from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout

from django.db.models import Q
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

#career roadmap
from .models import CareerRoadmap, Milestone
from .forms import CareerRoadmapForm, MilestoneForm
from django.shortcuts import get_object_or_404


# Create your views here.


#rooms = [
#    {'id': 1, 'name': 'Lets learn python'},
 #   {'id': 2, 'name': 'Design with me'},
 #   {'id': 3, 'name': 'fronted developers'},

#]
def loginPage(request):

    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
                messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username OR Password does not exist')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An errror has occurred during registration')


    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,'participants':participants}
    return render(request, 'base/room.html',context)

from .models import Room

def room_list(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    rooms = Room.objects.filter(topic__name__icontains=q)
    context = {
        'rooms': rooms,
        'topics': Topic.objects.all(),  # if you want a dropdown or list of topics
        'query': q
    }
    return render(request, 'base/room_list.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    print('Create Room View Called!')
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_id_or_name = request.POST.get('topic')

        try:
    
            topic = Topic.objects.get(id=topic_id_or_name)
        except (Topic.DoesNotExist, ValueError):
            
            topic, created = Topic.objects.get_or_create(name=topic_id_or_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )

        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)  



def deleteRoom(request,pk):
        room = Room.objects.get(id=pk)

        if request.user != room.host:
            return HttpResponse('You are not allowed here!')

        if request.method == 'POST':
            room.delete()
            return redirect('home')

        return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages}) 

def jobsPage(request):
<<<<<<< HEAD
    return render(request, 'jobs.html')
=======
    jobs = [
        {
            "title": "Software Engineer Intern",
            "description": "Work with our backend team to build scalable APIs and maintain services.",
            "requirements": [
                "Proficient in Python and Django",
                "Familiar with Git/GitHub",
                "Understanding of REST APIs"
            ]
        },
        {
            "title": "Business Analyst Intern",
            "description": "Analyze market trends and customer behavior for product strategy.",
            "requirements": [
                "Strong Excel & SQL skills",
                "Good presentation skills",
                "Basic knowledge of business analytics"
            ]
        },
        {
            "title": "Frontend Developer",
            "description": "Create interactive user interfaces using modern JS frameworks.",
            "requirements": [
                "Proficient in HTML, CSS, JavaScript",
                "React or Vue experience",
                "Responsive design knowledge"
            ]
        },
        {
            "title": "Marketing Associate",
            "description": "Develop and manage marketing strategies for digital campaigns.",
            "requirements": [
                "SEO & SEM skills",
                "Excellent written communication",
                "Experience with Google Analytics"
            ]
        },
        {
            "title": "Data Scientist Intern",
            "description": "Help build machine learning models and run experiments.",
            "requirements": [
                "Python, NumPy, Pandas",
                "Basic ML knowledge",
                "Data storytelling skills"
            ]
        },
        {
            "title": "Finance Assistant",
            "description": "Assist with budgeting and forecasting tasks within the finance team.",
            "requirements": [
                "Understanding of accounting principles",
                "Excel & QuickBooks experience",
                "Strong attention to detail"
            ]
        },
        {
            "title": "Product Manager Intern",
            "description": "Collaborate with cross-functional teams to define features.",
            "requirements": [
                "Agile/Scrum familiarity",
                "Customer empathy",
                "Clear documentation habits"
            ]
        },
    ]
    return render(request, 'base/jobs.html', {'jobs': jobs})

>>>>>>> 6d65a7b (Final commit: updated jobs.html, views.py, and styling)

def workshopPage(request):
    return render(request, 'workshop.html')

#career roadmap

# View all user-created roadmaps
@login_required
def roadmapList(request):
    roadmaps = CareerRoadmap.objects.filter(user=request.user).order_by('-created')
    return render(request, 'career/roadmap_list.html', {'roadmaps': roadmaps})

# Create a new roadmap
@login_required
def createRoadmap(request):
    form = CareerRoadmapForm()
    if request.method == 'POST':
        form = CareerRoadmapForm(request.POST)
        if form.is_valid():
            roadmap = form.save(commit=False)
            roadmap.user = request.user
            roadmap.save()
            return redirect('roadmap-detail', pk=roadmap.pk)
    return render(request, 'career/create_roadmap.html', {'form': form})

# View roadmap + milestones
@login_required
def roadmapDetail(request, pk):
    roadmap = get_object_or_404(CareerRoadmap, pk=pk, user=request.user)
    milestones = roadmap.milestones.order_by('order')
    total = milestones.count()
    completed = milestones.filter(is_complete=True).count()
    percent = int((completed / total) * 100) if total > 0 else 0
    show_congrats = total > 0 and completed == total
    return render(request, 'career/roadmap_detail.html', {
        'roadmap': roadmap,
        'milestones': milestones,
        'total': total,
        'completed': completed,
        'percent': percent,
        'show_congrats': show_congrats
    })

# Delete roadmap
@login_required
def deleteRoadmap(request, pk):
    roadmap = get_object_or_404(CareerRoadmap, pk=pk, user=request.user)
    if request.method == 'POST':
        roadmap.delete()
        return redirect('career-roadmap-list')
    return render(request, 'base/delete.html', {'obj': roadmap})

# Add a milestone
@login_required
def addMilestone(request, pk):
    roadmap = get_object_or_404(CareerRoadmap, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MilestoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.roadmap = roadmap
            milestone.save()
            return redirect('roadmap-detail', pk=pk)
    else:
        form = MilestoneForm()
    return render(request, 'career/add_milestone.html', {'form': form, 'roadmap': roadmap})

# Edit a milestone
@login_required
def editMilestone(request, pk):
    milestone = get_object_or_404(Milestone, pk=pk)
    if milestone.roadmap.user != request.user:
        return HttpResponse("Not authorized")
    if request.method == 'POST':
        form = MilestoneForm(request.POST, instance=milestone)
        if form.is_valid():
            form.save()
            return redirect('roadmap-detail', pk=milestone.roadmap.pk)
    else:
        form = MilestoneForm(instance=milestone)
    return render(request, 'career/edit_milestone.html', {'form': form, 'milestone': milestone})

# Delete a milestone
@login_required
def deleteMilestone(request, pk):
    milestone = get_object_or_404(Milestone, pk=pk)
    if milestone.roadmap.user != request.user:
        return HttpResponse("Not authorized")
    if request.method == 'POST':
        milestone.delete()
        return redirect('roadmap-detail', pk=milestone.roadmap.pk)
    return render(request, 'base/delete.html', {'obj': milestone})

# Toggle milestone completion
@login_required
def toggleMilestoneCompletion(request, pk):
    milestone = get_object_or_404(Milestone, pk=pk)
    if milestone.roadmap.user != request.user:
        return HttpResponse("Not authorized")
    milestone.is_complete = not milestone.is_complete
    milestone.save()
    return redirect('roadmap-detail', pk=milestone.roadmap.pk)
