
from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/',views.logoutUser, name='logout'),
    path('register/',views.registerPage, name='register'),

    path('', views.home, name="home"),
    path('room/<str:pk>/',views.room, name= "room"),
    path('rooms/', views.room_list, name="rooms"),
    path('profile/<str:pk>/',views.userProfile, name= "user-profile"),


    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:pk>',views.updateRoom,name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),  
    path('jobs/', views.jobsPage, name="jobs"),
    path('workshop/', views.workshopPage, name ="workshop"),
    path('career-roadmaps/', views.roadmapList, name='career-roadmap-list'),


    #career roadmap
    path('career-roadmaps/', views.roadmapList, name='career-roadmap-list'),
    path('career-roadmap/create/', views.createRoadmap, name='create-roadmap'),
    path('career-roadmap/<int:pk>/', views.roadmapDetail, name='roadmap-detail'),
    path('career-roadmap/<int:pk>/delete/', views.deleteRoadmap, name='delete-roadmap'),
    path('career-roadmap/<int:pk>/add-milestone/', views.addMilestone, name='add-milestone'),
    path('milestone/<int:pk>/edit/', views.editMilestone, name='edit-milestone'),
    path('milestone/<int:pk>/delete/', views.deleteMilestone, name='delete-milestone'),
    path('milestone/<int:pk>/toggle/', views.toggleMilestoneCompletion, name='toggle-milestone'),


]