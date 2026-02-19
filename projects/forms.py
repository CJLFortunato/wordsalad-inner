from django import forms
from . import models

class CreateProjects(forms.ModelForm):
  class Meta:
    model = models.Project
    fields = ['name', 'summary', 'target_count', 'genres', 'type_id']

class LogProgressProject(forms.ModelForm):
  class Meta:
    model = models.Progress
    fields = ['word_count']

class LogProgressDashboard(forms.ModelForm):
  class Meta:
    model = models.Progress
    fields = ['word_count', 'project_id']