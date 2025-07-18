from django.urls import path

from django.contrib.auth import views as auth_views

from .import views


urlpatterns = [
    path('register/',views.registerPage,name="register"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logOut,name="logout"),

    path('', views.home,name="dashboard"),
    path('user/', views.userPage,name="user"),

    path('account/', views.accountSettings, name="account"),

    path('customer/<str:pk>/',views.customer,name="customer"),
    path('products/',views.products,name="product"),
    path('create_order/<str:pk>/',views.createOrder,name='create_order'),
    # path('create_customer/',views.createCustomer,name='create_customer'),
    path('update_order/<str:pk>/',views.updateOrder,name='update_order'),
    # path('update_customer/<str:pk>/',views.updateCustomer,name='update_customer'),
    path('delete_order/<str:pk>/',views.deleteOrder,name='delete_order'),
    # path('delete_customer/<str:pk>/',views.deleteCustomer,name='delete_customer'),


    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name = 'accounts/password_reset.html'),
         name='reset_password'),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name = 'accounts/password_reset_sent.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name = 'accounts/password_reset_form.html'),
         name='password_reset_confirm'),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name = 'accounts/password_reset_done.html'),
         name='password_reset_complete'),



]