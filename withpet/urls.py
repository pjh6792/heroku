"""withpet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import blog.views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blog.views.home, name='home'),
    path('comment_write/<int:post_pk>/', blog.views.comment_write, name="comment_write" ),
    path('delete/<int:post_id>', blog.views.delete, name = 'delete'),
    path('delete1/<int:post_id>/<int:comment_id>', blog.views.delete1, name = 'delete1'),
    path('post/<int:post_id>', blog.views.post, name = 'post'),
    path('post/<pk>/likes/', blog.views.like, name = 'likes'),
    path('modify/<int:post_id>', blog.views.modify, name='modify'),
    path('new/', blog.views.new, name = "new"),
    path('accounts/',include('accounts.urls')),
    path('detail/', blog.views.detail, name = "detail"),

] 
urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)