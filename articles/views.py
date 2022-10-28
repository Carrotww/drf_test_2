from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from articles.models import Article, Comment
from  articles.serializers import ArticleSerializer, ArticleListSerializer, ArticleCreateSerializer, CommentSerializer, CommentCreateSerializer

# Create your views here.

class ArticleView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        serializer_list = ArticleListSerializer(articles, many=True)

        return Response(serializer_list.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        slz = ArticleSerializer(data=request.data)
        slz = ArticleCreateSerializer(data=request.data)
        if slz.is_valid():
            slz.save(user=request.user)
            return Response(slz.data, status.HTTP_200_OK)
        else:
            return Response(slz.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetailView(APIView):
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        slz = ArticleSerializer(article)
        return Response(slz.data, status=status.HTTP_200_OK)
    
    def put(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            slz = ArticleCreateSerializer(article, data=request.data)
            if slz.is_valid():
                slz.save()
                return Response(slz.data, status.HTTP_200_OK)
            else:
                return Response(slz.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)


    def delete(self, request, article_id):
        article = Article.objects.get(id=article_id)
        if request.user == article.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

class CommentView(APIView):
    def get(self, request, article_id):
        article = Article.objects.get(id=article_id)
        comments = article.comment_set.all()
        slz = CommentSerializer(comments, many=True)
        return Response(slz.data, status=status.HTTP_200_OK)
    
    def post(self, request, article_id):
        slz = CommentCreateSerializer(data=request.data)
        if slz.is_valid():
            slz.save(user=request.user, article_id=article_id)
            return Response(slz.data, status.HTTP_200_OK)
        else:
            return Response(slz.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            slz = CommentCreateSerializer(comment, data=request.data)
            if slz.is_valid():
                slz.save()
                return Response(slz.data, status=status.HTTP_200_OK)
            else:
                return Response(slz.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!.", status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!.", status=status.HTTP_403_FORBIDDEN)


class LikeView(APIView):
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response("unfollow is done", status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response("follow is done", status=status.HTTP_200_OK)

