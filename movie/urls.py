from django.contrib import admin
from django.urls import path, include
from user import views as user_view
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include('user.urls')),
    path('login/', user_view.Login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),
    path('register/', user_view.register, name='register'),
    path('create_playlist/', user_view.create_playlist, name='create_playlist'),
    path('add/<str:movie>', user_view.add_to_playlist, name='add_to_playlist'),
    path('playlists', user_view.playlist, name='playlist'),
    path('add/<str:movie>/<int:pk>', user_view.add_movie_playlist, name='add_movie_playlist')

]
