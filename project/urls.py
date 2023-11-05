from django.contrib import admin
from django.urls import path,include

from django.conf.urls.static import static
from django.conf import settings

# add your sitemap URL
from django.contrib.sitemaps import views
from blog.sitemaps import PostSitemap


sitemaps = {
    'posts': PostSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/',include('blog.urls')),
    path('users/',include('users.urls')),

    # add your sitemap path
    path('sitemap.xml', views.sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    # https://pypi.org/project/django-ckeditor/#installation
    path('ckeditor/', include('ckeditor_uploader.urls')),
 
         
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)