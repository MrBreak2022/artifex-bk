from django.urls import path
from . views import *

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='my_token_obtain_pair'),
    path('register/', RegisterView.as_view(), name="sign_up"),
    path('profile/', getUserProfile, name="user-profile"),
    path('profile/update/', updateUserProfile, name="user-profile-update"),
    path('users/', getUsers, name="users"),
    path('users/<str:pk>/', getUserById,name="get_user"),
    path('users/edit/<str:pk>/', updateUser, name="user-edit"),
    path('users/delete/<str:pk>/', deleteUser, name="user-delete")
]