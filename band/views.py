from django.shortcuts import render,get_object_or_404
from .models import Musician 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.http import Http404,HttpResponse

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


# views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Musician, Band, Venue

def musician_list(request):
    # Handle per_page parameter
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


# views.py
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

# views.py
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
        # Deny access with a 404 error
        raise Http404("Permission denied")
