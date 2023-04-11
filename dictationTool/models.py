from django.db import models
from tinymce.models import HTMLField

# Create your models here.


class Editor(models.Model):
    content = HTMLField()

