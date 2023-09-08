import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404
from connectamiapp.abstract.models import AbstractModel, AbstractManager


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.public_id, filename)


class UserManager(BaseUserManager, AbstractManager):
    """
    Custom manager for the User model.
    """

    def get_object_by_public_id(self, public_id):
        """
        Retrieve a user object by their public_id.

        Args:
            public_id (UUID): The public_id of the user to retrieve.

        Returns:
            User: The user object.
        Raises:
            Http404: If the user with the specified public_id does not exist.
        """
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404

    def create_user(self, username, email, password=None, **kwargs):
        """
        Create and return a `User` with an email, phone number, username, and password.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str): The user's password.
            **kwargs: Additional keyword arguments.

        Returns:
            User: The created user object.
        Raises:
            TypeError: If username, email, or password is None.
        """
        if username is None:
            raise TypeError('Users must have a username!')
        if email is None:
            raise TypeError('Users must have an email!')
        if password is None:
            raise TypeError('User must have an email password!')
        user = self.model(username=username,
                          email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email, password,
                         **kwargs):
        """
        Create and return a `User` with superuser (admin) permissions.

        Args:
            username (str): The username of the superuser.
            email (str): The email address of the superuser.
            password (str): The superuser's password.
            **kwargs: Additional keyword arguments.

        Returns:
            User: The created superuser object.
        Raises:
            TypeError: If username, email, or password is None.
        """
        if password is None:
            raise TypeError('Superuser must have an email password!')
        if email is None:
            raise TypeError('Superuser must have an email!')
        if username is None:
            raise TypeError('Superuser must have an username!')
        user = self.create_user(username, email, password,
                                **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email as the unique identifier.
    """
    public_id = models.UUIDField(db_index=True, unique=True,
                                 default=uuid.uuid4, editable=False)
    username = models.CharField(db_index=True,
                                max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(
        null=True, blank=True, upload_to=user_directory_path)

    posts_liked = models.ManyToManyField(
        "connectamiapp_post.Post", related_name="liked_by")
    comments_liked = models.ManyToManyField(
        "connectamiapp_comment.Comment", related_name="commented_by")

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        """
        String representation of the user (email).
        """
        return f"{self.email}"

    @property
    def name(self):
        """
        Get the full name of the user.
        """
        return f"{self.first_name} {self.last_name}"

    def like_post(self, post):
        """Like `post` if it hasn't been done yet"""
        return self.posts_liked.add(post)

    def remove_like_post(self, post):
        """Remove a like from a `post`"""
        return self.posts_liked.remove(post)

    def has_liked_post(self, post):
        """Return True if the user has liked a `post`; else False"""
        return self.posts_liked.filter(pk=post.pk).exists()

    def like_comment(self, comment):
        """Like `comment` if it hasn't been done yet"""
        return self.comments_liked.add(comment)

    def remove_like_comment(self, comment):
        """Remove a like from a `comment`"""
        return self.comments_liked.remove(comment)

    def has_liked_comment(self, comment):
        """Return True if the user has liked a `comment`; else False"""
        return self.comments_liked.filter(pk=comment.pk).exists()
