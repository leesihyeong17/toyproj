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