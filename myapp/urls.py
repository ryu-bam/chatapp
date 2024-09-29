from django.urls import path
from . import views

app_name = "myapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:friend_id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('update/<int:update_id>', views.update, name='update'),
    path('updated/<int:updated_id>', views.updated, name='updated'),
    path('password_update', views.PasswordChange.as_view(), name='password_update'),
    path('password_updated', views.password_updated, name='password_updated'),
    path('logout', views.logout_view, name='logout_view'),
]
