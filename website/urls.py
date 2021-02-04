from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="website/index.html")),
    path('search', views.Search.as_view()),
    path('download/<query>', views.DownloadCSV.as_view()),
]