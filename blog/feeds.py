from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostsFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'
    
    def items(self):
        return Post.objects.filter(P_status='published')[:5]

    def item_title(self, item):
        return item.P_subject
    
    def item_description(self, item):
        return truncatewords(item.P_body, 30)