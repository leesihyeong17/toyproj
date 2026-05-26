from rest_framework import serializers
from .models import Guestbook

class GuestbookSerializer(serializers.ModelSerializer):

  class Meta:
    model = Guestbook    # serializer가 어떤 모델을 기반으로 만들어지는지 >> guestbook
    fields = '__all__'
    extra_kwargs = {'password': {'write_only': True}} # password 필드는 쓰기만 가능

  def validate_password(self, value):
      if len(value) != 4 or not value.isdigit():
          raise serializers.ValidationError("비밀번호는 4자리 숫자여야 합니다.")
      return value

  def validate_writer(self, value):
      if len(value) > 10:
          raise serializers.ValidationError("이 필드의 글자 수가 10 이하인지 확인하세요.")
      return value

  def validate_title(self, value):
      if len(value) > 30:
          raise serializers.ValidationError("이 필드의 글자 수가 30 이하인지 확인하세요.")
      return value