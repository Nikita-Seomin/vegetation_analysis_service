from django.db import models
from django.conf import settings
from django.conf.urls.static import static
import uuid

def user_directory_path(instance, filename):
    return "inputFile/" + str(uuid.uuid4()) + ".zip"


class InputFile(models.Model):
    models.BigAutoField(primary_key=False, db_index=True, unique=True, editable=False)
    upload = models.FileField(upload_to=user_directory_path)