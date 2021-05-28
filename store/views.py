from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError

from .models import Album, Artist, Contact, Booking
from .forms import ContactForm, ParagraphErrorList



# Create your views here.

def index(request):
    albums = Album.objects.filter(available=True).order_by("-created_at")[:12]
    context = {'albums': albums}
    return render(request, 'store/index.html', context)

def listing(request):
    albums_list = Album.objects.filter(available=True)
    paginator = Paginator(albums_list, 3)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        # If page isn't an integer, deliver first page
        albums = paginator.page(1)
         
    except EmptyPage:
        # If page is out of range, deliver last page
        albums = paginator.page(paginator.num_pages)

    context = {'albums': albums, 'paginate': True}
    return render(request, 'store/listing.html', context)

@transaction.atomic
def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    artist_name = " ".join([artist.name for artist in album.artist.all()])
    context = {
        'album_title': album.title,
        'artist_name': artist_name,
        'album_id': album.id,
        'thumbnail': album.picture
    }
    if request.method == 'POST':
        form = ContactForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            try:
                with transaction.atomic():
                    contact = Contact.objects.filter(email=email)
                    if not contact.exists():
                        # If a contact is not registered, create a new one.
                        contact = Contact.objects.create(
                            email=email,
                            name=name
                        )
                    else:
                        contact = contact.first()
                    album = get_object_or_404(Album, id=album_id)
                    booking = Booking.objects.create(
                        contact=contact,
                        album=album
                    )
                    album.available = False
                    album.save()
                    context = {
                        'album_title': album.title
                    }
                    return render(request, 'store/merci.html', context)
            except IntegrityError:
                form.errors['internal'] = "L'album demandé est déja commandé par un autre client. Essayer un autre album. "
    else:
        form = ContactForm()

    context['form'] = form
    context['errors'] = form.errors.items()
    return render(request, 'store/detail.html', context)

def search(request):
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)

    if not albums.exists():
        albums = Album.objects.filter(artist__name__icontains=query)
    
    title = "Résultats pour la requête %s"%query 
    context = {
        'albums': albums,
        'title': title
    }

    return render(request, 'store/search.html', context)