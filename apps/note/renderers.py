from rest_framework import renderers


class StandardResponseRenderer(renderers.JSONRenderer):
    """
    رندرر سفارشی برای کادوپیچ کردن تمام پاسخ‌های API در یک ساختار یکسان:
    {
        "meta": {
            "message": "...",
            "errors": {}
        },
        "data": ...
    }
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            request = renderer_context.get("request")
            response = renderer_context.get("response")

            # استثنا: برای فایل‌های نقشه سواگر و ادمین جنگو قالب را دست‌نخورده رد کن
            if request and (
                request.path.startswith("/api/schema")
                or request.path.startswith("/admin")
            ):
                return super().render(data, accepted_media_type, renderer_context)

            # اگر داده از قبل در قالب meta و data پیچیده شده بود، مجدداً کاری نکن
            if isinstance(data, dict) and "meta" in data and "data" in data:
                return super().render(data, accepted_media_type, renderer_context)

            status_code = response.status_code if response else 200
            method = request.method if request else "GET"

            # ۱. در صورت وجود خطا (کدهای وضعیت 400 به بالا)
            if status_code >= 400:
                message = "خطایی در انجام عملیات رخ داد"
                errors = data if isinstance(data, (dict, list)) else {"detail": str(data)}
                
                # اگر خطای ولیدیشن تک پیامی بود
                if isinstance(data, dict) and "detail" in data:
                    message = data["detail"]
                    errors = {"detail": data["detail"]}
                elif isinstance(data, dict) and "non_field_errors" in data:
                    message = data["non_field_errors"][0] if data["non_field_errors"] else message

                wrapped_data = {
                    "meta": {
                        "message": message,
                        "errors": errors,
                    },
                    "data": None,
                }
                return super().render(wrapped_data, accepted_media_type, renderer_context)

            # ۲. در صورت موفقیت‌آمیز بودن عملیات (کدهای وضعیت 200 یا 201 یا 204)
            default_messages = {
                "GET": "Retrieved successfully",
                "POST": "Created successfully",
                "PUT": "Updated successfully",
                "PATCH": "Updated successfully",
                "DELETE": "Deleted successfully",
            }
            message = default_messages.get(method, "Operation successful")

            # اگر داده شامل پیام اختصاصی بود (مثلاً در ثبت نام)، همان پیام را بردار
            clean_data = data
            if isinstance(data, dict) and "message" in data:
                clean_data = {k: v for k, v in data.items() if k != "message"}
                message = data["message"]

            # در متد DELETE یا پاسخ‌های خالی 204، دیتا مقدار null می‌گیرد
            if status_code == 204 or clean_data is None:
                clean_data = None
                if response:
                    # برای بازگرداندن متن به همراه کدهای حذف، کد وضعیت را به 200 تغییر می‌دهیم
                    response.status_code = 200

            wrapped_data = {
                "meta": {
                    "message": message,
                    "errors": {},
                },
                "data": clean_data,
            }
            return super().render(wrapped_data, accepted_media_type, renderer_context)

        return super().render(data, accepted_media_type, renderer_context)
