# Generated by Django 5.1.1 on 2024-09-18 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_remove_visit_doctor_remove_visit_patient_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='advance_paid',
            new_name='total_payable',
        ),
    ]
