from django.db import models


class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('section1', '1st Section'),
        ('section2', '2nd Section'),
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
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

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
