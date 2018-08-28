from django.urls import path, include
from django.conf.urls import url
from Blog.views import HomePage, ContentPage

app_name = 'Blog'
urlpatterns = [
    path('', HomePage.as_view(), name="homepage"),
    path('<id>', ContentPage.as_view(), name="Content")
]