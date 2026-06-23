from django.urls import path
from . import views
from . import cms_views

urlpatterns = [
    # ===== VISUAL PAGE EDITORS (CMS) =====
    path('dashboard/home-editor/', cms_views.home_editor, name='dashboard_home_editor'),
    path('dashboard/about-editor/', cms_views.about_editor, name='dashboard_about_editor'),
    path('dashboard/services-editor/', cms_views.services_editor, name='dashboard_services_editor'),
    path('dashboard/corporate-services-editor/', cms_views.corporate_services_editor, name='dashboard_corporate_services_editor'),
    path('dashboard/other-services-editor/', cms_views.other_services_editor, name='dashboard_other_services_editor'),
    path('dashboard/gallery-editor/', cms_views.gallery_editor, name='dashboard_gallery_editor'),
    path('cms/data/<str:page>/', cms_views.cms_data, name='cms_data'),
    path('cms/save/', cms_views.cms_save, name='cms_save'),
    path('cms/image/', cms_views.cms_image_upload, name='cms_image_upload'),
    path('cms/bg/', cms_views.cms_bg_upload, name='cms_bg_upload'),
    path('cms/gallery-image/', cms_views.cms_gallery_image, name='cms_gallery_image'),
    path('cms/reset/', cms_views.cms_reset, name='cms_reset'),

    # ===== PUBLIC APIS =====
    path('api/offdays/', views.public_api_offdays, name='public_api_offdays'),
    path('api/check-conflict/', views.public_api_check_conflict, name='public_api_check_conflict'),

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/corporate-events/', views.corporate_events, name='corporate_events'),
    path('services/other-services/', views.other_services, name='other_services'),
    path('gallery/', views.gallery, name='gallery'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('book-now/', views.book_now, name='book_now'),
      # ===== ADMIN DASHBOARD =====
    path('dashboard/login/', views.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),
    path('admin/', views.dashboard_bookings, name='dashboard_bookings'),
    path('dashboard/bookings/<int:pk>/', views.dashboard_booking_detail, name='dashboard_booking_detail'),
    path('dashboard/bookings/<int:pk>/delete/', views.dashboard_booking_delete, name='dashboard_booking_delete'),
    path('dashboard/contacts/', views.dashboard_contacts, name='dashboard_contacts'),
    path('dashboard/contacts/<int:pk>/delete/', views.dashboard_contact_delete, name='dashboard_contact_delete'),
    
    # ===== DASHBOARD CALENDAR =====
    path('dashboard/calendar/', cms_views.calendar_dashboard, name='dashboard_calendar'),
    path('dashboard/api/offdays/', cms_views.dashboard_api_offdays, name='dashboard_api_offdays'),

path(
    'dashboard/celebration-images/',
    views.celebration_images,
    name='dashboard_celebration_images'
),

path(
    'dashboard/celebration-images/add/',
    views.celebration_create,
    name='dashboard_celebration_create'
),

path(
    'dashboard/celebration-images/<int:pk>/edit/',
    views.celebration_update,
    name='dashboard_celebration_update'
),

path(
    'dashboard/celebration-images/<int:pk>/delete/',
    views.celebration_delete,
    name='dashboard_celebration_delete'
),
path(
    'dashboard/gallery/',
    views.gallery_manage,
    name='dashboard_gallery'
),

path(
    'dashboard/gallery/add/',
    views.gallery_create,
    name='dashboard_gallery_create'
),

path(
    'dashboard/gallery/<int:pk>/edit/',
    views.gallery_update,
    name='dashboard_gallery_update'
),

path(
    'dashboard/gallery/<int:pk>/delete/',
    views.gallery_delete,
    name='dashboard_gallery_delete'
),
# ===== FAQ DASHBOARD =====

path(
    'dashboard/faqs/',
    views.dashboard_faqs,
    name='dashboard_faqs'
),

path(
    'dashboard/faqs/add/',
    views.dashboard_faq_create,
    name='dashboard_faq_create'
),

path(
    'dashboard/faqs/<int:pk>/',
    views.dashboard_faq_detail,
    name='dashboard_faq_detail'
),

path(
    'dashboard/faqs/<int:pk>/delete/',
    views.dashboard_faq_delete,
    name='dashboard_faq_delete'
),


path(
    "dashboard/services/hero/edit/",
    views.edit_service_hero,
    name="edit_service_hero"
),

path('dashboard/services/', views.dashboard_services, name='dashboard_services'),
path(
    'dashboard/services/add/',
    views.dashboard_service_create,
    name='dashboard_service_create'
),

path(
    'dashboard/services/<int:pk>/edit/',
    views.dashboard_service_update,
    name='dashboard_service_update'
),

path(
    'dashboard/services/<int:pk>/delete/',
    views.dashboard_service_delete,
    name='dashboard_service_delete'
),

    path(
        "dashboard/corporate-events/",
        views.corporate_event_list,
        name="corporate_event_list",
    ),

    path(
        "dashboard/corporate-events/create/",
        views.corporate_event_create,
        name="corporate_event_create",
    ),

    path(
        "dashboard/corporate-events/<int:pk>/edit/",
        views.corporate_event_update,
        name="corporate_event_update",
    ),

    path(
        "dashboard/corporate-events/<int:pk>/delete/",
        views.corporate_event_delete,
        name="corporate_event_delete",
    ),
# ===== OTHER SERVICES DASHBOARD =====

path(
    "dashboard/other-services/",
    views.other_services_dashboard,
    name="other_services_dashboard"
),

path(
    "dashboard/other-services/add/",
    views.other_service_create,
    name="other_service_create"
),

path(
    "dashboard/other-services/<int:id>/edit/",
    views.other_service_update,
    name="other_service_update"
),

path(
    "dashboard/other-services/<int:id>/delete/",
    views.other_service_delete,
    name="other_service_delete"
),

]
