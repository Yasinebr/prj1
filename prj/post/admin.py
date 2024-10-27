from django.contrib import admin
from . models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    prepopulated_fields = {'slug':('body',)}
    search_fields = ('slug', 'body')
    list_filter = ('updated',)
    list_display = ('user', 'slug', 'updated')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin)   :
    list_display = ('user', 'post', 'created', 'is_reply')
    raw_id_fields = ('user', 'post', 'reply')



