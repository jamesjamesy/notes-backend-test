from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    # نام دسته‌بندی با حداکثر ۱۰۰ کاراکتر
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Note(models.Model):
    # ارتباط با کاربر: مشخص می‌کند صاحب این یادداشت کیست
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # اگر کاربر حذف شد، یادداشت‌های او هم خودکار پاک شوند
        null=True,                 # برای اینکه یادداشت‌های قدیمی که کاربر ندارند دچار خطا نشوند
        blank=True,                # در فرم‌ها اجباری نباشد تا بتوانیم خودمان در بک‌اند مقداردهی کنیم
        related_name="notes",      # به ما اجازه می‌دهد تمام یادداشت‌های یک کاربر را با user.notes صدا بزنیم
    )
    # عنوان یادداشت با حداکثر ۲۰۰ کاراکتر
    title = models.CharField(max_length=200)
    # متن اصلی یادداشت
    content = models.TextField()
    # تاریخ و ساعت ساخت یادداشت که خودکار ذخیره می‌شود
    created_at = models.DateTimeField(auto_now_add=True)
    # دسته‌بندی اختیاری یادداشت
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]  # نمایش به ترتیب جدیدترین به قدیمی‌ترین
        
    def __str__(self):
        return self.title
