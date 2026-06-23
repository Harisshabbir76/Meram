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
from .models import ServiceSection
from .forms import ServiceSectionForm
from .forms import ContactForm, BookingForm, CelebrationImageForm, GalleryImageForm, CorporateEventForm
from .models import ServiceHero, MainService, CorporateEvent
from .models import MainService, ServiceHero, OtherService
from .forms import MainServiceForm
from django.db.models import Q

def is_slot_available(date, start_time, end_time):
    return not BookingRequest.objects.filter(
        event_date=date
    ).filter(
        Q(start_time__lt=end_time) &
        Q(end_time__gt=start_time)
    ).exists()


def services(request):

    services = MainService.objects.all()

    celebration_images = GalleryImage.objects.filter(
        category='cts'
    )[:8]

    return render(
        request,
        'main/services.html',
        {
            'services': services,
            'celebration_images': celebration_images,
            'cms_page_name': 'services',
        }
    )


def corporate_events(request):

    celebration_images = GalleryImage.objects.filter(
        category='cts'
    )[:8]

    gallery = GalleryImage.objects.filter(
        category='corporate'
    )[:9]

    corporate = CorporateEvent.objects.all()
    print(corporate.count())

    return render(request, 'main/corporate_events.html', {
        'corporate': corporate,
        'gallery': gallery,
        'celebration_images': celebration_images,
        'cms_page_name': 'corporate_events',
    })
def other_services(request):
    celebration_images = GalleryImage.objects.filter(
        category='cts'
    )[:8]
    services = OtherService.objects.all().order_by('-created_at')

    return render(request, 'main/other_services.html', {
        'celebration_images': celebration_images,
        'services': services,
        'cms_page_name': 'other_services',
    })


def gallery(request):
    celebration_images = GalleryImage.objects.filter(
        category='cts'
    )[:8]

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
        'cms_page_name': 'gallery',
    })


from django.shortcuts import render, redirect
from django.contrib import messages

def book_now(request):
    celebration_images = GalleryImage.objects.filter(category='cts')[:8]

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)

            # ✅ CHECK SLOT FIRST
            if not is_slot_available(
                booking.event_date,
                booking.start_time,
                booking.end_time
            ):
                # ❌ DO NOT SAVE
                messages.error(
                    request,
                    "⚠️ This time slot is already booked. Please choose another time."
                )

                return render(request, 'main/book_now.html', {
                    'form': form,
                    'celebration_images': celebration_images
                })

            # ✅ ONLY SAVE IF AVAILABLE
            booking.save()

            messages.success(
                request,
                "Your booking request has been submitted!"
            )

            return redirect('book_now')

    else:
        form = BookingForm()

    return render(request, 'main/book_now.html', {
        'form': form,
        'celebration_images': celebration_images
    })

def home(request):
    celebration_images = GalleryImage.objects.filter(
        category='cts'
    )[:8]

    featured_gallery = GalleryImage.objects.filter(
        is_featured=True
    )[:6]

    testimonials = Testimonial.objects.filter(
        is_active=True
    )[:3]

    return render(request, 'main/home.html', {
        'celebration_images': celebration_images,
        'featured_gallery': featured_gallery,
        'testimonials': testimonials,
        'cms_page_name': 'home',
    })


def about(request):
    return render(request, 'main/about.html', {'cms_page_name': 'about'})

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
    if request.user.is_authenticated:
        return redirect('dashboard_bookings')

    error = None

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        from django.contrib.auth.models import User

        username = email

        user_obj = User.objects.filter(email__iexact=email).first()
        if user_obj:
            username = user_obj.username

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

        form = CelebrationImageForm(
            request.POST,
            request.FILES
        )

        print("POST DATA:", request.POST)
        print("FILES:", request.FILES)

        if form.is_valid():

            print("FORM VALID")
            form.save()

            return redirect('dashboard_celebration_images')

        else:
            print("FORM ERROR:", form.errors)

    else:
        form = CelebrationImageForm()

    return render(
        request,
        'dashboard/celebration_form.html',
        {'form': form}
    )

