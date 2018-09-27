from django.urls import path
from Blog.views import HomePage, ContentPage, EditPage,SignupView,LoginView,ArticlesView,LogoutView

app_name = 'Blog'
urlpatterns = [
    path('', HomePage.as_view(), name="homepage"),
    path('<int:id>', ContentPage.as_view(), name="Content"),
    path('<int:id>/edit/<secret_key>', EditPage.as_view(), name="homepage"),
    path('<int:id>/edit/', EditPage.as_view(), name="homepage"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('mine/', ArticlesView.as_view(), name="mine")
]