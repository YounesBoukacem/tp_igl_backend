from django.urls import path
from . import views


urlpatterns=[
    path('user_detail/<int:user_id>/', views.UserDetail.as_view()),
    path('reas_of_user/<int:user_id>/', views.ReasOfUser.as_view()),
    path('favs_of_user/<int:user_id>/', views.FavsOfUser.as_view()),
    path('offers_of_rea/<int:rea_id>/', views.OffersOfRea.as_view())
]