from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import Category, Note
from .serializers import (
    CategorySerializer,
    NoteSerializer,
    NoteWriteSerializer,
    RegisterSerializer,
)


class NoteViewSet(viewsets.ModelViewSet):
    # انتخاب نوع سریالایزر: برای ایجاد/ویرایش از فرمت سبک‌تر و برای نمایش از فرمت کامل استفاده می‌شود
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return NoteWriteSerializer

        return NoteSerializer

    # واکشی یادداشت‌ها از دیتابیس با فیلتر مالکیت کاربر
    def get_queryset(self):
        # اگر کاربر لاگین کرده باشد، فقط یادداشت‌های متعلق به خودش را برمی‌گرداند
        if self.request.user.is_authenticated:
            return Note.objects.filter(user=self.request.user)

        # در صورتی که کاربری لاگین نکرده باشد، یادداشت‌های عمومی قبلی را نشان می‌دهد تا اپ فلوتر تا زمان ساخت لاگین از کار نیفتد
        return Note.objects.filter(user__isnull=True)

    # قلاب (Hook) ساخت نوت جدید: هنگام ذخیره در دیتابیس فراخوانی می‌شود
    def perform_create(self, serializer):
        # اگر کاربری وارد شده باشد، به صورت خودکار کاربر فعلی را به عنوان صاحب نوت ثبت کن
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    # دسته‌بندی‌ها فعلاً عمومی هستند و همه کاربران می‌توانند آن‌ها را ببینند
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RegisterView(generics.CreateAPIView):
    # این آدرس برای همه آزاد است و نیازی به داشتن توکن از قبل ندارد
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    # متد پردازش ساخت کاربر جدید
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # کاربر ذخیره می‌شود
        user = serializer.save()
        # بلافاصله برای کاربر تازه ثبت‌نام‌شده توکن ساخته می‌شود تا کاربر در همان لحظه لاگین شود
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "username": user.username,
                "message": "کاربر با موفقیت ثبت شد",
            },
            status=status.HTTP_201_CREATED,
        )
