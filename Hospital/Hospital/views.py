from django.shortcuts import get_object_or_404, render,redirect
from app.models import Appointment, Doctor, Patient, Payment, Service , RoomAllotment
from datetime import datetime , timedelta
from app.forms import PaymentForm , RoomAllotmentForm
from django.http import HttpResponse, JsonResponse
from django.db.models import CharField, Value as V
from django.db.models.functions import Cast
from django.db.models import Sum
from django.utils.timezone import now


from django.utils.dateparse import parse_date


def BASE(request):
    return render(request ,'base.html')


def ADD_PATIENT(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        status = request.POST.get('status')
        last_visit_date = request.POST.get('last_visit_date')

        # Combine date into a single datetime object with default time if provided
        if last_visit_date:
            last_visit = datetime.strptime(last_visit_date, '%Y-%m-%d')
        else:
            last_visit = None

        patient = Patient(
            patient_Name=patient_name,
            date_of_birth=dob,
            age=age,
            phone=phone,
            email=email,
            gender=gender,
            address=address,
            status=status,
            last_visit=last_visit
        )
        patient.save()
        


    return render(request, 'patients/add_patient.html')



def ADD_DOC(request):
    if request.method == 'POST':
        doctor_name = request.POST.get('doctor_name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        specialization = request.POST.get('specialization')  
        experience = request.POST.get('experience')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        doctor_detail = request.POST.get('doctor_detail')  
        address = request.POST.get('address')

        doctor = Doctor(
            doctor_Name=doctor_name,
            date_of_birth=dob,
            age=age,
            specialization=specialization,  
            experience=experience,  
            phone=phone,
            email=email,
            gender=gender,
            doctor_detail=doctor_detail, 
            address=address
        )
        
        doctor.save()

    return render(request, 'doctor/add_doc.html')



def ADD_APPOINTMENT(request):
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        patient_id = request.POST.get('patient-id')
        department = request.POST.get('department')
        doctor_name = request.POST.get('doctor-name')
        appointment_date = request.POST.get('appointment-date') 
        time_slot = request.POST.get('time-slot')  
        problem = request.POST.get('problem')
        
        try:
            appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            time_slot = datetime.strptime(time_slot, '%H:%M').time()
        except ValueError as e:
            print(f"Error parsing date/time: {e}")
            return render(request, 'appointments/add_appointment.html', {
                'patients': patients,
                'doctors': doctors,
                'error': 'Invalid date or time format'
            })

        appointment = Appointment(
            Patient_ID=patient_id,
            Department=department,
            Doctor_name=doctor_name,
            Appointment_date=appointment_date,
            Time_slot=time_slot,
            Problem=problem,
        )
        
        appointment.save()
        return render(request, 'appointments/add_appointment.html', {
            'patients': patients,
            'doctors': doctors,
            'success': True
        })

    return render(request, 'appointments/add_appointment.html', {
        'patients': patients,
        'doctors': doctors
    })



# def ADD_Payment(request):
#     if request.method == 'POST':
#         form = PaymentForm(request.POST)
#         if form.is_valid():
#             # Save the payment data
#             payment = form.save()

#             # Get the list of service names and costs from the form
#             service_names = request.POST.getlist('service_name[]')
#             service_costs = request.POST.getlist('treatment_cost[]')

#             # Save each service associated with the payment
#             for service_name, treatment_cost in zip(service_names, service_costs):
#                 if service_name and treatment_cost:
#                     Service.objects.create(
#                         payment=payment,
#                         service_name=service_name,
#                         treatment_cost=treatment_cost
#                     )

#             return redirect('payments') 
#         else:
#             print("Form errors:", form.errors)  

#     else:
#         form = PaymentForm()  

#     return render(request, 'Payment/add_payment.html', {'form': form})
def ADD_Payment(request):
    if request.method == 'POST':
        # Get form data from POST request
        appointment_id = request.POST.get('appointment')  # Get the selected appointment ID
        patient_id = request.POST.get('patient_id')
        department = request.POST.get('department')
        doctor_name = request.POST.get('doctor_name')
        admission_date = request.POST.get('admission_date')  # Expected in YYYY-MM-DD format
        discharge_date = request.POST.get('discharge_date')  # Expected in YYYY-MM-DD format
        discount = request.POST.get('discount')
        total_payable = request.POST.get('total_payable')
        payment_type = request.POST.get('payment_type')
        card_check_no = request.POST.get('card_check_no')  # Optional, may be blank

        # Fetch the appointment object
        try:
            appointment = Appointment.objects.get(Token_Number=appointment_id)
        except Appointment.DoesNotExist:
            # Handle invalid appointment selection
            return HttpResponse("Invalid appointment selected")

        # Fetch the patient object using patient_id
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            # Handle invalid patient selection
            return HttpResponse("Invalid patient selected")

        # Get the patient_name from the patient object (using 'patient_Name' field)
        patient_name = patient.patient_Name  # Correct field from Patient model

        # Save the payment
        payment = Payment(
            appointment=appointment,
            patient_id=patient_id,
            patient_name=patient_name,  # Assign the patient's name from the 'patient_Name' field
            department=department,
            doctor_name=doctor_name,
            admission_date=admission_date,  # Make sure this is not null
            discharge_date=discharge_date,  # Make sure this is not null
            discount=discount,
            total_payable=total_payable,
            payment_type=payment_type,
            card_check_no=card_check_no,  # Can be blank or null
        )
        
        try:
            payment.save()
        except Exception as e:
            return HttpResponse(f"Error saving payment: {e}")

        # After saving, render 'Payment/pay_invoice.html'
        return render(request, 'Payment/pay_invoice.html', {'payment': payment})

    # For GET requests, render the form
    patients = Patient.objects.all()
    appointments = Appointment.objects.all()
    doctors = Doctor.objects.all()

    return render(request, 'Payment/add_payment.html', {
        'patients': patients,
        'appointments': appointments,
        'doctors': doctors,
    })



 


def add_room_allotment(request):
    if request.method == 'POST':
        form = RoomAllotmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms')
    else:
        form = RoomAllotmentForm()
    
    return render(request, 'Room_allotment/add_roomalt.html', {'form': form})



def PATIENTS(request):
    all_Patients = Patient.objects.all
    return render(request , 'patients/PATIENTS.html',{'all':all_Patients})


# def about_patient(request):
#     query = request.GET.get('q', '')
#     if query:
#         patients = Patient.objects.filter(patient_Name__icontains=query)
#     else:
#         patients = Patient.objects.all()

#     return render(request, 'patients/about_patient.html', {
#         'patients': patients,
#     })


def about_patient(request):
    query = request.GET.get('q')

    if query:
        # Filter patients by name
        patients = Patient.objects.filter(patient_Name__icontains=query)

        # Get all visits (appointments) for the filtered patients
        patient_ids = patients.annotate(patient_id_str=Cast('id', CharField())).values_list('patient_id_str', flat=True)
        
        # Fetch appointments for these patients
        visits = Appointment.objects.filter(Patient_ID__in=patient_ids)

        # Fetch related payments for these appointments
        payments = Payment.objects.filter(appointment__in=visits)

        # Combine visits with payment data
        visits_with_payment = []
        for visit in visits:
            payment = payments.filter(appointment=visit).first()  # Get payment for each appointment (if exists)
            visits_with_payment.append({
                'date': visit.Appointment_date,
                'doctor_name': visit.Doctor_name,
                'problem': visit.Problem,
                'payment_amount': payment.total_payable if payment else 'N/A',
                'invoice_url': f"/invoices/{visit.Token_Number}/"  # Example URL for invoice
            })
    else:
        patients = Patient.objects.none()  # Empty queryset
        visits_with_payment = []  # Empty list for visits

    context = {
        'patients': patients,
        'visits': visits_with_payment,
    }

    return render(request, 'patients/about_patient.html', context)




def about_doctor(request):
    query = request.GET.get('q')

    if query:
        # Filter doctors by name (use the correct field name: 'doctor_Name')
        doctors = Doctor.objects.filter(doctor_Name__icontains=query)

        # Get the doctor names for the filtered doctors
        doctor_names = doctors.values_list('doctor_Name', flat=True)

        # Fetch appointments for these doctor names
        visits = Appointment.objects.filter(Doctor_name__in=doctor_names)

        # Fetch related payments for these appointments
        payments = Payment.objects.filter(appointment__in=visits)

        # Combine visits with payment data
        visits_with_payment = []
        for visit in visits:
            payment = payments.filter(appointment=visit).first()  # Get payment for each appointment (if exists)
            visits_with_payment.append({
                'date': visit.Appointment_date,
                'patient_name': visit.Patient_ID,  # Assuming Patient_ID is what you want to show
                'problem': visit.Problem,
                'payment_amount': payment.total_payable if payment else 'N/A',
                'invoice_url': f"/invoices/{visit.Token_Number}/"  # Example URL for invoice
            })
    else:
        doctors = Doctor.objects.none()  # Empty queryset
        visits_with_payment = []  # Empty list for visits

    context = {
        'doctors': doctors,
        'visits': visits_with_payment,
    }

    return render(request, 'doctor/about_doc.html', context)


# def about_appointment(request, appointment_id):
#     # Fetch the appointment using the appointment_id from the URL
#     appointment = get_object_or_404(Appointment, id=appointment_id)

#     # Retrieve related doctor information
#     doctor = get_object_or_404(Doctor, id=appointment.Doctor_name.id)

#     context = {
#         'patient_id': appointment.Patient_ID,  # Assuming Patient_ID is a string
#         'department': appointment.Department,
#         'doctor_name': doctor.doctor_Name,  # Change according to your field
#         'appointment_date': appointment.Appointment_date.strftime('%d-%b-%Y'),  # Format date as needed
#         'time_slot': appointment.Time_slot,
#         'token_number': appointment.Token_Number,
#         'problem': appointment.Problem,
#     }

#     return render(request, 'appointments/appointment_details.html', context)




def Edit_patient(request):
    return render(request , 'patients/edit_patient.html')



def home(request):
    return render(request , 'home.html')



# def ADD_DOC(request):
#     return render(request , 'doctor/add_doc.html')

def DOCTORS(request):
    all_doctors = Doctor.objects.all
    return render(request , 'doctor/DOCTORS.html', {'all':all_doctors})

def About_doc(request):
    return render(request , 'doctor/about_doc.html')

def Edit_doc(request):
    return render(request , 'doctor/edit_doc.html')



# def ADD_APPOINTMENT(request):
#     return render(request , 'appointments/add_appointment.html')

def APPOINTMENTS(request):
    all_appointments = Appointment.objects.all()
    return render(request , 'appointments/all_appointments.html',{'all':all_appointments})

def About_Appointment(request):
    return render(request , 'appointments/appointment_details.html')

def Edit_Appointment(request):
    return render(request , 'appointments/edit_appointment.html')


# def ADD_Payment(request):
#     return render(request , 'Payment/add_payment.html')

def payments(request):
    payments_list = Payment.objects.all()

    return render(request, 'Payment/payments.html', {'payments': payments_list})

def Invoice_Payments(request):
    return render(request , 'Payment/pay_invoice.html')


# def ADD_Roomalt(request):
#     return render(request , 'Room_allotment/add_roomalt.html')

def Roomavl(request):
    all_rooms = RoomAllotment.objects.all()
    return render(request , 'Room_allotment/roomavl.html',{'all':all_rooms})

def Edit_Room(request):
    return render(request , 'Room_allotment/edit_roomalt.html')


# def home(request):
#     return render(request , 'home.html')

def patient_search(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.filter(patient_Name__icontains=query)
    return render(request, 'patient/patient_list.html', {
        'patients': patients,
    })

def patient_detail(request, patient_id):
    # Fetch the patient object based on the provided ID
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Fetch related data (appointments and payments) for this patient
    appointments = Appointment.objects.filter(Patient_ID=patient.id)
    payments = Payment.objects.filter(patient_id=patient.id)

    # Render the patient detail template with the patient data
    return render(request, 'patients/about_patient.html', {
        'patient': patient,
        'appointments': appointments,
        'payments': payments,
    })



def download_invoice(request, payment_id):
    # Logic to generate or retrieve the invoice for the given payment
    payment = get_object_or_404(Payment, id=payment_id)

    # Here, you would generate a PDF or retrieve the existing invoice file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{payment.id}.pdf"'

    # Generate the PDF (using a library like ReportLab, WeasyPrint, etc.)
    # For now, let's assume the invoice content is being written to the response.

    return response



def home(request):
    today = now().date()
    current_month = today.month
    previous_month = (today.replace(day=1) - timedelta(days=1)).month
    previous_month_year = (today.replace(day=1) - timedelta(days=1)).year

    # Fetch the latest 5 appointments
    all_appointments = Appointment.objects.all().order_by('-Appointment_date')[:5]
    
    # Fetch all doctors and their availability
    all_doctors = Doctor.objects.all()

    # Current and previous month patients
    total_patients_current = Patient.objects.filter(created_at__year=today.year, created_at__month=current_month).count()
    total_patients_previous = Patient.objects.filter(created_at__year=previous_month_year, created_at__month=previous_month).count()

    # Current and previous month appointments
    total_appointments_current = Appointment.objects.filter(Appointment_date__year=today.year, Appointment_date__month=current_month).count()
    total_appointments_previous = Appointment.objects.filter(Appointment_date__year=previous_month_year, Appointment_date__month=previous_month).count()

    # Current and previous month revenue
    total_revenue_current = Payment.objects.filter(discharge_date__year=today.year, discharge_date__month=current_month).aggregate(total=Sum('total_payable'))['total'] or 0
    total_revenue_previous = Payment.objects.filter(discharge_date__year=previous_month_year,discharge_date__month=previous_month).aggregate(total=Sum('total_payable'))['total'] or 0
    # Calculate percentage changes
    def calculate_percentage_change(current, previous):
        if previous == 0:
            return 0  # To avoid division by zero
        return ((current - previous) / previous) * 100

    patient_growth = calculate_percentage_change(total_patients_current, total_patients_previous)
    appointment_growth = calculate_percentage_change(total_appointments_current, total_appointments_previous)
    revenue_growth = calculate_percentage_change(total_revenue_current, total_revenue_previous)

    return render(request, 'home.html', {
        'all_appointments': all_appointments,
        'all_doctors': all_doctors,
        'total_patients': total_patients_current,
        'total_appointments': total_appointments_current,
        'total_revenue': total_revenue_current,
        'patient_growth': patient_growth,  # Pass dynamic growth values
        'appointment_growth': appointment_growth,
        'revenue_growth': revenue_growth,
    })



