from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns=[
   # path('test/', views.userr),
    path('auth/', views.login),
    path('user_detail/<int:user_id>/', views.UserDetail.as_view()),
    path('post_rea/<int:user_id>/', views.PostRea.as_view()),
    path('reas_of_user/<int:user_id>/', views.ReasOfUser.as_view()),
    path('favs_of_user/<int:user_id>/', views.FavsOfUser.as_view()),
    path('search_for_reas/', views.SearchForReas.as_view()),
    path('offers_of_rea/<int:rea_id>/', views.OffersOfRea.as_view()),
    path('offers_made_by_user/<int:user_id>/', views.OffersMadeByUser.as_view()),
    path('posting_offer/<int:rea_id>/', views.PostingOffer.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)