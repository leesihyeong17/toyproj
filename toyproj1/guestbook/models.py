from django.db import models

# Create your models here.
class BaseModel(models.Model): # models.Model을 상속받음
    created_at = models.DateTimeField(auto_now_add=True) # 객체를 생성할 때 날짜와 시간 저장
    #updated_at = models.DateTimeField(auto_now=True) # 객체를 저장할 때 날짜와 시간 갱신

    class Meta:
        abstract = True


class Guestbook(BaseModel): # BaseModel을 상속받음

    
    id = models.AutoField(primary_key=True)
    writer = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    content = models.TextField()
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.title
    
    def like_count(self):
        return self.likes.count()
    
class Comment(BaseModel): # BaseModel을 상속받음 -> 작성 시간, 수정 시간 저장
    id = models.AutoField(primary_key=True)
    writer = models.CharField(max_length=20)
    content = models.TextField()
    password = models.CharField(max_length=10)
    post = models.ForeignKey(Guestbook, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"{self.post.title}의 댓글: {self.content}"
    
class GuestbookLike(models.Model):
    guestbook = models.ForeignKey(Guestbook, on_delete=models.CASCADE, related_name='likes')
    ip = models.GenericIPAddressField()

    class Meta:
        unique_together = ('guestbook', 'ip')  # 같은 IP로 중복 좋아요 방지


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    ip = models.GenericIPAddressField()

    class Meta:
        unique_together = ('comment', 'ip')  # 같은 IP로 중복 좋아요 방지