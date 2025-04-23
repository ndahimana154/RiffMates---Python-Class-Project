from django.db import models

class Musician(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    birth=models.DateField()
    def __str__(self):
        return f"Musician={self.id}, first_name={self.first_name}, last_name={self.last_name}, birth={self.birth}"
    

# Musicians
# ● Bands
# ● Classifieds
# ● Venues
# ● Venue lineups
