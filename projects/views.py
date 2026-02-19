from django.shortcuts import render, redirect
from .models import Project, Progress, Genre, Type
from users.models import User
from django.contrib.auth.decorators import login_required
from django.utils.timezone import activate, localtime
from . import forms
from .utils.get_progress_color import get_progress_color
from .utils.format_donut_chart_data import format_donut_chart_data
from .utils.format_line_chart_data import format_line_chart_data

# Create your views here.
@login_required(login_url="/users/login")
def dashboard(request):
  projects = Project.objects.filter(user_id=request.user).order_by('-insertion_date')
  user = User.objects.get(id=request.user.id)
  activate(user.timezone)

  most_recent_progress = Progress.objects.filter(user_id=request.user).order_by('-insertion_date').first()
  most_recent_progress.color = get_progress_color((most_recent_progress.word_count / most_recent_progress.project_id.target_count) * 100)

  most_advanced_project = Progress.objects.filter(user_id=request.user).order_by('-word_count').first()
  most_advanced_project.color = get_progress_color((most_advanced_project.word_count / most_advanced_project.project_id.target_count) * 100)

  for project in projects:
    project.percentage = 0
    project.word_count = 0
    last_progress = Progress.objects.filter(project_id=project.id, user_id=request.user).order_by('-insertion_date').first()
    if last_progress is not None:
      project.percentage = round((last_progress.word_count / project.target_count) * 100, 1)
      project.word_count = last_progress.word_count
    project.color = get_progress_color(project.percentage)

  if request.method == "POST":
    form = forms.LogProgressDashboard(request.POST)

    if form.is_valid():
      # save with user
      new_progress = form.save(commit=False)
      new_progress.user_id = request.user
      new_progress.save()

      return redirect('projects:dashboard')

  else:
    form = forms.LogProgressDashboard()

  chart_data = format_donut_chart_data(projects)
  # print(chart_data)

  return render(request, 'projects/dashboard.html', {
    'projects': projects,
    'form': form,
    'chart_data': chart_data,
    'most_recent_progress': most_recent_progress,
    'most_advanced_project': most_advanced_project
  })

@login_required(login_url="/users/login")
def project_page(request, prj_id):
  # Using that instead of .get() to avoid getting an error if project doesn't exist
  # print(prj_id)
  user = User.objects.get(id=request.user.id)
  activate(user.timezone)

  project = Project.objects.filter(id=prj_id).first()
  genres = project.genres.all()
  progress = Progress.objects.filter(project_id=prj_id, user_id=request.user).order_by('-insertion_date')
  most_recent_count = progress.first()

  if project is None:
    return redirect('projects:dashboard')

  if project.user_id != request.user:
    return redirect('projects:dashboard')

  if most_recent_count is None:
    percentage = 0

  else:
    percentage = round((most_recent_count.word_count / project.target_count) * 100, 1)

  if request.method == "POST":
    form = forms.LogProgressProject(request.POST)

    if form.is_valid():
      # save with user
      new_progress = form.save(commit=False)
      new_progress.user_id = request.user
      new_progress.project_id = project
      new_progress.save()

      return redirect('projects:project', prj_id=project.id)

  else:
    form = forms.LogProgressProject()

  project.insertion_date = localtime(project.insertion_date).strftime("%d/%m/%Y %H:%M")
  for entry in progress:
    entry.insertion_date = localtime(entry.insertion_date).strftime("%d/%m/%Y %H:%M")

  datapoints = format_line_chart_data(progress.reverse(), project.target_count)

  # print(project.__dict__)
  return render(request, 'projects/project_page.html', {
    'project': project,
    'genres': genres,
    'progress': progress,
    'most_recent_count':most_recent_count,
    'percentage': percentage,
    'color': get_progress_color(percentage),
    'form': form,
    'datapoints': datapoints
  })

@login_required(login_url="/users/login")
def create_project(request):
  if request.method == "POST":
    form = forms.CreateProjects(request.POST)

    if form.is_valid():
      # save with user
      new_post = form.save(commit=False)
      new_post.user_id = request.user
      new_post.save()

      for genre in request.POST["genres"]:
        new_post.genres.add(genre)
        new_post.save()

      return redirect('projects:dashboard')

  else:
    form = forms.CreateProjects()

  return render(request, 'projects/create_project.html', {
    'form': form
  })

@login_required(login_url="/users/login")
def update_project(request, prj_id):
  project = Project.objects.filter(id=prj_id).first()
  # genres = project.genres.all()
  # print("update")
  # project.genres = genres
  id = project.id

  if request.method == "POST":
    form = forms.CreateProjects(request.POST)
    # print(form)
    if form.is_valid():
      # save with user
      # print(form["target_count"].value())
      project.name = form["name"].value()
      project.summary = form["summary"].value()
      project.target_count = form["target_count"].value()
      new_type = Type.objects.get(id=form["type_id"].value())
      project.type_id = new_type
      project.save()

      project.genres.clear()
      print(request.POST["genres"])
      print("length")
      print(len(request.POST["genres"]))
      for genre in request.POST["genres"]:
        # print(genre)
        new_genre = Genre.objects.get(id=genre)
        project.genres.add(new_genre)

      project.save()

      return redirect('projects:project', prj_id=id)

  else:
    form = forms.CreateProjects(instance=project)

  return render(request, 'projects/update_project.html', {
    'form': form,
    'project_id': id,
  })
