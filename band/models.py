from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Musician(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    birth=models.DateField()
    def __str__(self):
        return f"Musician={self.id}, first_name={self.first_name}, last_name={self.last_name}, birth={self.birth}"
    
class Venue(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    picture = models.ImageField( blank=True, null=True)

    def __str__(self):
        return f"id={self.id}, name={self.name}"

class Room(models.Model):
    name = models.CharField(max_length=50)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return f"Room={self.id}, name={self.name}, venue={self.venue}"

class Band(models.Model):
    name = models.CharField(max_length=50)
    musicians = models.ManyToManyField(Musician)

    def __str__(self):
        return f"Band={self.id}, name={self.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    musician_profiles = models.ManyToManyField(Musician, blank=True)
    venue_controlled = models.ManyToManyField(Venue, blank=True)

    def __str__(self):
        return self.user.username

# Automatically create UserProfile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Musicians
# ● Bands
# ● Classifieds
# ● Venues
# ● Venue lineups
