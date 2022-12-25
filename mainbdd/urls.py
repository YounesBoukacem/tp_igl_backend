from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns=[
    path('user_detail/<int:user_id>/', views.UserDetail.as_view()),
    path('reas_of_user/<int:user_id>/', views.ReasOfUser.as_view()),
    path('favs_of_user/<int:user_id>/', views.FavsOfUser.as_view()),
    path('offers_of_rea/<int:rea_id>/', views.OffersOfRea.as_view()),
    path('search_for_reas/', views.SearchForReas.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)