from django.shortcuts import render,get_object_or_404
from .models import Musician 

def viewAllBands(request):
    musicians = Musician.objects.all()
    
    context = {
        'musicians': musicians
    }
    return render(request, 'all_bands.html', context)

def viewMusicianDetails(request, id):
    musician = get_object_or_404(Musician, id=id)  # Safer way to get objects
    context = {
        'musician': musician  # Proper context dictionary with key
    }
    return render(request, 'musician_detail.html', context)