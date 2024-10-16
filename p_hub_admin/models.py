from django.db import models

# Create your models here.
class user(models.Model):
    username = models.char_field(max_length = 100)
    password = models.char_field(max_length = 20)

    def __str__ (self):
        return self.username