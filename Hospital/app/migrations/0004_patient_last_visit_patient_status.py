from django.db import migrations, models
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_patient_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='last_visit',
            field=models.DateTimeField(default=timezone.now, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='status',
            field=models.CharField(max_length=50, default='unknown'),
        ),
    ]
