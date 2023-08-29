from django.urls import path

from . import views

urlpatterns = [
    path('login/',views.loginPage,name="loginPage"),
    path('logout/',views.logoutUser,name="logoutUser"),
    path('register/',views.registerUser,name="registerUser"),
    path('profile/<str:pk>',views.userProfile,name="userProfile"),
    path('',views.home,name="home"),
    path('rooms/<str:pk>',views.room,name="room"),
    path('room_form/',views.room_form,name="room_form"),
    path('room_edit/<str:pk>',views.updateRoom,name="room_edit"),
    path('room_delete/<str:pk>',views.deleteRoom,name="room_delete"),
    path('message_delete/<str:pk>',views.deleteMessage,name="message_delete"),
    path('update-user/',views.updateUser,name="user_update"),
    path('topics/',views.topicPage,name="topicPage"),
    path('activity/',views.activityPage,name="activityPage"),
]