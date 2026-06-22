from django.db import models


class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('section1', '1st Section'),
        ('section2', '2nd Section'),
        ('cts', 'CTS Section'),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='section1'
    )
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class CelebrationImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='celebration/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ContactSubmission(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=300, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} - {self.submitted_at.strftime('%d %b %Y')}"


class BookingRequest(models.Model):

    EVENT_TYPES = [
        ('wedding', 'Wedding'),
        ('engagement', 'Engagement'),
        ('corporate', 'Corporate Event'),
        ('private', 'Private Celebration'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    TIME_SLOTS = [
    ('10:00', '10:00 AM'),
    ('12:00', '12:00 PM'),
    ('14:00', '02:00 PM'),
    ('16:00', '04:00 PM'),
    ('18:00', '06:00 PM'),
]

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)

    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_date = models.DateField()

    # 🔥 NEW FIELDS
    start_time = models.CharField(max_length=10, choices=TIME_SLOTS)
    end_time = models.CharField(max_length=10, choices=TIME_SLOTS)

    guest_count = models.CharField(max_length=100, blank=True)
    venue = models.CharField(max_length=300, blank=True)
    budget = models.CharField(max_length=100, blank=True)
    details = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.full_name} - {self.event_type} - {self.event_date}"


class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('wedding', 'Wedding'),
        ('corporate', 'Corporate'),
        ('booking', 'Booking'),
    ]

    question = models.CharField(max_length=500)
    question_ar = models.CharField(max_length=500, blank=True, null=True)

    answer = models.TextField()
    answer_ar = models.TextField(blank=True, null=True)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='general'
    )

    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question[:80]


class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=100)
    message = models.TextField()
    rating = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.client_name} - {self.event_type}"
    

class ServiceSection(models.Model):

    SERVICE_CHOICES = [
        ('wedding', 'Wedding & Event Planning'),
        ('floral', 'Floral & Decor Design'),
        ('vip', 'VIP Hospitality'),
    ]

    service_type = models.CharField(
        max_length=30,
        choices=SERVICE_CHOICES,
        unique=True
    )

    title_en = models.CharField(max_length=255)
    title_ar = models.CharField(max_length=255)

    tagline_en = models.CharField(max_length=255)
    tagline_ar = models.CharField(max_length=255)

    body_en = models.TextField()
    body_ar = models.TextField()

    subheading_en = models.CharField(max_length=255)
    subheading_ar = models.CharField(max_length=255)

    quote_en = models.TextField()
    quote_ar = models.TextField()

    image_left = models.ImageField(upload_to='services/')
    image_right = models.ImageField(upload_to='services/')

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title_en
    
class ServicePoint(models.Model):

    service = models.ForeignKey(
        ServiceSection,
        on_delete=models.CASCADE,
        related_name='points'
    )

    point_en = models.CharField(max_length=255)
    point_ar = models.CharField(max_length=255)

    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.point_en
    
class ServiceHero(models.Model):
    eyebrow = models.CharField(max_length=200)
    title = models.TextField()
    subtitle = models.CharField(max_length=300)
    script = models.CharField(max_length=300)

    def __str__(self):
        return "Services Hero"
    
class MainService(models.Model):

    # English
    card_title = models.CharField(max_length=255)

    title = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)

    description = models.TextField()

    bullet1 = models.CharField(max_length=255, blank=True)
    bullet2 = models.CharField(max_length=255, blank=True)
    bullet3 = models.CharField(max_length=255, blank=True)
    bullet4 = models.CharField(max_length=255, blank=True)
    bullet5 = models.CharField(max_length=255, blank=True)

    quote = models.TextField(blank=True)

    # Arabic
    card_title_ar = models.CharField(
        max_length=255,
        blank=True
    )

    title_ar = models.CharField(
        max_length=255,
        blank=True
    )

    tagline_ar = models.CharField(
        max_length=255,
        blank=True
    )

    description_ar = models.TextField(
        blank=True
    )

    bullet1_ar = models.CharField(max_length=255, blank=True)
    bullet2_ar = models.CharField(max_length=255, blank=True)
    bullet3_ar = models.CharField(max_length=255, blank=True)
    bullet4_ar = models.CharField(max_length=255, blank=True)
    bullet5_ar = models.CharField(max_length=255, blank=True)

    quote_ar = models.TextField(blank=True)

    # Images
    card_image = models.ImageField(
        upload_to='services/cards/'
    )

    left_image = models.ImageField(
        upload_to='services/details/'
    )

    right_image = models.ImageField(
        upload_to='services/details/'
    )

    def __str__(self):
        return self.title
    
class CorporateEvent(models.Model):

    # English
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField()

    paragraph1 = models.TextField(blank=True)
    paragraph2 = models.TextField(blank=True)
    paragraph3 = models.TextField(blank=True)

    # Arabic
    title_ar = models.CharField(max_length=255, blank=True)
    subtitle_ar = models.CharField(max_length=255, blank=True)
    description_ar = models.TextField(blank=True)

    paragraph1_ar = models.TextField(blank=True)
    paragraph2_ar = models.TextField(blank=True)
    paragraph3_ar = models.TextField(blank=True)

    # Images
    main_image = models.ImageField(upload_to="corporate/main/")
    side_image = models.ImageField(upload_to="corporate/side/", blank=True, null=True)

    def __str__(self):
        return self.title
    
class OtherService(models.Model):
    title = models.CharField(max_length=255)
    title_ar = models.CharField(max_length=255, blank=True)

    description = models.TextField()
    description_ar = models.TextField(blank=True)

    image = models.ImageField(upload_to='other_services/')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title