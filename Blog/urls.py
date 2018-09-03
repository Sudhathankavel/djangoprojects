from django.urls import path
from Blog.views import HomePage, ContentPage, EditPage

app_name = 'Blog'
urlpatterns = [
    path('', HomePage.as_view(), name="homepage"),
    path('<id>', ContentPage.as_view(), name="Content"),
    path('<id>/edit/<secret_key>', EditPage.as_view(), name="homepage")
]