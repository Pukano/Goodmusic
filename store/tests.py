from django.test import TestCase
from django.urls import reverse
from .models import Album, Artist, Contact, Note, Booking
# Create your tests here.

# Index page 
class IndexPageTestCase(TestCase):
    # test that index page returns a 200
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


# Detail Page  
class DetailPageTestCase(TestCase):

    def setUp(self):
        impossible = Album.objects.create(title="Transmission impossible")
        self.album = Album.objects.get(title="Transmission impossible")

    # test that detail page returns 200 if the item exists
    def test_detail_page_returns_200(self):
        album_id = self.album.id
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 200)

    # test that detail page returns 404 if the item does not exists 
    def test_detail_returns_404(self):
        album_id = self.album.id+1
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 404)

# Booking page 
class BookingPageTestCase(TestCase):

    def setUp(self):
        Contact.objects.create(name='Albert', email='albert@gmail.com')
        impossible = Album.objects.create(title="Transmission impossible")
        journey = Artist.objects.create(name="Journey")
        impossible.artist.add(journey)
        self.contact = Contact.objects.get(name="Albert")
        self.album = Album.objects.get(title="Transmission impossible")

    # test that a new booking is made 
    def test_new_booking_is_registered(self):
        old_bookings = Booking.objects.count()
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse("store:detail", args=(album_id,)), {
            'name': name,
            'email': email
        })
        new_bookings = Booking.objects.count()
        self.assertEqual(new_bookings, old_bookings + 1)

    # test that a booking belongs to a contact 
    def test_booking_belongs_contact(self):
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse('store:detail', args=(album_id,)), {
            'name' : name,
            'email' : email
        })
        booking = Booking.objects.first()
        self.assertEqual(self.contact, booking.contact)

    # test that a booking belongs to an album 
    def test_booking_belong_album(self):
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse("store:detail", args=(album_id,)), {
            'name':name,
            'email':email
        })
        booking = Booking.objects.first()
        self.assertEqual(self.album, booking.album)

    # test that an album is not available after a booking is made 
    def test_album_not_available_after_booking(self):
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse("store:detail", args=(album_id,)), {
            'name':name,
            'email':email
        })
        # Make query again otherwise available will still be set to True
        self.album.refresh_from_db()
        self.assertFalse(self.album.available)

