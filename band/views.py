from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from band.models import Musician,UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Musician, Band, Venue
from band.forms import VenueForm
from django.http import Http404


def viewAllBands(request):
    musicians_list = Musician.objects.all()
    paginator = Paginator(musicians_list, 10) 

    page_number = request.GET.get('page')
    try:
        musicians = paginator.page(page_number)
    except PageNotAnInteger:
        musicians = paginator.page(1)
    except EmptyPage:
        musicians = paginator.page(paginator.num_pages)

    context = {'musicians': musicians}
    return render(request, 'all_bands.html', context)

def viewMusicianDetails(request, id):

    musician = get_object_or_404(Musician, id=id)
    context = {
        'musician': musician
    }
    return render(request, 'musician_detail.html', context)

def musician_list(request):
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
        per_page = min(max(1, per_page), 50)  # Constrain between 1-50
    except ValueError:
        per_page = 10

    musicians_list = Musician.objects.all()
    paginator = Paginator(musicians_list, per_page)
    
    page_number = request.GET.get('page')
    try:
        musicians = paginator.page(page_number)
    except PageNotAnInteger:
        musicians = paginator.page(1)
    except EmptyPage:
        musicians = paginator.page(paginator.num_pages)

    context = {
        'musicians': musicians,
        'per_page': per_page,
    }
    return render(request, 'musician_list.html', context)

def band_list(request):
    # Handle per_page parameter
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
        per_page = min(max(1, per_page), 50)
    except ValueError:
        per_page = 10

    bands_list = Band.objects.all()
    paginator = Paginator(bands_list, per_page)
    
    page_number = request.GET.get('page')
    try:
        bands = paginator.page(page_number)
    except PageNotAnInteger:
        bands = paginator.page(1)
    except EmptyPage:
        bands = paginator.page(paginator.num_pages)

    context = {
        'bands': bands,
        'per_page': per_page,
    }
    return render(request, 'band_list.html', context)

def band_detail(request, id):
    band = get_object_or_404(Band, id=id)
    return render(request, 'band_detail.html', {'band': band})

def venue_list(request):
    venues = Venue.objects.prefetch_related('room_set').all()
    return render(request, 'venue_list.html', {'venues': venues})

@login_required
def restricted_page(request):
    data={
        'title': 'Restricted Page',
        'content': "This is a restricted page. You must be logged in to view this page."
    }
    return render(request, 'general.html', data)


@login_required
def musician_restricted(request, musician_id):
    musician = get_object_or_404(Musician, id=musician_id)
    profile = getattr(request.user, 'userprofile', None)
    if not profile:
     return render(request, "profile/profile_not_found.html")
    allowed = False

    if profile.musician_profiles.filter(id=musician.id).exists():
        allowed = True
    else:
        musician_profiles = set(profile.musician_profiles.all())
        for band in musician.band_set.all():
            band_musicians = set(band.musicians.all())
            if musician_profiles.intersection(band_musicians):
                allowed = True
                break

    if allowed:
        return render(request, "musician_restricted.html", {"musician": musician})
    else:
        return render(request, "profile/profile_not_found.html")
    

@receiver(post_save, sender=User)
def create_user_profile(sender,**kwargs):
    if kwargs['created'] and not kwargs['raw']:
        user = kwargs['instance']
        try:
            UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=user)


@login_required
def edit_venue(request, venue_id=0):
    # print(f"Controlled venues: {profile.venues_controlled.all()}")

    if venue_id != 0:
        venue = get_object_or_404(Venue, id=venue_id)
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if not profile.venue_controlled.filter(id=venue_id).exists():
            raise Http404("Can only edit controlled venues")

    if request.method == "GET":
        if venue_id == 0:
            form = VenueForm()
        else:
            form = VenueForm(instance=venue)
    else:
        if venue_id ==0:
            venue = Venue.objects.create()
        
        form = VenueForm(request.POST, request.FILES, instance=venue)

        if form.is_valid():
            venue = form.save()

            profile.venue_controlled.add(venue)
            return redirect("venues")
        
    data = {
        'form': form,
    }

    return render(request, 'edit_venue.html')


def _get_items_per_page(request):
    try:
        items_per_page = int(request.GET.get("items_per_page", 10))
    except ValueError:
        items_per_page = 10

    if items_per_page < 1:
        items_per_page = 10
    elif items_per_page > 50:
        items_per_page = 50
    return items_per_page

def _get_page_num(request, paginator):
    try:
        page_num = int(request.GET.get("page", 1))
    except ValueError:
        page_num = 1

    if page_num < 1:
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages
    return page_num

def venues(request):
    all_venues = list(Venue.objects.all().order_by("name"))
    profile = getattr(request.user, 'userprofile', None)

    for venue in all_venues:
        if profile:
            venue.controlled = profile.venue_controlled.filter(id=venue.id).exists()
        else:
            venue.controlled = False

    items_per_page = _get_items_per_page(request)
    paginator = Paginator(all_venues, items_per_page)
    page_num = _get_page_num(request, paginator)
    page = paginator.page(page_num)

    context = {
        'venues': page.object_list,
        'page': page,
    }
    return render(request, 'venues.html', context)