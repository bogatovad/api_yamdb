from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Comment, Review, Category, Genre, Title

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=('title_id', 'author'),
        #         message='cannot add another review'
        #     )
        # ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']


# class CategorySerializer(serializers.ModelSerializer):
#     # slug = serializers.SlugRelatedField(
#     #     slug_field='slug',
#     #     read_only=True,
#     #     default=serializers.CurrentUserDefault())
#
#     class Meta:
#         fields = ('__all__')
#         model = Category
#
#
# class GenreSerializer(serializers.ModelSerializer):
#     # slug = serializers.SlugRelatedField(
#     #     slug_field='slug',
#     #     read_only=True,
#     #     default=serializers.CurrentUserDefault())
#
#     class Meta:
#         fields = ('__all__')
#         model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name','slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name','slug')


class TitleSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('__all__')
        model = Title

