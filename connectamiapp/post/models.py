from django.db import models
from connectamiapp.abstract.models import AbstractModel, AbstractManager


class PostManager(AbstractManager):
    pass


class Post(AbstractModel):
    author = models.ForeignKey(to="connectamiapp_user.User",
                               on_delete=models.CASCADE)
    body = models.TextField()
    edited = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    liked = models.BooleanField(default=False)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)

    objects = PostManager()

    def __str__(self):
        return f"{self.author.name}"

    class Meta:
        db_table = "'connectamiapp.post'"
