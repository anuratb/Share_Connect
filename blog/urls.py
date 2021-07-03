from django.urls import path
from . import views

urlpatterns = [
    path('post-blog/', views.post_blog ),
    path('upvote-blog/<blog_id>/',views.upvote),
    path('downvote-blog/<blog_id>/',views.downvote),
    path('upvote-comment/<comment_id>/',views.upvote_comment),
    path('downvote-comment/<comment_id>/',views.downvote_comment),
    path('delete-blog/',views.delete_blog),
    path('get-blogs/',views.get_blogs),
    path('post-comments/<blog_id>/',views.add_comment),
    path('update-blog/<blog_id>/',views.update_blog)
]