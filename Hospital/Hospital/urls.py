from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('base/', views.BASE, name='base'),

    # Patient URLs
    path('Patient/add/', views.ADD_PATIENT, name='add_patient'),
    path('Patient/all/', views.PATIENTS, name='PATIENTS'),
    path('Patient/abt_pat/', views.about_patient, name='about_patient'),
    path('Patient/edit_pat/', views.Edit_patient, name='edit_patient'),

    # Ensure this URL pattern matches the search functionality
    path('Patient/search/', views.about_patient, name='about_patient'),
    # New URL pattern for searching patients
    path('Patient/search/', views.patient_search, name='patient_search'),
    # New URL pattern for viewing patient details
    path('Patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),

    path('', views.home, name='home'),

    # Doctor URLs
    path('Doctor/all/', views.DOCTORS, name='doctors'),
    path('Doctor/about/', views.about_doctor, name='about_doctor'),
    path('Doctor/edit_doc/', views.Edit_doc, name='edit_doc'),
    path('Doctor/add/', views.ADD_DOC, name='add_doctor'),

    # Appointment URLs
    path('Appointment/add/', views.ADD_APPOINTMENT, name='add_appointment'),
    path('Appointment/all/', views.APPOINTMENTS, name='appointments'),
    path('Appointment/abt/', views.About_Appointment, name='about_appointment'),
    path('Appointment/edit/', views.Edit_Appointment, name='edit_appointment'),

    # Payment URLs
    path('Payment/add/', views.ADD_Payment, name='add_payment'),
    path('Payment/all/', views.payments, name='payments'),
    path('Payment/invoice/', views.Invoice_Payments, name='pay_invoice'),

    path('invoice/<int:payment_id>/', views.download_invoice, name='invoice_pdf'),

    # RoomA URLs
    path('RoomA/add/', views.add_room_allotment, name='add_room'),
    path('RoomA/avl/', views.Roomavl, name='rooms'),
    path('RoomA/edit/', views.Edit_Room, name='edit_room'),


    # path('home/', views.home, name='home'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
