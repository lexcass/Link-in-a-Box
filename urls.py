from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # Home page
    url(r'^$', views.login_user, name="home"),

    # User registration
    url(r'^register/', views.register_user, name="register"),

    # Email confirmation
    url(r'^confirm_email/(?P<user_id>\d+)/(?P<confirmation_code>\w+)/', views.confirm_email, name="confirm_email"),
    url(r'^confirmation_sent/', views.confirmation_sent, name="confirmation_sent"),

    # Password reset
    url(r'^password_reset/$', auth_views.password_reset, name="password_reset"),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name="password_reset_done"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name="password_reset_confirm"),
    url(r'^reset/complete/$', auth_views.password_reset_complete, name="password_reset_complete"),

    # Login/Logout
    url(r'^login/', views.login_user, name="login"),
    url(r'^logout/', views.logout_user, name="logout"),

    # Clipboard (changed in-app to "box" to fit name)
    url(r'^create_box/', views.create_clipboard, name="create_clipboard"),
    #url(r'^edit_clipboard/', views.edit_clipboard, name="edit_clipboard"),
    url(r'^my_box/', views.show_clipboard, name="show_clipboard"),
    url(r'^help/', views.help, name="help")
]
