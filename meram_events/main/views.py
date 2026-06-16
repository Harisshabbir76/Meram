from django.shortcuts import render, redirect
from django.contrib import messages
from .models import GalleryImage, CelebrationImage, FAQ, Testimonial
from .forms import ContactForm, BookingForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import BookingRequest


def is_slot_available(date, start_time, end_time):
    return not BookingRequest.objects.filter(
        event_date=date,
        status='confirmed'
    ).filter(
        Q(start_time__lt=end_time) &
        Q(end_time__gt=start_time)
    ).exists()


def book_now(request):

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            # 🔥 SLOT CHECK HERE
            if not is_slot_available(
                booking.event_date,
                booking.start_time,
                booking.end_time
            ):
                messages.error(request, "This time slot is already booked. Please choose another time.")
                return render(request, 'main/book_now.html', {'form': form})

            # save if available
            booking.save()

            messages.success(request, 'Your booking request has been submitted! We will contact you within 24 hours.')
            return redirect('book_now')

    else:
        form = BookingForm()

    return render(request, 'main/book_now.html', {'form': form})

def home(request):
    celebration_images = CelebrationImage.objects.filter(is_active=True)[:8]
    featured_gallery = GalleryImage.objects.filter(is_featured=True)[:6]
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    return render(request, 'main/home.html', {
        'celebration_images': celebration_images,
        'featured_gallery': featured_gallery,
        'testimonials': testimonials,
    })


def about(request):
    return render(request, 'main/about.html')


def services(request):
    return render(request, 'main/services.html')


def corporate_events(request):
    gallery = GalleryImage.objects.filter(category='corporate')[:9]
    return render(request, 'main/corporate_events.html', {'gallery': gallery})


def other_services(request):
    return render(request, 'main/other_services.html')


def gallery(request):
    category = request.GET.get('category', 'all')
    if category == 'all':
        images = GalleryImage.objects.all()
    else:
        images = GalleryImage.objects.filter(category=category)
    categories = GalleryImage.CATEGORY_CHOICES
    return render(request, 'main/gallery.html', {
        'images': images,
        'categories': categories,
        'active_category': category,
    })


def faq(request):
    faqs = FAQ.objects.filter(is_active=True)
    general = faqs.filter(category='general')
    wedding = faqs.filter(category='wedding')
    corporate = faqs.filter(category='corporate')
    booking = faqs.filter(category='booking')
    return render(request, 'main/faq.html', {
        'general': general,
        'wedding': wedding,
        'corporate': corporate,
        'booking': booking,
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})

