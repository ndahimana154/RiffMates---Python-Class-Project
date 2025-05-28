from django.shortcuts import render,redirect
from django.core.mail import send_mail
from content.forms import CommentForm
from content.models import SeekingAd, MusicianBandChoice

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
    data = {
        'seeking_musician': SeekingAd.objects.filter(seeking=MusicianBandChoice.MUSICIAN).order_by('-date'),
        'seeking_bands': SeekingAd.objects.filter(seeking=MusicianBandChoice.BAND).order_by('-date'),
    }
    return render(request, 'list_ads.html', data)