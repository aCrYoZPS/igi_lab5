# Generated by Django 5.2 on 2025-05-01 13:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning_service', '0007_alter_faq_answer_date_alter_vacancy_job_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='history',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='faq',
            name='answer_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 1, 16, 55, 55, 514232)),
        ),
    ]
