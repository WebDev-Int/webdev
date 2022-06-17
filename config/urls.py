"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.static import serve
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from webdev import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.index, name='index'),
    path('about/', v.about, name='about'),
    path('contact/', v.contact, name='contact'),
    path('services/', v.services, name='services'),
    path('profile/', v.profile, name='profile'),
    path('newticketform/', v.new_ticket_form_view,
         name='newticketform'),
    path('login/', v.login_view, name='login'),
    path('logout/', v.logout_view, name='logout'),
    path('edit/<int:id>/', v.edit_ticket_view, name='edit'),
    path('dev/<int:id>/', v.dev_person_view, name='dev'),
    path('ticket/<int:id>/', v.ticket_detail_view, name='ticket'),
    path('tickets/', v.all_tickets_view, name='tickets'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += staticfiles_urlpatterns()

# urlpatterns = patterns('',
#                        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
#                         {'document_root': settings.MEDIA_ROOT}),
#                        )
