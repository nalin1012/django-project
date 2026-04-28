# Importing DRF’s serializers module to convert: Django Model → JSON & JSON → Django Model
# DRF provides classes like: Serializer, ModelSerializer
# To handle: Data conversion, Validation, Saving data

from rest_framework import serializers
from .models import Post

# Creating a serializer class for Post model
# Why we use ModelSerializer? It automatically Creates fields, Adds validation, Handles create/update
class PostSerializer(serializers.ModelSerializer):
    
    # Show username instead of ID
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = '__all__'