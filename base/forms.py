from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User

#career roadmap
from .models import CareerRoadmap, Milestone

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']

#career roadmap
class CareerRoadmapForm(ModelForm):
    class Meta:
        model = CareerRoadmap
        fields = ['title', 'goal', 'notes']

class MilestoneForm(ModelForm):
    class Meta:
        model = Milestone
        fields = ['title', 'description', 'order']