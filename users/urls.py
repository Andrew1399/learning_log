from django.urls import path, include
# from topics.views import logout
from users import views

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    # path('logout/', logout, name='logout'),
    path('register', views.register, name='register'),
    path('profile/<username>/', views.user_profile, name='profile'),
    path('profiles_list/', views.profiles_list, name='profiles_list'),
    path('<slug>/', views.ProfileDetailView.as_view(), name='detail')
]
