from django.shortcuts import HttpResponseRedirect, render, reverse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages



from .models import Tickets, Profile
from .forms import adding_new_ticket_form, login_form, UserRegisterForm, UserUpdateForm, ProfileUpdateForm


# def index(request):
#     return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def services(request):
    return render(request, 'services.html')


def index(request):
    html = 'index.html'

    new = Tickets.objects.filter(
        ticket_status='New').order_by('-post_date')
    in_progress = Tickets.objects.filter(
        ticket_status='In Progress').order_by('-post_date')
    done = Tickets.objects.filter(
        ticket_status='Done').order_by('-post_date')
    invalid = Tickets.objects.filter(
        ticket_status='Invalid').order_by('-post_date')

    return render(request, html, {
        'new': new,
        'in_progress': in_progress,
        'done': done,
        'invalid': invalid
    })


@login_required
def new_ticket_form_view(request):
    html = 'genericform.html'

    if request.method == 'POST':
        form = adding_new_ticket_form(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Tickets.objects.create(
                title=data['title'],
                description=data['description'],
                ticket_status=data['ticket_status'],
                created_by=request.user,
                assigned_by=data['assigned_by']
            )
            return HttpResponseRedirect(reverse('index'))

    form = adding_new_ticket_form()

    return render(request, html, {'form': form})


@login_required
def dev_person_view(request, id):
    html = 'devperson.html'

    created = Tickets.objects.filter(created_by=id)
    assigned = Tickets.objects.filter(assigned_by=id)
    completed = Tickets.objects.filter(completed_by=id)

    return render(request, html,
                  {'created': created,
                   'assigned': assigned,
                   'completed': completed})


@login_required
def ticket_detail_view(request, id):
    html = 'ticket.html'

    ticket = Tickets.objects.filter(id=id)

    return render(request, html, {'ticket': ticket})


def login_view(request):
    html = 'genericform.html'

    if request.method == 'POST':
        form = login_form(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get(
                        'next',
                        reverse('index')
                    )
                )

    form = login_form()

    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def edit_ticket_view(request, id):
    html = 'genericform.html'

    instance = Tickets.objects.get(id=id)

    if request.method == 'POST':
        form = adding_new_ticket_form(
            request.POST,
            instance=instance
        )
        form.save()

        if instance.ticket_status == 'Done':
            instance.completed_by = instance.assigned_by
            instance.assigned_by = None
            form.save()
        elif instance.ticket_status == 'Invalid':
            instance.assigned_by = None
            instance.completed_by = None
            form.save()
        elif instance.ticket_status == 'In Progress' and instance.assigned_by is None:
            instance.assigned_by = instance.created_by
            instance.completed_by = None
            form.save()
        elif instance.assigned_by is not None:
            instance.ticket_status = 'In Progress'
            instance.completed_by = None
            form.save()

        return HttpResponseRedirect(reverse('index'))

    form = adding_new_ticket_form(instance=instance)

    return render(request, html, {'form': form})


def all_tickets_view(request):
    html = 'all_tickets.html'

    all_tickets = Tickets.objects.all()

    return render(request, html, {'all_tickets': all_tickets})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) 
        if form.is_valid():
            form.save() 
            username = form.cleaned_data.get('username') 
            messages.success(request, f'Your account has been created! You are now able to log in') 
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# Update it here
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile) 
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)