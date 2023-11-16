from django.urls import path
from base.views import user_views as views

urlpatterns = [
    # path('',views.getUsers,name='users'),
    # path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('profile/',views.UserProfileView.as_view(),name='user-profile'),
    # path('register/',views.registerUser,name='register-user'),
    # path('profile/update/', views.updateUserProfile, name='update-profile'),

    path('', views.GetAllUsersView.as_view(), name='all-users'),
    path('register/', views.UserRegistrationView.as_view(), name='register-user'),
    path('login/', views.UserLoginView.as_view(), name='login-user'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('password/change/', views.UserChangePasswordView.as_view(), name='password-change'),
    path('password/reset/email/', views.SendPasswordResetEmailView.as_view(), name='password-reset-email'),
    path('password/reset/<uid>/<token>/', views.UserPasswordResetView.as_view(), name='password-reset'),
]
