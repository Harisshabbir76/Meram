from django import forms
from .models import ContactSubmission, BookingRequest, CelebrationImage, GalleryImage, CorporateEvent
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

from .models import ServiceSection

from .models import ServiceHero, MainService


class ServiceHeroForm(forms.ModelForm):
    class Meta:
        model = ServiceHero
        fields = '__all__'


class MainServiceForm(forms.ModelForm):
    class Meta:
        model = MainService
        fields = '__all__'
class CorporateEventForm(forms.ModelForm):
    class Meta:
        model = CorporateEvent
        fields = '__all__'
class ServiceSectionForm(forms.ModelForm):
    class Meta:
        model = ServiceSection
        fields = '__all__'

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = [
            'title',
            'image',
            'is_featured',
            'category',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'db-input',
                'placeholder': 'Image title'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'db-checkbox'
            }),
        }

class CelebrationImageForm(forms.ModelForm):
    class Meta:
        model = CelebrationImage
        fields = [
            'title',
            'image',
            'is_active',
        ]
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
        exclude = ['status']

        widgets = {

            'event_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'start_time': forms.Select(),
            'end_time': forms.Select(),
        }