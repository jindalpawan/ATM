from django.urls import path
from . import views

app_name='machine'
urlpatterns = [
    path('user/deposite/', views.Deposite.as_view(), name='deposite'),
    path('user/withdraw/', views.Withdraw.as_view(), name='withdraw'),
    path('users/login/', views.AuthViewSet.as_view({'post': 'login'})),
    path('users/logout/', views.AuthViewSet.as_view({'get': 'logout'})),
    
]