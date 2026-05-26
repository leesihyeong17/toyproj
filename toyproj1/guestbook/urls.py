from django.urls import path
from guestbook.views import *

urlpatterns = [
    path('', GuestbookList.as_view()),
    path('<int:guestbook_id>/', GuestbookDetail.as_view()),
]