from django.contrib import admin
from .models import Patient, Doctor, Appointment, Payment, Service, RoomAllotment

# Register Patient model
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_Name', 'date_of_birth', 'age', 'phone', 'email', 'gender', 'address', 'last_visit', 'status')
    search_fields = ('patient_Name', 'email')

# Register Doctor model
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_Name', 'date_of_birth', 'specialization', 'experience', 'age', 'phone', 'email', 'gender', 'doctor_detail', 'address')
    search_fields = ('doctor_Name', 'email', 'specialization')

# Register Appointment model
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('Patient_ID', 'Department', 'Doctor_name', 'Appointment_date', 'Time_slot','Token_Number', 'Problem')
    search_fields = ('Patient_ID', 'Department', 'Doctor_name')

# Register Payment model
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'patient_name', 'department', 'doctor_name', 'admission_date', 'discharge_date', 'discount', 'total_payable', 'payment_type', 'card_check_no')
    search_fields = ('patient_id', 'patient_name', 'department', 'doctor_name', 'payment_type')

# Register Service model
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('payment', 'service_name', 'treatment_cost')
    search_fields = ('service_name', 'payment__patient_name')  

# Register RoomAllotment model
@admin.register(RoomAllotment)
class RoomAllotmentAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'patient_name', 'admission_date', 'discharge_date', 'doctor_name')
    search_fields = ('room_number', 'patient__patient_Name', 'doctor__doctor_Name', 'room_type')
    list_filter = ('room_type', 'admission_date', 'discharge_date')

    def patient_name(self, obj):
        return obj.patient.patient_Name
    patient_name.admin_order_field = 'patient'
    patient_name.short_description = 'Patient Name'

    def doctor_name(self, obj):
        return obj.doctor.doctor_Name
    doctor_name.admin_order_field = 'doctor'
    doctor_name.short_description = 'Doctor Name'
