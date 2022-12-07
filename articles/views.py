from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from articles.models import Article, Comment, Book
from articles.serializers import ArticleSerializer, ArticleCreateSerializer, ArticleDetailSerializer, CommentCreateSerializer
from rest_framework.generics import get_object_or_404
from django.db.models import Count
from articles import crowling, function
import json

# crowling.function()

class ArticleView(APIView): #게시글 불러오기(인기글로) main1
    def get(self, request):
        print(request.data)
        test = request.data.get("select_books_id")
        book_list = Book.objects.filter(id__in=test)
        book_name_list = []
        for book in book_list:
            book_name_list.append(book.book_title)
        print(book_name_list)
        function.select_recommendations(book_name_list)

        return Response(status=status.HTTP_200_OK)

    def post(self, request): # 게시글 작성
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)



class ArticleListView(APIView): # 피드페이지
    def get(self, request):
        articles_list = Article.objects.all()
        serializer = ArticleSerializer(articles_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleDetailView(APIView):
    def get(self, request, article_id): # 게시글&댓글 보여주기
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self, request, article_id): # 게시글 삭제하기
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("작성자가 아닙니다!", status=status.HTTP_403_FORBIDDEN)
    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleEditView(APIView):
    def put(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            serializer = ArticleCreateSerializer(article, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("작성자가 아닙니다!", status=status.HTTP_403_FORBIDDEN)


class CommentEditView(APIView):
    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("작성자가 아닙니다!", status=status.HTTP_403_FORBIDDEN)
    def delete(self, request, comment_id, article_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("작성자가 아닙니다!", status=status.HTTP_403_FORBIDDEN)


class LikeView(APIView): #좋아요
    def post(self, request, article_id):
        article = get_object_or_404(Article, id = article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response({"message":"좋아요 취소 완료!"}, status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response({"message":"좋아요 등록 완료!"}, status=status.HTTP_200_OK)







