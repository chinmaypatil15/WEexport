from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import ContactSubmission

from django.contrib import admin
from .models import ContactSubmission

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'category', 'submitted_at', 'is_responded')
    list_filter = ('category', 'is_responded', 'submitted_at')
    search_fields = ('name', 'email', 'subject', 'message')
