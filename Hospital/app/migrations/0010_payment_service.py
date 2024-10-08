# Generated by Django 5.1.1 on 2024-09-15 15:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_appointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(max_length=100)),
                ('patient_name', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('doctor_name', models.CharField(max_length=100)),
                ('admission_date', models.DateField()),
                ('discharge_date', models.DateField()),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('advance_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_type', models.CharField(max_length=50)),
                ('card_check_no', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=255)),
                ('treatment_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='app.payment')),
            ],
        ),
    ]
