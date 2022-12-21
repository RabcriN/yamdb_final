from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "bio",
        "role",
        "confirmation_code",
    )
    list_editable = ("role",)
    search_fields = ("username", "role")
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
