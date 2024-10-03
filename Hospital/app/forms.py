from django import forms
from .models import Payment
from app.models import RoomAllotment
from .models import Payment, Patient, Doctor, Appointment

class PaymentForm(forms.ModelForm):
    # Dropdowns for existing patients and doctors
    patient_id = forms.ModelChoiceField(queryset=Patient.objects.all(), label="Patient ID")
    doctor_name = forms.ModelChoiceField(queryset=Doctor.objects.all(), label="Doctor Name")
    appointment = forms.ModelChoiceField(queryset=Appointment.objects.all(), label="Appointment")

    class Meta:
        model = Payment
        fields = [
            'patient_id',  # Dropdown for existing patients
            'department',
            'doctor_name',  # Dropdown for existing doctors
            'admission_date',
            'discharge_date',
            'discount',
            'total_payable',  # Updated field name
            'payment_type',
            'card_check_no',
            'appointment',  # New appointment field
        ]
        widgets = {
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            'discharge_date': forms.DateInput(attrs={'type': 'date'}),
        }


class RoomAllotmentForm(forms.ModelForm):
    class Meta:
        model = RoomAllotment
        fields = ['room_number', 'room_type', 'patient', 'admission_date', 'discharge_date', 'doctor']
        widgets = {
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            'discharge_date': forms.DateInput(attrs={'type': 'date'}),
        }
