from django.urls import path
from guestbook.views import *

urlpatterns = [
    path('', GuestbookList.as_view()),
    path('<int:guestbook_id>/', GuestbookDetail.as_view()),
    path('<int:guestbook_id>/comment/', CommentList.as_view()),
    path('<int:guestbook_id>/comment/<int:comment_id>/', CommentDetail.as_view()),
    path('<int:guestbook_id>/like/', GuestbookLikeView.as_view()),
    path('<int:guestbook_id>/comment/<int:comment_id>/like/', CommentLikeView.as_view()),
    path('hot/', GuestbookHotList.as_view()),
]