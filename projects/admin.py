from django.contrib import admin
from .models import Project, Type, Genre, Progress

class GenreAdmin(admin.ModelAdmin):
  list_display = ["id", "name"]

class ProjectAdmin(admin.ModelAdmin):
  list_display = ["id", "name", "insertion_date", "user_id", "target_count"]
  filter_horizontal = ["genres"]

# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Type)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Progress)