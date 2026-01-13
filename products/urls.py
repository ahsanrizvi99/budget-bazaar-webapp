from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.product_list, name='product_list'), 
    path('register/', views.register, name='register'),  
    path('login/', views.user_login, name='login'),  
    path('logout/', views.user_logout, name='logout'),  
    path('search/', views.product_search, name='product_search'),  
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

