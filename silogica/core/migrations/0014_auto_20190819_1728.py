# Generated by Django 2.2.4 on 2019-08-19 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_e_classe_e_pro'),
    ]

    operations = [
        migrations.RenameField(
            model_name='e_classe',
            old_name='e_pro',
            new_name='e_prof',
        ),
    ]
