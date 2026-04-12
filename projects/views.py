from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import ProjectForm
from .models import Project

def project_list_view(request):
    projects = Project.objects.select_related('owner').order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
def create_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect('projects:detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'projects/create_project.html', {'form': form, 'is_edit': False})

def project_detail(request, project_id):
    project = get_object_or_404(Project.objects.select_related('owner').prefetch_related('participants'), id=project_id)
    return render(request, 'projects/project_details.html', {'project': project})


@login_required
def edit_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/create_project.html', {'form': form, 'is_edit': True})


@login_required
def complete_project_view(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id, owner=request.user)
        project.status = 'closed'
        project.save()
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        print(f"Ошибка в complete_project_view: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def toggle_participate(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id)
        user = request.user
        
        if project.owner == user:
            return JsonResponse({
                'status': 'error',
                'message': 'Автор не может участвовать в своём проекте'
            }, status=400)
        
        if user in project.participants.all():
            project.participants.remove(user)
            participant = False
        else:
            project.participants.add(user)
            participant = True
        
        return JsonResponse({
            'status': 'ok',
            'participant': participant
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
