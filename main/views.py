from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import GalleryImage, CelebrationImage, FAQ, Testimonial
from .forms import ContactForm, BookingForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import BookingRequest, ContactSubmission
from django.utils import timezone
from datetime import timedelta
from .forms import ContactForm, BookingForm, CelebrationImageForm, GalleryImageForm
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
    celebration_images = CelebrationImage.objects.filter(is_active=True)[:8]
    return render(request, 'main/services.html', {
        'celebration_images': celebration_images
    })


def corporate_events(request):
    celebration_images = CelebrationImage.objects.filter(is_active=True)[:8]
    gallery = GalleryImage.objects.filter(category='corporate')[:9]
    return render(request, 'main/corporate_events.html', {'gallery': gallery, 'celebration_images': celebration_images,})


def other_services(request):
    celebration_images = CelebrationImage.objects.filter(is_active=True)[:8]
    return render(request, 'main/other_services.html', {
        'celebration_images': celebration_images,
    })


def gallery(request):
    celebration_images = CelebrationImage.objects.filter(is_active=True)[:8]

    top_images = GalleryImage.objects.filter(
        category='section1'
    ).order_by('order', '-created_at')

    main_images = GalleryImage.objects.filter(
        category='section2'
    ).order_by('order', '-created_at')

    return render(request, 'main/gallery.html', {
        'top_images': top_images,
        'main_images': main_images,
        'celebration_images': celebration_images,
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

# ======================================================================
# ADMIN DASHBOARD — custom login + dashboard (Philosophy-style design)
# ======================================================================

def dashboard_login(request):
    """Custom styled login page for the admin dashboard."""
    if request.user.is_authenticated:
        return redirect('dashboard_bookings')

    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        # Allow login via username OR email
        from django.contrib.auth.models import User
        username = email
        try:
            user_obj = User.objects.get(email__iexact=email)
            username = user_obj.username
        except User.DoesNotExist:
            pass

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            auth_login(request, user)
            return redirect('dashboard_bookings')
        else:
            error = 'Invalid email or password.'

    return render(request, 'dashboard/login.html', {'error': error})


def dashboard_logout(request):
    auth_logout(request)
    return redirect('dashboard_login')


@login_required(login_url='dashboard_login')
def dashboard_bookings(request):
    """Main bookings dashboard — filterable list with date range + quick filters."""
    bookings = BookingRequest.objects.all().order_by('-submitted_at')

    quick_filter = request.GET.get('quick', 'all')
    on_date = request.GET.get('on_date', '')
    date_from = request.GET.get('from', '')
    date_to = request.GET.get('to', '')

    today = timezone.localdate()

    if quick_filter == 'today':
        bookings = bookings.filter(event_date=today)
    elif quick_filter == 'yesterday':
        bookings = bookings.filter(event_date=today - timedelta(days=1))
    elif quick_filter == 'last3':
        bookings = bookings.filter(event_date__gte=today - timedelta(days=3), event_date__lte=today)

    if on_date:
        bookings = bookings.filter(event_date=on_date)
    if date_from:
        bookings = bookings.filter(event_date__gte=date_from)
    if date_to:
        bookings = bookings.filter(event_date__lte=date_to)

    context = {
        'bookings': bookings,
        'total': bookings.count(),
        'quick_filter': quick_filter,
        'on_date': on_date,
        'date_from': date_from,
        'date_to': date_to,
        'active_page': 'booking',
        'unread_contacts': ContactSubmission.objects.filter(is_read=False).count(),
    }
    return render(request, 'dashboard/bookings.html', context)


@login_required(login_url='dashboard_login')
def dashboard_booking_detail(request, pk):
    booking = get_object_or_404(BookingRequest, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        if status:
            booking.status = status
        booking.notes = notes
        booking.save()
        messages.success(request, 'Booking updated successfully.')
        return redirect('dashboard_booking_detail', pk=booking.pk)
    return render(request, 'dashboard/booking_detail.html', {
        'booking': booking,
        'active_page': 'booking',
    })


@login_required(login_url='dashboard_login')
@require_POST
def dashboard_booking_delete(request, pk):
    booking = get_object_or_404(BookingRequest, pk=pk)
    booking.delete()
    return JsonResponse({'success': True})


@login_required(login_url='dashboard_login')
def dashboard_contacts(request):
    """Contact-us submissions list."""
    contacts = ContactSubmission.objects.all().order_by('-submitted_at')
    context = {
        'contacts': contacts,
        'total': contacts.count(),
        'active_page': 'contacts',
        'unread_contacts': ContactSubmission.objects.filter(is_read=False).count(),
    }
    return render(request, 'dashboard/contacts.html', context)


@login_required(login_url='dashboard_login')
@require_POST
def dashboard_contact_delete(request, pk):
    contact = get_object_or_404(ContactSubmission, pk=pk)
    contact.delete()
    return JsonResponse({'success': True})


@login_required(login_url='dashboard_login')
def gallery_manage(request):

    images = GalleryImage.objects.all()

    q = request.GET.get('q')
    category = request.GET.get('category')

    if q:
        images = images.filter(title__icontains=q)

    if category:
        images = images.filter(category=category)

    context = {
        'images': images,
        'total': images.count(),
        'query': q or '',
        'selected_category': category or '',
        'categories': GalleryImage.CATEGORY_CHOICES,
        'active_page': 'gallery',
        'unread_contacts': ContactSubmission.objects.filter(is_read=False).count(),
    }

    return render(
        request,
        'dashboard/gallery_manage.html',
        context
    )
@login_required(login_url='dashboard_login')
def gallery_create(request):
    if request.method == "POST":
        form = GalleryImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('dashboard_gallery')

    else:
        form = GalleryImageForm()

    return render(
        request,
        "dashboard/gallery_form.html",
        {
            "form": form,
            "active_page": "gallery"
        }
    )
@login_required(login_url='dashboard_login')
def gallery_update(request, pk):

    image = get_object_or_404(GalleryImage, pk=pk)

    if request.method == "POST":
        form = GalleryImageForm(
            request.POST,
            request.FILES,
            instance=image
        )

        if form.is_valid():
            form.save()
            return redirect('dashboard_gallery')

    else:
        form = GalleryImageForm(instance=image)

    return render(
        request,
        "dashboard/gallery_form.html",
        {
            "form": form,
            "object": image,
            "active_page": "gallery"
        }
    )
@login_required(login_url='dashboard_login')
@require_POST
def gallery_delete(request, pk):

    image = get_object_or_404(
        GalleryImage,
        pk=pk
    )

    if image.image:
        image.image.delete(save=False)

    image.delete()

    return JsonResponse({
        'success': True
    })

def celebration_images(request):

    images = CelebrationImage.objects.all()

    q = request.GET.get("q")

    if q:
        images = images.filter(title__icontains=q)

    context = {
        "images": images,
        "total": images.count(),
        "query": q or "",
        'active_page': 'celebration',
    }

    return render(
        request,
        "dashboard/celebration_images.html",
        context
    )
@login_required(login_url='dashboard_login')
def celebration_create(request):
    if request.method == "POST":
        form = CelebrationImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('dashboard_celebration_images')
    else:
        form = CelebrationImageForm()

    return render(
        request,
        'dashboard/celebration_form.html',
        {'form': form}
    )
@login_required(login_url='dashboard_login')
def celebration_update(request, pk):
    image = get_object_or_404(CelebrationImage, pk=pk)

    if request.method == "POST":
        form = CelebrationImageForm(
            request.POST,
            request.FILES,
            instance=image
        )

        if form.is_valid():
            form.save()
            return redirect('dashboard_celebration_images')
    else:
        form = CelebrationImageForm(instance=image)

    return render(
        request,
        'dashboard/celebration_form.html',
        {
            'form': form,
            'object': image
        }
    )
@login_required(login_url='dashboard_login')
@require_POST
def celebration_delete(request, pk):
    image = get_object_or_404(CelebrationImage, pk=pk)

    if image.image:
        image.image.delete(save=False)

    image.delete()

    return JsonResponse({
        'success': True
    })

@login_required(login_url='dashboard_login')
def dashboard_faqs(request):

    faqs = FAQ.objects.all()

    return render(request,"dashboard/faq_list.html",{
        "faqs":faqs,
        "total":faqs.count(),
        "active_page":"faq",
        "unread_contacts":ContactSubmission.objects.filter(is_read=False).count(),
    })



@login_required(login_url='dashboard_login')
def dashboard_faq_create(request):

    if request.method=="POST":

        FAQ.objects.create(
            question=request.POST.get("question"),
            question_ar=request.POST.get("question_ar"),
            answer=request.POST.get("answer"),
            answer_ar=request.POST.get("answer_ar"),
            category=request.POST.get("category") or "general",
            order=request.POST.get("order",0),
            is_active=True if request.POST.get("is_active") else False
        )

        return redirect("dashboard_faqs")


    return render(request,"dashboard/faq_form.html",{
        "active_page":"faq"
    })



@login_required(login_url='dashboard_login')
def dashboard_faq_detail(request,pk):

    faq=get_object_or_404(FAQ,pk=pk)


    if request.method=="POST":

        faq.question=request.POST.get("question")
        faq.question_ar=request.POST.get("question_ar")
        faq.answer=request.POST.get("answer")
        faq.answer_ar=request.POST.get("answer_ar")
        faq.category = request.POST.get("category") or "general"
        faq.order=request.POST.get("order",0)
        faq.is_active=True if request.POST.get("is_active") else False

        faq.save()

        return redirect("dashboard_faqs")


    return render(request,"dashboard/faq_form.html",{
        "faq":faq,
        "active_page":"faq"
    })



@login_required(login_url='dashboard_login')
@require_POST
def dashboard_faq_delete(request,pk):

    faq=get_object_or_404(FAQ,pk=pk)

    faq.delete()

    return JsonResponse({
        "success":True
    })
