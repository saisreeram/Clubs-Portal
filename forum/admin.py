from django.contrib import admin
from .models import Post, Comments, NotificationsEvents, NotificationsPost

# Register your models here.
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(NotificationsEvents)
admin.site.register(NotificationsPost)