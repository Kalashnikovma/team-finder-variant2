from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from .forms import ProjectForm
from users.models import User


def project_list(request):
    skill_name = request.GET.get('skill')
    projects = Project.objects.all().order_by('-created_at')
    
    if skill_name:
        projects = projects.filter()  # Пока без фильтра по навыкам проекта (вариант 2 — по пользователям)
    
    return render(request, 'projects/project_list.html', {
        'projects': projects,
        'active_skill': skill_name
    })


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            messages.success(request, "Проект успешно создан!")
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user:
        messages.error(request, "У вас нет прав на редактирование")
        return redirect('project_detail', pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Проект обновлён")
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})


@login_required
def complete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner == request.user and project.status == "open":
        project.status = "closed"
        project.save()
        messages.success(request, "Проект завершён")
    return redirect('project_detail', pk=pk)


@login_required
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user in project.participants.all():
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return redirect('project_detail', pk=pk)
