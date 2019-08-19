# Generated by Django 2.2.4 on 2019-08-19 10:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_erro'),
    ]

    operations = [
        migrations.CreateModel(
            name='CLASSE',
            fields=[
                ('cla_codigo', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cla_prof', models.CharField(max_length=100)),
            ],
        ),
    ]
