from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('post/<int:pk>/', views.blog_detail_view, name='blog-detail'),
    path('post/<int:pk>/edit/', views.edit_post_view, name='edit-post'),
    path('post/<int:pk>/delete/', views.delete_post_view, name='delete-post'),
    path('post/<int:pk>/like/', views.like_post_view, name='like-post'),
    path('post/<int:pk>/comment/', views.add_comment_view, name='add-comment'),
    path('post/<int:post_pk>/comment/<int:comment_pk>/delete/', views.delete_comment_view, name='delete-comment'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('create/', views.create_post_view, name='create-post'),
]
