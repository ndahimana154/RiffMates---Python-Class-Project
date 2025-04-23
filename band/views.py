from django.shortcuts import render,get_object_or_404
from .models import Musician 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def viewAllBands(request):
    musicians_list = Musician.objects.all()
    paginator = Paginator(musicians_list, 5)  # 10 items per page

    page_number = request.GET.get('page')
    try:
        musicians = paginator.page(page_number)
    except PageNotAnInteger:
        # Deliver first page if page is not an integer
        musicians = paginator.page(1)
    except EmptyPage:
        # Deliver last page if page is out of range
        musicians = paginator.page(paginator.num_pages)

    context = {'musicians': musicians}
    return render(request, 'all_bands.html', context)

def viewMusicianDetails(request, id):
    musician = get_object_or_404(Musician, id=id)  # Safer way to get objects
    context = {
        'musician': musician  # Proper context dictionary with key
    }
    return render(request, 'musician_detail.html', context)