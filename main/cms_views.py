"""
Visual "Home" page editor — backend.

  home_editor       renders the real home page in edit mode (login required)
  cms_data          GET  json of all overrides for a page (used by the live site)
  cms_save          POST upsert text + style overrides
  cms_image_upload  POST replace an element's image
  cms_reset         POST delete one override (revert to original)
"""

import json

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import PageContent, GalleryImage, Testimonial, MainService, CorporateEvent, OtherService


def _home_context():
    """Same data the public home view passes, so the editor is pixel-identical."""
    return {
        'celebration_images': GalleryImage.objects.filter(category='cts')[:8],
        'featured_gallery': GalleryImage.objects.filter(is_featured=True)[:6],
        'testimonials': Testimonial.objects.filter(is_active=True)[:3],
    }


def _serialize(page):
    data = {}
    for block in PageContent.objects.filter(page=page):
        data[block.element_key] = {
            'content_en': block.content_en,
            'content_ar': block.content_ar,
            'styles': block.styles or {},
            'styles_en': block.styles_en or {},
            'styles_ar': block.styles_ar or {},
            'image': block.image.url if block.image else None,
            'hero_media': block.hero_media.url if block.hero_media else None,
            'hero_type': block.hero_type or '',
        }
    return data


def _merge_styles(existing, incoming):
    """Merge a style dict; empty/None values delete the property."""
    merged = dict(existing or {})
    for k, v in (incoming or {}).items():
        if v in (None, ''):
            merged.pop(k, None)
        else:
            merged[k] = v
    return merged


@login_required(login_url='dashboard_login')
def home_editor(request):
    ctx = _home_context()
    ctx.update({
        'cms_edit': True,
        'cms_page_name': 'home',
        'active_page': 'home_editor',
    })
    return render(request, 'main/home.html', ctx)


@login_required(login_url='dashboard_login')
def about_editor(request):
    return render(request, 'main/about.html', {
        'cms_edit': True,
        'cms_page_name': 'about',
        'active_page': 'about_editor',
    })


@login_required(login_url='dashboard_login')
def services_editor(request):
    return render(request, 'main/services.html', {
        'services': MainService.objects.all(),
        'celebration_images': GalleryImage.objects.filter(category='cts')[:8],
        'cms_edit': True,
        'cms_page_name': 'services',
        'active_page': 'services_editor',
    })


@login_required(login_url='dashboard_login')
def corporate_services_editor(request):
    return render(request, 'main/corporate_events.html', {
        'corporate': CorporateEvent.objects.all(),
        'gallery': GalleryImage.objects.filter(category='corporate')[:9],
        'celebration_images': GalleryImage.objects.filter(category='cts')[:8],
        'cms_edit': True,
        'cms_page_name': 'corporate_events',
        'active_page': 'corporate_services_editor',
    })


@login_required(login_url='dashboard_login')
def other_services_editor(request):
    return render(request, 'main/other_services.html', {
        'services': OtherService.objects.all().order_by('-created_at'),
        'celebration_images': GalleryImage.objects.filter(category='cts')[:8],
        'cms_edit': True,
        'cms_page_name': 'other_services',
        'active_page': 'other_services_editor',
    })


@login_required(login_url='dashboard_login')
def gallery_editor(request):
    return render(request, 'main/gallery.html', {
        'celebration_images': GalleryImage.objects.filter(category='cts')[:8],
        'top_images': GalleryImage.objects.filter(category='section1').order_by('order', '-created_at'),
        'main_images': GalleryImage.objects.filter(category='section2').order_by('order', '-created_at'),
        'cms_edit': True,
        'cms_page_name': 'gallery',
        'active_page': 'gallery_editor',
    })


def cms_data(request, page):
    """Public — returns saved overrides so the live page can apply them."""
    return JsonResponse({'page': page, 'blocks': _serialize(page)})


