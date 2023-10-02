from django.contrib import admin
from comments.models import CommentLike, Comment
from couples.models import Couple
from favourites.models import Admirer
from likes.models import Liker
from posts.models import Post

from accounts.models import UserProfile

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Couple)
admin.site.register(Admirer)
admin.site.register(Liker)
admin.site.register(Comment)
admin.site.register(CommentLike)



