# Meram Events - Full Django Website

## Project Structure
```
meram_events/
├── main/                    # Main app
│   ├── models.py            # Database models
│   ├── views.py             # Page views
│   ├── admin.py             # Admin panel config
│   ├── forms.py             # Contact & Booking forms
│   ├── urls.py              # URL routes
│   └── templates/main/      # HTML templates
│       ├── base.html        # Base layout (navbar + footer)
│       ├── home.html        # Homepage
│       ├── about.html       # About page
│       ├── services.html    # Services page
│       ├── corporate_events.html
│       ├── other_services.html
│       ├── gallery.html     # Gallery with lightbox + filter
│       ├── faq.html         # FAQ accordion
│       ├── contact.html     # Contact form
│       └── book_now.html    # Booking form
├── meram_events/            # Django project config
│   ├── settings.py
│   └── urls.py
├── db.sqlite3               # SQLite database
└── manage.py
```

## 9 Pages
1. **Home** - Hero, partners marquee, intro, crafting section, services, why choose, celebration gallery
2. **About** - Story, stats, values
3. **Services** - 4 services with full-width rows
4. **Corporate Events** - Corporate-focused page with features grid
5. **Other Services** - Floral, VIP, intimate gatherings
6. **Gallery** - Filterable, with lightbox viewer
7. **FAQ** - Accordion with 4 categories
8. **Contact** - Contact form + details
9. **Book Now** - Full booking form with steps

## Admin Panel Features
- **Gallery Images** - Upload, categorize, reorder, mark featured
- **Celebration Images** - Manage homepage "Create a Celebration" section images
- **Contact Submissions** - View all contact form entries, mark as read
- **Booking Requests** - View bookings, update status (pending/confirmed/cancelled/completed), add notes
- **FAQ** - Add/edit/reorder FAQ items by category
- **Testimonials** - Manage client testimonials

## Setup & Run
```bash
# Install dependencies
pip install django pillow

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver
```

## Access
- Website: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/
- Admin Login: admin / admin123

## Pages URLs
- / — Home
- /about/ — About
- /services/ — Services
- /services/corporate-events/ — Corporate Events
- /services/other-services/ — Other Services
- /gallery/ — Gallery
- /faq/ — FAQ
- /contact/ — Contact
- /book-now/ — Book Now

## Language Support
Footer has English/Arabic toggle. Add data-en="Text" attributes to elements for auto-translation.

## Design Colors
- Cream: #F5F0E8
- Dark: #1A1612
- Gold: #C9A96E
- Fonts: Cormorant Garamond (display) + Montserrat (body)