@login_required(login_url='dashboard_login')
@require_POST
def cms_save(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return HttpResponseBadRequest('Invalid JSON')

    page = payload.get('page')
    changes = payload.get('changes') or {}
    if not page:
        return HttpResponseBadRequest('Missing page')

    saved = 0
    for element_key, fields in changes.items():
        if not element_key:
            continue
        block, _ = PageContent.objects.get_or_create(page=page, element_key=element_key)
        if 'content_en' in fields:
            block.content_en = fields['content_en']
        if 'content_ar' in fields:
            block.content_ar = fields['content_ar']
        if isinstance(fields.get('styles'), dict):
            block.styles = _merge_styles(block.styles, fields['styles'])
        if isinstance(fields.get('styles_en'), dict):
            block.styles_en = _merge_styles(block.styles_en, fields['styles_en'])
        if isinstance(fields.get('styles_ar'), dict):
            block.styles_ar = _merge_styles(block.styles_ar, fields['styles_ar'])
        block.save()
        saved += 1

    return JsonResponse({'ok': True, 'saved': saved})


@login_required(login_url='dashboard_login')
@require_POST
def cms_image_upload(request):
    page = request.POST.get('page')
    element_key = request.POST.get('element_key')
    image = request.FILES.get('image')
    if not (page and element_key and image):
        return HttpResponseBadRequest('Missing page, element_key or image')

    block, _ = PageContent.objects.get_or_create(page=page, element_key=element_key)
    block.image = image
    block.save()  # auto-converts to webp via model.save()
    return JsonResponse({'ok': True, 'url': block.image.url})


@login_required(login_url='dashboard_login')
@require_POST
def cms_bg_upload(request):
    """Upload a hero background — an image (converted to WebP) or a video."""
    page = request.POST.get('page')
    element_key = request.POST.get('element_key')
    media_type = request.POST.get('media_type')
    f = request.FILES.get('file')
    if not (page and element_key and media_type in ('image', 'video') and f):
        return HttpResponseBadRequest('Missing page, element_key, media_type or file')

    block, _ = PageContent.objects.get_or_create(page=page, element_key=element_key)

    if media_type == 'image':
        import os
        from .image_utils import encode_webp_bytes
        data = encode_webp_bytes(f)
        new_name = os.path.splitext(f.name)[0] + '.webp'
        block.hero_media.save(new_name, ContentFile(data), save=False)
    else:
        from .video_utils import VideoCompressionError, compressed_hero_video
        try:
            new_name, data = compressed_hero_video(f)
        except VideoCompressionError as exc:
            return JsonResponse({'ok': False, 'error': str(exc)}, status=400)
        block.hero_media.save(new_name, data, save=False)

    block.hero_type = media_type
    block.save()
    return JsonResponse({'ok': True, 'url': block.hero_media.url, 'type': media_type})


@login_required(login_url='dashboard_login')
@require_POST
def cms_gallery_image(request):
    """Replace a shared GalleryImage's file — updates it on EVERY page at once."""
    gallery_id = request.POST.get('gallery_id')
    image = request.FILES.get('image')
    if not (gallery_id and image):
        return HttpResponseBadRequest('Missing gallery_id or image')
    try:
        obj = GalleryImage.objects.get(pk=gallery_id)
    except GalleryImage.DoesNotExist:
        return HttpResponseBadRequest('No such gallery image')
    obj.image = image
    obj.save()  # auto-converts to WebP via model.save()
    return JsonResponse({'ok': True, 'url': obj.image.url})


@login_required(login_url='dashboard_login')
@require_POST
def cms_reset(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return HttpResponseBadRequest('Invalid JSON')
    page = payload.get('page')
    element_key = payload.get('element_key')
    PageContent.objects.filter(page=page, element_key=element_key).delete()
    return JsonResponse({'status': 'ok'})


@login_required(login_url='dashboard_login')
def calendar_dashboard(request):
    return render(request, 'dashboard/calendar.html', {
        'active_page': 'calendar'
    })


@login_required(login_url='dashboard_login')
def dashboard_api_offdays(request):
    import json
    from datetime import datetime
    from .models import OffDay

    if request.method == 'GET':
        year = request.GET.get('year')
        month = request.GET.get('month')
        if year and month:
            off_days = OffDay.objects.filter(date__year=year, date__month=month)
            data = []
            for od in off_days:
                data.append({
                    'id': od.id,
                    'date': od.date.strftime('%Y-%m-%d'),
                    'is_full_day': od.is_full_day,
                    'start_time': od.start_time,
                    'end_time': od.end_time
                })
            return JsonResponse({'status': 'ok', 'off_days': data})
        return JsonResponse({'status': 'error', 'message': 'Missing year/month'}, status=400)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            date_str = data.get('date')
            is_full_day = data.get('is_full_day', False)
            start_time = data.get('start_time')
            end_time = data.get('end_time')

            if not date_str:
                return JsonResponse({'status': 'error', 'message': 'Date is required'}, status=400)

            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

            # Create or update the off day
            od, created = OffDay.objects.get_or_create(date=date_obj)
            od.is_full_day = is_full_day
            od.start_time = start_time if not is_full_day else None
            od.end_time = end_time if not is_full_day else None
            od.save()

            return JsonResponse({
                'status': 'ok',
                'off_day': {
                    'id': od.id,
                    'date': od.date.strftime('%Y-%m-%d'),
                    'is_full_day': od.is_full_day,
                    'start_time': od.start_time,
                    'end_time': od.end_time
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            date_str = data.get('date')
            if date_str:
                OffDay.objects.filter(date=date_str).delete()
                return JsonResponse({'status': 'ok'})
            return JsonResponse({'status': 'error', 'message': 'Date is required'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
