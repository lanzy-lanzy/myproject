from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db import DatabaseError
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import Skill, Project, TimelineEvent, Service, ContactMessage, SkillCategory


def home(request):
    """Home page with all sections"""
    skills = Skill.objects.filter(is_featured=True).select_related('category')[:12]
    projects = Project.objects.filter(is_featured=True)[:10]
    timeline_events = TimelineEvent.objects.all()[:6]
    services = Service.objects.filter(is_active=True)[:6]
    
    context = {
        'skills': skills,
        'projects': projects,
        'timeline_events': timeline_events,
        'services': services,
    }
    return render(request, 'portfolio/home.html', context)


def projects(request):
    """Projects listing page"""
    all_projects = Project.objects.all()
    
    context = {
        'projects': all_projects,
    }
    return render(request, 'portfolio/projects.html', context)


def contact(request):
    """Contact page"""
    return render(request, 'portfolio/contact.html')


@require_http_methods(["POST"])
@csrf_exempt
def contact_submit(request):
    """Handle contact form submission via HTMX"""
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    subject = request.POST.get('subject', '').strip()
    message = request.POST.get('message', '').strip()
    
    errors = {}
    
    if not name:
        errors['name'] = 'Name is required'
    if not email:
        errors['email'] = 'Email is required'
    elif '@' not in email:
        errors['email'] = 'Please enter a valid email'
    if not message:
        errors['message'] = 'Message is required'
    
    if errors:
        if request.headers.get('HX-Request'):
            return render(request, 'portfolio/partials/contact_form.html', {
                'errors': errors,
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
            })
        messages.error(request, 'Please fix the errors in the form.')
        return redirect('portfolio:contact')
    
    try:
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
    except DatabaseError:
        pass
    
    if request.headers.get('HX-Request'):
        return render(request, 'portfolio/partials/contact_success.html')
    
    messages.success(request, 'Thank you for your message! I will get back to you soon.')
    return redirect('portfolio:contact')
