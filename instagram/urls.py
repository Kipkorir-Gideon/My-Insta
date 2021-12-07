from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,re_path
from . import views as app_views
from . import views
from django.conf.urls import include


urlpatterns=[
    path('',views.homepage, name='homePage'),
    # path('accounts/register/', views.user_register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("user", views.user_page, name = "userpage"),
    re_path(r'^comment/(?P<image_id>\d+)$',app_views.commenting,name='commenting'),
    re_path(r'^allcomments/(?P<image_id>\d+)$',app_views.all_comments,name='all_comments'),
    re_path(r'^likes/(?P<image_id>\d+)', app_views.likes, name='likes'),
    re_path(r'^userpost/(?P<pk>\d+)$',app_views.user_page, name='userpage'),
    re_path(r'^userprofile/(?P<pk>\d+)$',app_views.users_profile, name='users_profile'),
    re_path(r'^search/$',app_views.search,name='search'),
    path('post/',app_views.posting,name='post'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)