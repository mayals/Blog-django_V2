from django.contrib import admin
from .models import Post
from .models import Comment



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('p_subject', 'p_author', 'p_created_at', 'p_published_at',
                    'p_updated_at', 'p_body', 'p_slug', 'p_status','p_tags')
    list_filter = ('p_status', 'p_created_at', 'p_published_at', 'p_author')
    search_fields = ('p_subject', 'p_body')
    prepopulated_fields = {'p_slug': ('p_subject',)}
    raw_id_fields = ('p_author',)
    date_hierarchy = 'p_published_at'
    ordering = ('p_status', 'p_published_at')


admin.site.register(Comment)
