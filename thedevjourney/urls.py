
from django.contrib import admin
from django.urls import path, include
from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('comments/delete/<uuid:pk>/', views.DeleteCommentConfirmView, name='comment-delete'),
    path ('login/', views.LoginView, name='login'),
    path('articles/<slug:slug>/', views.ArticleDetailView, name='article_detail'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sign-up/', views.SignUpForm.as_view(), name='signup'),
    path('admin/', admin.site.urls),
]
