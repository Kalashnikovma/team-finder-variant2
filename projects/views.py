from http import HTTPStatus

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from .forms import ProjectForm
from .models import Project


def project_list_view(request):
    projects = Project.objects.select_related('owner').order_by('-created_at')
    
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'projects/project_list.html', {'page_obj': page_obj})


@login_required
def create_project_view(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect("projects:detail", project_id=project.id)
    else:
        form = ProjectForm()
    return render(
        request, "projects/create_project.html", {"form": form, "is_edit": False}
    )


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("participants"),
        id=project_id,
    )
    return render(request, "projects/project_details.html", {"project": project})


@login_required
def edit_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects:detail", project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(
        request, "projects/create_project.html", {"form": form, "is_edit": True}
    )


@login_required
def complete_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    project.status = "closed"
    project.save()
    return JsonResponse({"status": "ok"})


@login_required
@require_http_methods(["POST"])
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user

    if project.owner == user:
        return JsonResponse(
            {
                "status": "error",
                "message": "Автор не может участвовать в своём проекте",
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    is_participant = project.participants.filter(id=user.id).exists()
    if is_participant:
        project.participants.remove(user)
        participant = False
    else:
        project.participants.add(user)
        participant = True

    return JsonResponse({"status": "ok", "participant": participant})
