from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(statut='published')


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    def __str__(self):
        return self.name
    

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="category_posts"   )
    STATUT_CHOICES =(
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    statut = models.CharField(choices=STATUT_CHOICES,
                               default='draft', max_length=10)
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posted',  )
    objects = models.Manager() #default manager
    published_posts = PublishedManager() #custom manager

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post_detail", args=[self.published.year, self.published.month, self.published. day, self.slug ] )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # username = models.CharField(max_length=100)
    # email = models.EmailField( max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField( auto_now_add=True)
    updated = models.DateTimeField( auto_now=True)

    def __str__(self) -> str:
        return self.post.title
    

