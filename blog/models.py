from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField



# -----------------# Post # -----------------------------------------------#
class Post(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )
    
    p_author       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='autherposts', null=True) 
    p_subject      = models.CharField(max_length=50, null=True , blank=False)
    p_slug         = models.SlugField(null=True, blank=True, max_length=250)
    p_body         = RichTextField()
    p_status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default='p')
    p_created_at   = models.DateTimeField(default=timezone.now, null=True)
    p_published_at = models.DateTimeField( auto_now_add=True, auto_now=False, null=True)
    p_updated_at   = models.DateTimeField( auto_now_add=False, auto_now=True, null=True)   
    p_tags         = TaggableManager()
       
    class Meta:
      ordering        = ('-p_published_at',)
      unique_together = ["p_subject", "p_published_at"]
    
    def __str__(self):
      return self.p_subject

    # -- for share post by email ----
    def get_absolute_url(self):
      return reverse('blog:post_share_email_path', args=[str(self.id)])

    # -- get absolute url for each detail post
    def get_absolute_url(self):
      return reverse('blog:post_detail', args=[str(self.id)])
 



# -----------------# Comment # -----------------------------------------------#
class Comment(models.Model):
  STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
  )

  c_post         = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postcomments")
  c_body         = RichTextField()
  c_owner_name   = models.CharField(max_length=50, null=True)
  c_owner_email  = models.EmailField(null=True, blank=False)
  c_status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default='p')
  c_created_at   = models.DateTimeField(null=True, auto_now_add=True, auto_now=False)
  p_published_at = models.DateTimeField( auto_now_add=True, auto_now=False, null=True)
  c_updated_at   = models.DateTimeField(null=True, auto_now_add=False, auto_now=True)

  def __str__(self):
    return 'Commented by ({}) on the post: "{}" '.format(self.c_owner_name, self.c_post)

  class Meta:
    ordering = ('-p_published_at',)