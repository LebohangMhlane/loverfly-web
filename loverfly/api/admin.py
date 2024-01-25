from django.contrib import admin
from comments.models import CommentLike, Comment, CommentReply, CommentReplyLike
from couples.models import Couple
from admirers.models import Admirer
from likes.models import Liker
from posts.models import Post

from accounts.models import ProfilePicture, UserProfile, UserSetting

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Couple)
admin.site.register(Admirer)
admin.site.register(Liker)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(CommentReply)
admin.site.register(CommentReplyLike)
admin.site.register(ProfilePicture)
admin.site.register(UserSetting)





