from django.db import models
import uuid

def user_directory_path(instance, filename):
    return "inputFile/" + str(uuid.uuid4()) + ".zip"

def input_file_true_color(instance, filename):
    print('filename: ',filename)
    return "true_colors/" + str(uuid.uuid4()) + ".tiff"

def result_directory_path(instance, filename):
    return "inputFile/" + str(uuid.uuid4()) + ".zip"


class InputFile(models.Model):
    models.BigAutoField(primary_key=False, db_index=True, unique=True, editable=False)
    upload = models.FileField(upload_to=user_directory_path)


class InputFileTrueColor(models.Model):
    models.BigAutoField(primary_key=False, db_index=True, unique=True, editable=False)
    upload = models.FileField(upload_to=input_file_true_color)


class ResultFile(models.Model):
    models.BigAutoField(primary_key=False, db_index=True, unique=True, editable=False)
    result_file = models.FileField(upload_to=result_directory_path)