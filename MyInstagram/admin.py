from django.contrib import admin

from .models import City
admin.site.register(City)

from .models import User
admin.site.register(User)

from .models import Photo
admin.site.register(Photo)

from .models import Comment
admin.site.register(Comment)

from .models import Post
admin.site.register(Post)

