from rest_framework.serializers import ModelSerializer, ValidationError, ReadOnlyField
from .models import Like, Comment, Rating, Dislike, Favorites


class CommentSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        comment = Comment.objects.create(author=user, **validated_data)
        return comment


class RatingSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = '__all__'

    def validate_rating(self, rating):
        if rating in range(1, 6):
            return rating
        raise ValidationError(
            'rating not be more 5'
        )

    def validate_product(self, product):
        user = self.context.get('request').user
        if self.Meta.model.objects.filter(product=product, author=user):
            raise ValidationError(
                "You can't be rating"
            )
        return product

    def create(self, validated_data):
        user = self.context.get('request').user
        return self.Meta.model.objects.create(author=user, **validated_data)


class RatingActionSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    product = ReadOnlyField()

    class Meta:
        model = Rating
        fields = '__all__'

    def validate_rating(self, rating):
        if rating in range(1, 6):
            return rating
        raise ValidationError(
            'rating not be more 5'
        )

    def validate_product(self, product):
        user = self.context.get('request').user
        if self.Meta.model.objects.filter(product=product, author=user):
            raise ValidationError(
                "You can't be rating"
            )
        return product


class LikeSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    product = ReadOnlyField()

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        return self.Meta.model.objects.create(author=user, **validated_data)


class DisLikeSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    product = ReadOnlyField()

    class Meta:
        model = Dislike
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        return self.Meta.model.objects.create(author=user, **validated_data)


class FavoritesSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    product = ReadOnlyField()

    class Meta:
        model = Favorites
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        return self.Meta.model.objects.create(author=user, **validated_data)


class FavoritesListSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Favorites
        fields = '__all__'


# class FavoritesListSerializer(ModelSerializer):
#     product = ProductDetailSerializer
#
#     class Meta:
#         model = Favorites
#         fields = ['product']
