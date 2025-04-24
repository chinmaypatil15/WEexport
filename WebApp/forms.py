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
    # Honeypot field (matches your HTML)
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'display:none;',
            'id': 'id_phone_number'
        }),
        label='Phone Number'
    )
    
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'mobile', 'country', 'subject', 'category', 'message']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set up fields to match your HTML exactly
        self.fields['name'].widget.attrs.update({
            'id': 'name',
            'required': True,
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'id': 'email',
            'required': True,
            'class': 'form-control'
        })
        self.fields['mobile'].widget.attrs.update({
            'id': 'mobile',
            'type': 'tel',
            'pattern': '[0-9]{10}',
            'title': '10-digit number without spaces or dashes',
            'required': True,
            'class': 'form-control'
        })
        self.fields['country'].widget.attrs.update({
            'id': 'country',
            'class': 'form-control'
        })
        self.fields['subject'].widget.attrs.update({
            'id': 'subject',
            'class': 'form-control'
        })
        self.fields['category'].widget.attrs.update({
            'id': 'category',
            'class': 'form-control'
        })
        self.fields['message'].widget.attrs.update({
            'id': 'message',
            'rows': 5,
            'class': 'form-control'
        })
    
    def clean_phone_number(self):
        honeypot_value = self.cleaned_data.get('phone_number')
        if honeypot_value:
            raise forms.ValidationError("Invalid form submission")
        return honeypot_value
    
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile', '')
        if mobile and not mobile.isdigit():
            raise forms.ValidationError("Enter numbers only")
        if mobile and len(mobile) != 10:
            raise forms.ValidationError("Mobile number must be 10 digits")
        return mobile