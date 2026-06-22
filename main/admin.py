from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryImage, CelebrationImage, ContactSubmission, BookingRequest, FAQ, Testimonial
from .models import ServiceHero, MainService

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'order', 'image_preview']
    list_filter = ['category', 'is_featured']
    list_editable = ['order', 'is_featured']
    search_fields = ['title']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"


@admin.register(CelebrationImage)
class CelebrationImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'image_preview']
    list_editable = [ 'is_active']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'submitted_at', 'is_read']
    list_filter = ['is_read', 'submitted_at']
    search_fields = ['name', 'email', 'subject']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'submitted_at']

    def has_add_permission(self, request):
        return False


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'event_type', 'event_date', 'status', 'submitted_at']
    list_filter = ['status', 'event_type', 'event_date']
    search_fields = ['full_name', 'email', 'phone']
    list_editable = ['status']
    readonly_fields = ['full_name', 'email', 'phone', 'event_type', 'event_date',
                       'guest_count', 'venue', 'budget', 'details', 'submitted_at']
    fieldsets = (
        ('Client Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Event Details', {
            'fields': ('event_type', 'event_date', 'start_time', 'end_time', 'guest_count', 'venue', 'budget', 'details')
        }),
        ('Admin', {
            'fields': ('status', 'submitted_at')
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ('question', 'question_ar')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'event_type', 'rating', 'is_active', 'order']
    list_editable = ['is_active', 'order']


admin.site.site_header = "Meram Events Administration"
admin.site.site_title = "Meram Events Admin"
admin.site.index_title = "Welcome to Meram Events Dashboard"
admin.site.register(ServiceHero)
admin.site.register(MainService)