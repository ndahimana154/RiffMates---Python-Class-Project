from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import send_mail
from content.forms import CommentForm,SeekingAdForm
from content.models import SeekingAd, MusicianBandChoice
from django.contrib.auth.decorators import login_required

def comment(request):
    if request.method == 'GET':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            comment = form.cleaned_data['comment']
            message = f"Received comment from Name: {name}\nComment: {comment}"
            send_mail(
                'New Comment Received',
                message,
                'from@example.com',
                ['to@example.com'], 
                fail_silently=False,
            )
            return redirect('comment_accepted')
    
    data = {'form':form}
    return render(request, 'comment.html', data)

def comment_accepted(request):
    data = {"content":  "Thank you for your comment! It has been received."}
    return render(request, 'general.html', data)

def list_ads(request):
    print(SeekingAd.objects.all())
    data = {
        'seeking_musician': SeekingAd.objects.filter(seeking=MusicianBandChoice.MUSICIAN).order_by('-date'),
        'seeking_bands': SeekingAd.objects.filter(seeking=MusicianBandChoice.BAND).order_by('-date'),
    }
    return render(request, 'list_ads.html', data)

@login_required
def seeking_ad(request, ad_id=0):
    if request.method == 'GET':
        if ad_id == 0:
            form = SeekingAdForm()
        else:
            ad = get_object_or_404(SeekingAd, pk=ad_id, owner=request.user)
            form = SeekingAdForm(instance=ad)
            
    elif request.method == 'POST':
        if ad_id == 0:
            form = SeekingAdForm(request.POST)
        else:
            ad = get_object_or_404(SeekingAd, pk=ad_id, owner=request.user)
            form = SeekingAdForm(request.POST, instance=ad)
            
        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = request.user
            ad.save()
            return redirect('list_ads')
    
    data = {'form': form}
    return render(request, 'seeking_ad.html', data)