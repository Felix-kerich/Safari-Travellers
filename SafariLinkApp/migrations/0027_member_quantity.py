# Generated by Django 4.2.6 on 2024-03-05 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SafariLinkApp', '0026_alter_notifications_busdestination_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]