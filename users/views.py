from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.db.models import Q
import json
from .forms import RegistrationForm, LoginForm, ProfileEditForm
from django.contrib.auth.forms import PasswordChangeForm

from .models import Skill, UserSkill

User = get_user_model()

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/user_details.html', {'user': user})

def user_list(request):
    skill_name = request.GET.get('skill', '').strip()
    participants = User.objects.all()
    if skill_name:
        participants = participants.filter(
            user_skills__skill__name__iexact=skill_name
        ).distinct()
    context = {
        'participants': participants,
        'active_skill': skill_name,
        'skills': Skill.objects.all().order_by('name'),
    }
    return render(request, 'users/participants.html', context)

@login_required
@require_http_methods(["GET"])
def search_skills(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        skills = Skill.objects.none()
    else:
        skills = Skill.objects.filter(name__icontains=query)[:10]
    data = {
        'skills': list(skills.values('id', 'name'))
    }
    return JsonResponse(data)

@login_required
@require_http_methods(["POST"])
def add_skill(request):
    try:
        data = json.loads(request.body)
        skill_name = data.get('skill_name', '').strip()
        if not skill_name:
            return JsonResponse({
                'error': 'Навык не может быть пустым'
            }, status=400)
        if request.user.id != int(data.get('user_id')):
            return JsonResponse({
                'error': 'Нельзя добавить навык другому пользователю'
            }, status=403)
        skill, created = Skill.objects.get_or_create(
            name__iexact=skill_name,
            defaults={'name': skill_name}
        )
        user_skill, created = UserSkill.objects.get_or_create(
            user=request.user,
            skill=skill
        )
        if not created:
            return JsonResponse({
                'error': 'Этот навык уже добавлен'
            }, status=400)
        return JsonResponse({
            'success': True,
            'skill': {
                'id': skill.id,
                'name': skill.name,
                'user_skill_id': user_skill.id
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Неверный формат данных'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_http_methods(["DELETE"])
def remove_skill(request, user_skill_id):
    try:
        user_skill = get_object_or_404(UserSkill, id=user_skill_id)
        if user_skill.user != request.user:
            return JsonResponse({
                'error': 'Нельзя удалить навык другого пользователя'
            }, status=403)
        user_skill.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_user = authenticate(username=user.username, password=form.cleaned_data['password'])
            if login_user:
                login(request, login_user)
                return redirect('projects:project_list')
            else:
                return redirect('login')
        else:
            return render(request, 'users/register.html', {
                'form': form,
                'error': 'Проверьте правильность заполнения полей'
            })
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                authenticated_user = authenticate(username=user.username, password=password)
                if authenticated_user:
                    login(request, authenticated_user)
                    return redirect('projects:project_list')
                else:
                    return render(request, 'users/login.html', {
                        'form': form,
                        'error': 'Неверный email или пароль'
                    })
            except User.DoesNotExist:
                return render(request, 'users/login.html', {
                    'form': form,
                    'error': 'Неверный email или пароль'
                })
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('projects:project_list')

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile', user_id=request.user.id)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Пароль успешно изменён')
            return redirect('users:profile', user_id=request.user.id)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})