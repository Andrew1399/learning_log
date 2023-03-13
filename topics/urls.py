from django.urls import path
from topics import views

app_name = 'topics'

urlpatterns = [
    path('home/', views.index, name='index'),
    path('topics/', views.get_topics, name='topics'),
    path('topics/<int:topic_id>/', views.get_single_topic, name='topic'),
    path('topics/new_topic/', views.new_topic, name='new_topic'),
    path('topics/new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('topics/edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('topics/public_topics', views.users_public_topics, name='public_topics'),
    path('topics/delete/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    path('topics/delete/<int:topic_id>/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('topics/like/<int:pk>/', views.like_topic, name='like_topic')
]
