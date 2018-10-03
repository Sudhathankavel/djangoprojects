from django.urls import path
from Blog.views import (ArticlesView, ClaimView, ContentPage, HomePage, EditPage,
                        LoginView, SignupView, LogoutView)

app_name = 'Blog'
urlpatterns = [
    path('', HomePage.as_view(), name="homepage"),
    path('<int:id>', ContentPage.as_view(), name="Content"),
    path('<int:id>/edit/<secret_key>', EditPage.as_view(), name="editPage"),
    path('<int:id>/edit/', EditPage.as_view(), name="LogUserEdit"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('mine/', ArticlesView.as_view(), name="mine"),
    path('<int:id>/claim/<secret_key>', ClaimView.as_view(), name="Claim"),
]