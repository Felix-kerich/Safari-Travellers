from django.template.context_processors import static
from django.urls import path

from SafiriLink import settings
from . import views, admin
from .views import index_view,dashboard_view,register_view,login_view,book_view, daraja_view,home_view,logout_view

urlpatterns = [
    path('SafariLinkApp/', views.SafariLinkApp, name='SafariLinkApp'),
     path('', index_view, name='index'),  # Home page redirects to index.html
    path('dashboard/', dashboard_view, name='dashboard'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('book/', book_view, name='book'),
    path('homeDashboard/', home_view, name='home'),
    path('book_vehicle/', views.book_vehicle, name='book_vehicle'),
    path('daraja_view/',daraja_view, name='daraja'),
    path('logout/', logout_view, name='logout'),
    path('book_view/', views.book_view, name='book'),
    path('booking_receipt/', views.booking_receipt, name='receipt'),
    path('contact/', views.contact_view, name='contact'),
    path('notifications/', views.notifications_view, name='notifications')
    ]
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)