# Generated by Django 2.2.4 on 2019-08-19 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_premissas_clsse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='premissas',
            name='clsse',
        ),
        migrations.AddField(
            model_name='premissas',
            name='classe',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
