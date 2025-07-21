from django.urls import path
from . import views

urlpatterns = [
    # path('', views.test),
    path('login/', views.user_login.as_view(), name='login'),
    path('', views.signup), #'' it will work for default urls...
    path('home/', views.home, name='home'),
    path('mypost/', views.myPost.as_view(),name='mypost'),
    path('newpost/', views.newPost,name ='newpost'),
    path('signout/', views.signOut),
    path('post/<int:post_id>/', views.post_detail.as_view(), name='post_detail'),
    path('delete/<int:pk>/', views.delete_post.as_view(), name='delete_post'),

]
