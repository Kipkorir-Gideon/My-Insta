from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns=[
    path('',views.homepage, name='homepage'),
    path('register/', views.user_register, name='register'),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name= "logout"),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)