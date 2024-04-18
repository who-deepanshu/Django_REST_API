from home.views import index, person, login, PersonAPI, PeopleViewSet, RegisterAPI, LoginAPI
from django.urls import path, include
from rest_framework.routers import DefaultRouter


# Viewset are registers as - 
router = DefaultRouter()
router.register(r'people', PeopleViewSet, basename='people')
urlpatterns = router.urls


urlpatterns = [
    path('index/', index),
    path('person/', person),
    path('login/', LoginAPI.as_view()),
    path('persons/', PersonAPI.as_view()),
    path('', include(router.urls)),
    path('register/', RegisterAPI.as_view()),

]
