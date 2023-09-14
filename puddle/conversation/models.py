from django.db import models
from item.models import Item
from django.contrib.auth.models import User

# Create your models here.
class Conversation(models.Model):
    class Meta:
        # - means in descending order
        ordering = ('-modifiedAt', )

    item = models.ForeignKey(Item, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversations')
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='msg', on_delete=models.CASCADE)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(User, related_name='createdMsg', on_delete=models.CASCADE)