# Generated by Django 5.0.1 on 2024-01-31 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SafariLinkApp', '0008_member_groups_member_is_active_member_is_staff_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='member',
            name='is_staff',
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
