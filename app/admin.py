from django.contrib import admin
from app.models import User,Profile,Comment,Session,Module,Announcement,AnnounComment

# Register your models here.


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Session)
admin.site.register(Module)
admin.site.register(Announcement)
admin.site.register(AnnounComment)
