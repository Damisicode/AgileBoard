from django.contrib import admin
from .models import Board, Stage, Task, SubTask

# Register your models here.
admin.site.register(Board)
admin.site.register(Stage)
admin.site.register(Task)
admin.site.register(SubTask)