from django import forms
from .models import ContactSubmission, BookingRequest


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Full Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email Address', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone Number', 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'class': 'form-control', 'rows': 5}),
        }


class BookingForm(forms.ModelForm):

    class Meta:
        model = BookingRequest
        fields = '__all__'