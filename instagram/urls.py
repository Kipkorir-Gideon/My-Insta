from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,re_path
from . import views as app_views
from . import views


urlpatterns=[
    path('',views.homepage, name='homePage'),
    path('register/', views.user_register, name='register'),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name= "logout"),
    path("user", views.user_page, name = "userpage"),
    re_path(r'^comment/(?P<image_id>\d+)$',app_views.commenting,name='commenting'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)