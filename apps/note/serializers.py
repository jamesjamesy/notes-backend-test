from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, Note



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class NoteSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, allow_null=True)

    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "updated_at", "category"]
        read_only_fields = ["id", "created_at", "updated_at"]


class NoteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["title", "content", "category"]

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Title must be at least 3 characters long."
            )
        return value


class RegisterSerializer(serializers.ModelSerializer):
    # رمز عبور: فقط دریافت شود (write_only) و در پاسخ‌های سرور نمایش داده نشود
    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        # ساخت کاربر با متد create_user که خودکار رمز را هش (رمزنگاری یک‌طرفه) می‌کند
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user