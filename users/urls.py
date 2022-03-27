from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('new/', views.UserCreateView.as_view(), name='create-form'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='update-form'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('profile/editview/', views.EditProfile.as_view(), name='edit-profile-view'),
]
