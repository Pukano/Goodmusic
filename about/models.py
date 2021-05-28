from django.db import models

# Create your models here.

class About(models.Model):
    vision = models.TextField()
    mission = models.TextField()
    picture = models.URLField("URL de l'image", )

    def __str__(self):
        return str(self.id)
