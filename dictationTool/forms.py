from django.forms import Form, CharField
from tinymce.widgets import TinyMCE
from .models import Editor
from voiceDictation.settings import TINYMCE_DEFAULT_CONFIG

class FlatPageForm(Form):
    content = CharField(widget=TinyMCE(), label='')
