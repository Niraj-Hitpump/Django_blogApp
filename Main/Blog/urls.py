from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('features/', views.features, name='features'),
    path('login/', views.loginUser, name='login'),  # Corrected to point to loginUser
    path('logout/', views.logoutUser, name='logout'),  # Added logout route
    path('add_blog/', views.add_Blog, name='add_blog'),
    path('blog_detail/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('see_blog/', views.see_blog, name='see_blog'), 
     path('update_blog/<slug>/', views.update_blog, name='update_blog'),
    path('delete_blog/<id>/', views.delete_blog, name='delete_blog'),

]
