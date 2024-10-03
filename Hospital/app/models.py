from typing import Any
from django.db import models
from django.utils import timezone

# Create your models here.

class Patient(models.Model):               
    patient_Name = models.CharField(max_length=100)
    date_of_birth = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=50)
    address = models.TextField()
    last_visit = models.DateTimeField(default=timezone.now, null=True, blank=True)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.patient_Name
    

class Doctor(models.Model):               
    doctor_Name = models.CharField(max_length=100)
    date_of_birth = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=50)
    doctor_detail = models.CharField(max_length=200)
    address = models.TextField()
    
    def __str__(self):
        return self.doctor_Name
    


class Appointment(models.Model):
    Patient_ID = models.CharField(max_length=100)
    Department = models.CharField(max_length=100)
    Doctor_name = models.CharField(max_length=100)
    Appointment_date = models.DateField()
    Time_slot = models.TimeField()
    Token_Number = models.CharField(max_length=10, primary_key=True)
    Problem = models.CharField(max_length=100)

    def __str__(self):
        return f"Appointment {self.Token_Number} - {self.Patient_ID}"


class Payment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    patient_id = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    admission_date = models.DateField()
    discharge_date = models.DateField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    total_payable = models.DecimalField(max_digits=10, decimal_places=2)  # Updated field name
    payment_type = models.CharField(max_length=50)
    card_check_no = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Payment {self.patient_name} - {self.total_payable}"


class Service(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='services')
    service_name = models.CharField(max_length=255)
    treatment_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.service_name
    

class RoomAllotment(models.Model):
    ROOM_TYPES = [
        ('ICU', 'ICU'),
        ('General', 'General'),
        ('AC Room', 'AC Room'),
    ]

    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admission_date = models.DateField()
    discharge_date = models.DateField(null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Room {self.room_number} - {self.patient.patient_Name}"
    

    

