from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('create', views.create_project, name="create_project"),
    path('update/<int:prj_id>', views.update_project, name="update_project"),
    path('<int:prj_id>', views.project_page, name="project"),
]