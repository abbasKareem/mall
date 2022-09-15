from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.http import HttpResponse
import csv

from .models import Category, Product,  Order, CustomUser, ProductReview
from .forms import CustomUserCreationForm


def export_as_csv(self, request, queryset):
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]
    response = HttpResponse(content_type='text.csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
        meta)
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])
    return response


export_as_csv.short_description = "Download order"


def download_csv(modeladmin, request, queryset):
    import csv
    f = open('some.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(["mobile", 'email'])
    for s in queryset:
        writer.writerow([s.mobile, s.email])


class UserAdminConfig(UserAdmin):
    model = CustomUser
    readonly_fields = ['points']
    search_fields = ('email', 'username', 'first_name',)
    list_filter = ('is_staff', 'points', 'start_date')
    ordering = ('-start_date',)
    list_display = ('email', 'username', 'first_name',
                    'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Personal', {'fields': ('points',
         'shop_name', 'image', 'shop_discription')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'password1', 'password2',  'is_staff')}
         ),
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'title',  'user', 'price', 'selling_price',
                    'category', 'view_count', 'is_public', 'rating']
    ordering = ['-id']
    search_fields = ('title',)
    list_filter = ('price', 'selling_price', 'category',
                   'view_count', 'is_public')

    readonly_fields = ['view_count']
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = CustomUser.objects.filter(
                username=request.user.username)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['owner', 'product', 'ordered_by',
                       'shipping_address', 'mobile', 'email', 'mobile', 'total', 'total_after_discount', 'created_at']
    # exclude = ['owner']

    list_display = ['id', 'ordered_by',  'user_points',
                    'shipping_address', 'order_status', 'created_at', 'products_counts', 'mobile', 'email', 'discount', 'total', 'total_after_discount']
    ordering = ['-id']
    search_fields = ('product',)
    list_filter = ['ordered_by', 'order_status', 'discount']
    list_per_page = 10

    actions = [export_as_csv]

    def user_points(self, obj):
        return obj.ordered_by.points

    def products_counts(self, obj):
        return obj.product.count()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user).order_by('-id')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "order":
            kwargs["queryset"] = Order.objects.filter(
                owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductReviewAdmin(admin.ModelAdmin):
    readonly_fields = ['user', 'product', 'review_rating']


admin.site.register(CustomUser, UserAdminConfig)

admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register([Category])
