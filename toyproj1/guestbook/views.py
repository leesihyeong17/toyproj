from django.shortcuts import render
from django.http import JsonResponse # 추가
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods # 추가
from .models import *
# Create your views here.

### DRF 관련 import - APIView 사용
from .serializers import GuestbookSerializer, CommentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

class GuestbookList(APIView):
    def post(self, request, format=None):
        ALLOWED_FIELDS = {'writer', 'title', 'content', 'password'}
        try:
            data = request.data
        except Exception:
            return Response(
                {
                    "status": 400,
                    "message": "요청 본문의 JSON 형식이 올바르지 않습니다."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        for field in ALLOWED_FIELDS: # 필수 입력 필드가 request.data에 존재하는지 확인
            if field not in request.data:
                return Response(
                    {
                        "status": 400,
                        "message": [f"{field}: 이 필드는 blank일 수 없습니다." for field in ALLOWED_FIELDS if field not in request.data]
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        #허용되지 않은 필드 포함
        for field in request.data:
            if field not in ALLOWED_FIELDS:
                return Response(
                    {
                        "status": 400,
                        "message": [f"허용되지 않은 필드: {field}" for field in request.data if field not in ALLOWED_FIELDS]
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        serializer = GuestbookSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"status": 400, "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(
            {
                "status": 201,
                "message": "방명록 생성 성공",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def get(self, request, format=None):
        guestbooks = Guestbook.objects.all().order_by('-created_at')
        serializer = GuestbookSerializer(guestbooks, many=True)
        return Response({
            "status": 200,
            "message": "방명록 목록 조회 성공",
            "data": serializer.data
        })
    
class GuestbookHotList(APIView): #좋아요 수 3개 이상 조회
    def get(self, request, format=None):
        guestbooks = Guestbook.objects.all().order_by('-created_at')
        hot_guestbooks = [gb for gb in guestbooks if gb.like_count() >= 1]
        serializer = GuestbookSerializer(hot_guestbooks, many=True)
        return Response({
            "status": 200,
            "message": "인기 방명록 목록 조회 성공",
            "data": serializer.data
        })

class GuestbookDetail(APIView):
    def get(self, request, guestbook_id):
        try:
            guestbook = Guestbook.objects.get(id=guestbook_id)
        except Guestbook.DoesNotExist: #해당 ID의 게시글이 존재하지 않음
            return Response(
                {
                    "status": 404,
                    "message": "해당 방명록을 찾을 수 없습니다."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = GuestbookSerializer(guestbook)
        return Response(
            {
                "status": 200,
                "message": "방명록 조회 성공",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, guestbook_id):
        try:
            guestbook = Guestbook.objects.get(id=guestbook_id)
        except Guestbook.DoesNotExist: #해당 ID의 게시글이 존재하지 않음
            return Response(
                {
                    "status": 404,
                    "message": "해당 방명록을 찾을 수 없습니다."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        #password 외의 필드가 request.data에 존재하는지 확인
        for field in request.data:
            if field != 'password':
                return Response(
                    {
                        "status": 400,
                        "message": f"허용되지 않은 필드: {field}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.data.get('password') is None: #비밀번호 누락
            return Response(
                {
                    "status": 400,
                    "message": "비밀번호를 입력해주세요."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data.get('password') != guestbook.password: #비밀번호 불일치
            return Response(
                {
                    "status": 403,
                    "message": "비밀번호가 일치하지 않습니다."
                },
                status=status.HTTP_403_FORBIDDEN
            )



        guestbook.delete()
        return Response(
           {
                "status": 200,
                "message": "방명록 삭제 성공"
            },
            status=status.HTTP_200_OK
        )

    def patch(self, request, guestbook_id):
        ALLOWED_FIELDS = {'title', 'content', 'password'}
        try:
            guestbook = Guestbook.objects.get(id=guestbook_id)
        except Guestbook.DoesNotExist: #해당 ID의 게시글이 존재하지 않음
            return Response(
                {
                    "status": 404,
                    "message": "해당 방명록을 찾을 수 없습니다."
                },
                status=status.HTTP_404_NOT_FOUND
            )


        for field in ALLOWED_FIELDS: # 필수 입력 필드가 request.data에 존재하는지 확인
            if field not in request.data:
                return Response(
                    {
                        "status": 400,
                        "message": [f"{field}: 이 필드는 blank일 수 없습니다." for field in ALLOWED_FIELDS if field not in request.data]
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            #허용되지 않은 필드 포함
        for field in request.data:
            if field not in ALLOWED_FIELDS:
                return Response(
                    {
                        "status": 400,
                        "message": [f"허용되지 않은 필드: {field}" for field in request.data if field not in ALLOWED_FIELDS]
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.data.get('password') != guestbook.password: #비밀번호 불일치
            return Response(
                {
                    "status": 403,
                    "message": "비밀번호가 일치하지 않습니다."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = GuestbookSerializer(guestbook, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"status": 400, "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(
            {
                "status": 200,
                "message": "방명록 수정 성공",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class CommentList(APIView):
    def get(self, request, guestbook_id):
        try:
            guestbook = Guestbook.objects.get(id=guestbook_id)
        except Guestbook.DoesNotExist: #해당 ID의 게시글이 존재하지 않음
            return Response(
                {
                    "status": 404,
                    "message": "해당 방명록을 찾을 수 없습니다."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        comments = guestbook.comments.all().order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response({
            "status": 200,
            "message": "댓글 목록 조회 성공",
            "data": serializer.data
        })

    def post(self, request, guestbook_id):
        ALLOWED_FIELDS = {'writer', 'content', 'password'}
        try:
            guestbook = Guestbook.objects.get(id=guestbook_id)
        except Guestbook.DoesNotExist: #해당 ID의 게시글이 존재하지 않음
            return Response(
                {
                    "status": 404,
                    "message": "해당 방명록을 찾을 수 없습니다."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        for field in ALLOWED_FIELDS: # 필수 입력 필드가 request.data에 존재하는지 확인
            if field not in request.data:
                return Response(
                    {
                        "status": 400,
                        "message": [f"{field}: 이 필드는 blank일 수 없습니다." for field in ALLOWED_FIELDS if field not in request.data]
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        #허용되지 않은 필드 포함
        for field in request.data:
            if field not in ALLOWED_FIELDS:
                return Response(
                    {
                        "status": 400,
                        "message": [f"허용되지 않은 필드: {field}" for field in request.data if field not in ALLOWED_FIELDS]
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = CommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"status": 400, "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(post=guestbook)
        return Response(
            {
                "status": 201,
                "message": "댓글 생성 성공",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

class CommentDetail(APIView):
    def delete(self, request, guestbook_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, post_id=guestbook_id)
        except Comment.DoesNotExist: #해당 ID의 댓글이 존재하지 않음
            return Response(
                {
                    "status": 404,
                    "message": "해당 댓글을 찾을 수 없습니다."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        #password 외의 필드가 request.data에 존재하는지 확인
        for field in request.data:
            if field != 'password':
                return Response(
                    {
                        "status": 400,
                        "message": f"허용되지 않은 필드: {field}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.data.get('password') is None: #비밀번호 누락
            return Response(
                {
                    "status": 400,
                    "message": "비밀번호를 입력해주세요."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data.get('password') != comment.password: #비밀번호 불일치
            return Response(
                {
                    "status": 403,
                    "message": "비밀번호가 일치하지 않습니다."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()
        return Response(
           {
                "status": 200,
                "message": "댓글 삭제 성공"
            },
            status=status.HTTP_200_OK
        )

    def patch(self, request, guestbook_id, comment_id):
        ALLOWED_FIELDS = {'content', 'password'}
        try:
            comment = Comment.objects.get(id=comment_id, post_id=guestbook_id)
        except Comment.DoesNotExist: #해당 ID의 댓글이 존재하지 않음
            return Response(
                {
                    "status": 404,
                    "message": "해당 댓글을 찾을 수 없습니다."
                },
                status=status.HTTP_404_NOT_FOUND
            )


        for field in ALLOWED_FIELDS: # 필수 입력 필드가 request.data에 존재하는지 확인
            if field not in request.data:
                return Response(
                    {
                        "status": 400,
                        "message": [f"{field}: 이 필드는 blank일 수 없습니다." for field in ALLOWED_FIELDS if field not in request.data]
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            #허용되지 않은 필드 포함
        for field in request.data:
            if field not in ALLOWED_FIELDS:
                return Response(
                    {
                        "status": 400,
                        "message": [f"허용되지 않은 필드: {field}" for field in request.data if field not in ALLOWED_FIELDS]
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.data.get('password') != comment.password: #비밀번호 불일치
            return Response(
                {
                    "status": 403,
                    "message": "비밀번호가 일치하지 않습니다."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"status": 400, "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {
                "status": 200,
                "message": "댓글 수정 성공",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class GuestbookLikeView(APIView):
    def post(self, request, guestbook_id):
        try:
            guestbook = Guestbook.objects.get(id=guestbook_id)
        except Guestbook.DoesNotExist:
            return Response(
                {
                    "status": 404,
                    "message": "해당 방명록을 찾을 수 없습니다."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        ip = request.META.get('REMOTE_ADDR')
        likes = GuestbookLike.objects.filter(guestbook=guestbook, ip=ip)
        if likes.exists():
            likes.delete()  # 기존 좋아요 삭제
            return Response(
                {
                    "status": 200,
                    "message": "좋아요 취소 성공"
                },
                 status=status.HTTP_200_OK
            )

        GuestbookLike.objects.create(guestbook=guestbook, ip=ip)
        return Response(
            {
                "status": 201,
                "message": "좋아요 성공"
            },
                status=status.HTTP_201_CREATED
        )
    
class CommentLikeView(APIView):
    def post(self, request, guestbook_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, post_id=guestbook_id)
        except Comment.DoesNotExist:
            return Response(
                {
                    "status": 404,
                    "message": "해당 댓글을 찾을 수 없습니다."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        ip = request.META.get('REMOTE_ADDR')
        likes = CommentLike.objects.filter(comment=comment, ip=ip)
        if likes.exists():
            likes.delete()  # 기존 좋아요 삭제
            return Response(
                {
                    "status": 200,
                    "message": "좋아요 취소 성공"
                },
                 status=status.HTTP_200_OK
            )

        CommentLike.objects.create(comment=comment, ip=ip)
        return Response(
            {
                "status": 201,
                "message": "좋아요 성공"
            },
                status=status.HTTP_201_CREATED
        )