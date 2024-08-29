from django.db import models
from django.contrib.auth import get_user_model
import uuid


class Board(models.Model):
    """ Board model for creating different board based on the project needed """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25, unique=True)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)
    admins = models.ManyToManyField(get_user_model(), related_name='admin_boards', blank=True)
    members = models.ManyToManyField(get_user_model(), related_name='member_boards', blank=True)

    def __str__(self):
        return self.name


class Stage(models.Model):
    """ Stage Model for creating stages for each board """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='stages')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('name', 'board')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']


class Task(models.Model):
    """ Task Model for creating tasks """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)     # UUID field for primary key field
    title = models.CharField()
    assignees = models.ManyToManyField(get_user_model(), related_name='assigned_tasks', blank=True)
    description = models.TextField()     # Description of task
    createdat = models.DateTimeField(auto_now_add=True)     # Created date
    updatedat = models.DateTimeField(auto_now=True)     # Date updated
    targetcompletiondate = models.DateTimeField()       # Target Completion Date
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='tasks')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.description
    
    class Meta:
        ordering = ['order']


class SubTask(models.Model):
    """ Sub Task Model for adding sub tasks to each task """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)     # UUID field for primary key field
    assignees = models.ManyToManyField(get_user_model(), related_name='assigned_subtasks', blank=True)     # Many to many field for assigning the subtasks to different members of the board
    description = models.TextField()    # Text Field for adding the description of the subtask
    createdat = models.DateTimeField(auto_now_add=True)     # Created date for sorting and referencing
    updatedat = models.DateTimeField(auto_now=True)     # Date updated for sorting and referencing
    targetcompletiondate = models.DateTimeField()       # Target Completion Date
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')   # One to Many relationship for attaching sub tasks
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.description