from django.db import models
from users.models import User

# Create your models here.
class Type(models.Model):
  name = models.CharField(max_length=100, blank=False)

  def __str__(self):
    return self.name

class Genre(models.Model):
  name = models.CharField(max_length=100, blank=False)

  def __str__(self):
    return self.name

class Project(models.Model):
  name = models.CharField(max_length=100, blank=False)
  summary = models.TextField(blank=True)
  insertion_date = models.DateTimeField(auto_now_add=True)
  target_count = models.IntegerField(blank=False)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
  type_id = models.ForeignKey(Type, on_delete=models.SET(1), default=None, verbose_name="Type")
  genres = models.ManyToManyField(
    Genre,
    db_table="project_genre"
  )

  def __str__(self):
    return self.name

class Progress(models.Model):
  word_count = models.IntegerField(blank=False)
  insertion_date = models.DateTimeField(auto_now_add=True)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
  project_id = models.ForeignKey(Project, on_delete=models.CASCADE, default=None, verbose_name="Project")

  def __str__(self):
    return self.project_id.__str__() + self.word_count.__str__()