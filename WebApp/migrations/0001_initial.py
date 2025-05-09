# Generated by Django 5.1.6 on 2025-04-23 18:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=15)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('subject', models.CharField(blank=True, max_length=200)),
                ('message', models.TextField()),
                ('category', models.CharField(choices=[('general', 'General Inquiry'), ('support', 'Technical Support'), ('feedback', 'Feedback'), ('sales', 'Sales Question'), ('other', 'Other')], default='general', max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('is_responded', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('sent', 'Sent'), ('failed', 'Failed')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('error_message', models.TextField(blank=True)),
                ('related_submission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='WebApp.contactsubmission')),
            ],
        ),
    ]
