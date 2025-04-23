# # forms.py
# from django import forms
# from .models import ContactSubmission

# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = ContactSubmission
#         fields = ['name', 'email', 'subject', 'category', 'message']
#         widgets = {
#             'message': forms.Textarea(attrs={'rows': 5}),
#         }
        
# forms.py
from django import forms
from .models import ContactSubmission

class ContactForm(forms.ModelForm):
    # Add honeypot field (not in model)
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'style': 'display:none;'}),
        label='Leave this field empty'
    )
    
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'category', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
    
    def clean_phone_number(self):
        """Honeypot validation - if field has value, it's likely a bot"""
        honeypot_value = self.cleaned_data.get('phone_number', '')
        if honeypot_value:
            raise forms.ValidationError("This form was submitted by a bot.")
        return honeypot_value
    
    def clean(self):
        """Main clean method that calls all other clean methods"""
        cleaned_data = super().clean()
        # Any additional validation can go here
        return cleaned_data