@login_required(login_url='dashboard_login')
def celebration_update(request, pk):

    image = get_object_or_404(
        CelebrationImage,
        pk=pk
    )

    if request.method == "POST":

        form = CelebrationImageForm(
            request.POST,
            request.FILES,
            instance=image
        )

        print("UPDATE POST:", request.POST)
        print("UPDATE FILES:", request.FILES)

        if form.is_valid():

            print("UPDATE VALID")

            form.save()

            return redirect(
                'dashboard_celebration_images'
            )

        else:
            print(
                "UPDATE ERROR:",
                form.errors
            )

    else:

        form = CelebrationImageForm(
            instance=image
        )


    return render(
        request,
        'dashboard/celebration_form.html',
        {
            'form': form,
            'object': image,
            'active_page': 'celebration'
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
@login_required
def dashboard_services(request):

    hero = ServiceHero.objects.first()
    services = MainService.objects.all()

    return render(
        request,
        "dashboard/services.html",
        {
            "hero": hero,
            "services": services,
            "form": MainServiceForm(),
            "active_page": "services"
        }
    )

@login_required(login_url='dashboard_login')
def dashboard_service_create(request):

    if request.method == "POST":

        form = MainServiceForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("dashboard_services")

    else:
        form = MainServiceForm()

    return render(
        request,
        "dashboard/service_form.html",
        {
            "form": form,
            "title": "Add Service"
        }
    )

@login_required(login_url='dashboard_login')
@login_required
def dashboard_service_update(request, pk):
    service = get_object_or_404(MainService, pk=pk)

    if request.method == "POST":
        form = MainServiceForm(request.POST, request.FILES, instance=service)

        # if form.is_valid():
        #     form.save()
        #     messages.success(request, "Updated successfully")
        #     return redirect("dashboard_services")
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully!")
            return redirect("dashboard_services")

        else:
            print(form.errors)   # 🔥 VERY IMPORTANT
            messages.error(request, form.errors)  # show real error

        messages.error(request, "Fix errors")

    return redirect("dashboard_services") 

@login_required(login_url='dashboard_login')
@require_POST
def dashboard_service_delete(request, pk):

    service = get_object_or_404(MainService, pk=pk)

    service.delete()

    return redirect("dashboard_services")

@login_required
def edit_service_hero(request):

    hero = ServiceHero.objects.first()

    if request.method == "POST":

        hero.eyebrow = request.POST.get("eyebrow")
        hero.title = request.POST.get("title")
        hero.subtitle = request.POST.get("subtitle")
        hero.script = request.POST.get("script")

        hero.save()

        messages.success(request, "Hero updated")
        return redirect("dashboard_services")

    return redirect("dashboard_services")

@login_required
def edit_service(request, pk):

    service = get_object_or_404(MainService, pk=pk)

    if request.method == "POST":

        service.card_title = request.POST.get("card_title")
        service.title = request.POST.get("title")
        service.tagline = request.POST.get("tagline")

        service.description = request.POST.get("description")

        service.bullet1 = request.POST.get("bullet1")
        service.bullet2 = request.POST.get("bullet2")
        service.bullet3 = request.POST.get("bullet3")
        service.bullet4 = request.POST.get("bullet4")
        service.bullet5 = request.POST.get("bullet5")

        service.quote = request.POST.get("quote")
        service.card_title_ar = request.POST.get("card_title_ar")

        service.title_ar = request.POST.get("title_ar")
        service.tagline_ar = request.POST.get("tagline_ar")

        service.description_ar = request.POST.get("description_ar")

        service.bullet1_ar = request.POST.get("bullet1_ar")
        service.bullet2_ar = request.POST.get("bullet2_ar")
        service.bullet3_ar = request.POST.get("bullet3_ar")
        service.bullet4_ar = request.POST.get("bullet4_ar")
        service.bullet5_ar = request.POST.get("bullet5_ar")

        service.quote_ar = request.POST.get("quote_ar")

        if request.FILES.get("card_image"):
            service.card_image = request.FILES["card_image"]

        if request.FILES.get("left_image"):
            service.left_image = request.FILES["left_image"]

        if request.FILES.get("right_image"):
            service.right_image = request.FILES["right_image"]

        service.save()

        messages.success(request, "Service updated")

    return redirect("dashboard_services")
def add_service(request):

    if request.method == "POST":

        form = MainServiceForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("dashboard_services")

    else:
        form = MainServiceForm()

    return render(
        request,
        "dashboard/service_form.html",
        {
            "form": form,
            "title": "Add Service"
        }
    )

@login_required
def corporate_event_list(request):
    events = CorporateEvent.objects.all()
    form = CorporateEventForm()

    return render(request, "dashboard/corporate_events.html", {
        "events": events,
        "form": form,
        "active_page": "corporate"
    })
@login_required
def corporate_event_create(request):

    if request.method == "POST":

        form = CorporateEventForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Event added successfully.")
        else:
            messages.error(request, "Fix errors.")

        return redirect("corporate_event_list")

    return redirect("corporate_event_list")

@login_required
def corporate_event_update(request, pk):

    event = get_object_or_404(CorporateEvent, pk=pk)

    if request.method == "POST":

        form = CorporateEventForm(
            request.POST,
            request.FILES,
            instance=event
        )

        if form.is_valid():
            obj = form.save(commit=False)

            if not request.FILES.get("main_image"):
                obj.main_image = event.main_image

            if not request.FILES.get("side_image"):
                obj.side_image = event.side_image

            obj.save()
        else:
            messages.error(request, "Fix errors.")

    return redirect("corporate_event_list")

@login_required
@require_POST
def corporate_event_delete(request, pk):

    event = get_object_or_404(CorporateEvent, pk=pk)

    event.delete()

    messages.success(request, "Deleted successfully.")

    return redirect("corporate_event_list")

@login_required(login_url='dashboard_login')
def other_services_dashboard(request):
    services = OtherService.objects.all()

    return render(request, 'dashboard/other_services.html', {
        'services': services,
    })
@login_required(login_url='dashboard_login')
def other_service_create(request):
    if request.method == "POST":
        OtherService.objects.create(
            title=request.POST['title'],
            title_ar=request.POST.get('title_ar', ''),
            description=request.POST['description'],
            description_ar=request.POST.get('description_ar', ''),
            image=request.FILES.get('image')
        )
    return redirect('other_services_dashboard')
@login_required(login_url='dashboard_login')
def other_service_update(request, id):
    service = get_object_or_404(OtherService, id=id)

    if request.method == "POST":
        service.title = request.POST['title']
        service.title_ar = request.POST.get('title_ar', '')
        service.description = request.POST['description']
        service.description_ar = request.POST.get('description_ar', '')

        if request.FILES.get('image'):
            service.image = request.FILES['image']

        service.save()

    return redirect('other_services_dashboard')

@login_required(login_url='dashboard_login')
@require_POST
def other_service_delete(request, id):
    service = get_object_or_404(OtherService, id=id)

    if request.method == "POST":
        service.delete()

    return redirect('other_services_dashboard')


def public_api_offdays(request):
    import json
    from django.http import JsonResponse
    from .models import OffDay

    if request.method == 'GET':
        year = request.GET.get('year')
        month = request.GET.get('month')
        if year and month:
            off_days = OffDay.objects.filter(date__year=year, date__month=month)
            data = []
            for od in off_days:
                data.append({
                    'date': od.date.strftime('%Y-%m-%d'),
                    'is_full_day': od.is_full_day,
                    'start_time': od.start_time,
                    'end_time': od.end_time
                })
            return JsonResponse({'status': 'ok', 'off_days': data})
        return JsonResponse({'status': 'error', 'message': 'Missing year/month'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


def public_api_check_conflict(request):
    from .models import OffDay, BookingRequest
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
    date_str = request.GET.get('date')
    start_str = request.GET.get('start_time')
    end_str = request.GET.get('end_time')
    if not (date_str and start_str and end_str):
        return JsonResponse({'status': 'error', 'message': 'Missing parameters'}, status=400)

    def ttm(t):
        try:
            parts = t.strip().split(' ')
            hm = parts[0].split(':')
            h, m = int(hm[0]), int(hm[1])
            ampm = parts[1].upper()
            if ampm == 'PM' and h != 12:
                h += 12
            if ampm == 'AM' and h == 12:
                h = 0
            return h * 60 + m
        except Exception:
            return 0

    sel_start = ttm(start_str)
    sel_end = ttm(end_str)

    try:
        from datetime import date as date_type
        check_date = date_type.fromisoformat(date_str)
        off_day = OffDay.objects.filter(date=check_date).first()
        if off_day:
            if off_day.is_full_day:
                return JsonResponse({'status': 'off_day', 'message': 'full_day', 'date': date_str})
            if sel_start < ttm(off_day.end_time) and sel_end > ttm(off_day.start_time):
                return JsonResponse({
                    'status': 'off_day', 'message': 'partial', 'date': date_str,
                    'off_start': off_day.start_time, 'off_end': off_day.end_time
                })
    except Exception:
        pass

    try:
        for booking in BookingRequest.objects.filter(
            event_date=date_str, status__in=['pending', 'confirmed']
        ):
            if sel_start < ttm(booking.end_time) and sel_end > ttm(booking.start_time):
                return JsonResponse({
                    'status': 'booking_conflict', 'date': date_str,
                    'booked_start': booking.start_time, 'booked_end': booking.end_time
                })
    except Exception:
        pass

    return JsonResponse({'status': 'ok'})
