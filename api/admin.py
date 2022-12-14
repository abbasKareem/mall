from django.contrib import admin
from django_admin_geomap import ModelAdmin
from django.utils.html import format_html
from django.urls import reverse
from datetime import datetime, timezone
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.http import HttpResponse
import csv

from .models import *
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
    search_fields = ('phone_number', 'username')
    list_filter = ('is_staff', 'start_date', 'state')
    ordering = ('-start_date',)
    list_per_page = 10
    list_display = ('phone_number', 'username', 'is_superuser', 'is_active',
                    'is_staff', 'shop_name', 'state')
    fieldsets = (
        (None, {'fields': ('phone_number', 'username', 'email', 'otp')}),
        ('الصلاحيات', {'fields': ('is_staff', 'is_superuser', 'is_active',
                                  'groups', 'user_permissions')}),
        ('معلومات المحل', {
         'fields': ('shop_name', 'image', 'shop_discription', 'state')}),
        ('معلومات الزبون', {
         'fields': ('first_name', 'last_name', 'points')})
    )

    view_on_site = False
    admin.site.site_url = None

    def has_add_permission(self, request, obj=None):
        return False

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'username', 'password1', 'password2',  'is_staff')}
         ),
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = ['the_image', 'title', 'price', 'selling_price',
                    'category', 'view_count', 'is_public', 'quantity', 'shop', 'colors', 'sizes']
    # list_editable = ['is_public', 'price']
    ordering = ['-id']
    search_fields = ('title',)
    list_filter = ('category', 'is_public', 'quantity', 'size', 'color')

    filter_horizontal = ['color', 'size']

    # change_list_template = 'change_list_product.html'
    # change_form_template = 'change_form.html'

    readonly_fields = ['view_count']
    list_per_page = 10
    view_on_site = False

    def shop(self, obj):
        return obj.user.shop_name

    def colors(self, obj):
        return "\n, ".join([p.color_name for p in obj.color.all()])

    def sizes(self, obj):
        return "\n, ".join([p.size_name for p in obj.size.all()])

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = CustomUser.objects.filter(
                username=request.user.username)
            # kwargs["queryset"] = request.user

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderAdmin(ModelAdmin):
    geomap_field_longitude = "id_lon"
    geomap_field_latitude = "id_lat"
    geomap_default_longitude = "44.03287850414396"
    geomap_default_latitude = "32.616430004635404"
    # geomap_height = "300px"

    view_on_site = False

    def has_add_permission(self, request, obj=None):
        return False

    fieldsets = (
        ('اسم المحل', {'fields': ('shop',)}),
        ('التخفيضات وحالة الطلب', {'fields': ('discount', 'order_status')}),
        ('معلومات الزبون', {'fields': ('points', 'email',
         'user_phone',   'user_name', 'full_name')}),
        ('معلومات الطلب', {'fields': ('quantity_of_product_ordered',
         'product_ordered', 'created_at', 'total', 'total_after_discount', 'message')}),
    )

    readonly_fields = ['owner', 'user_name', 'product', 'mobile', 'email', 'since',
                       'total', 'total_after_discount', 'created_at', 'lon', 'lat', 'message', 'points', 'user_phone', 'quantity_of_product_ordered', 'product_ordered', 'full_name', 'shop']
    list_display = ['view', 'since', 'order_status',  'products_counts',
                    'discount', 'total', 'total_after_discount', 'created_at', 'email', 'points', 'user_phone']
    ordering = ['-id']
    search_fields = ('product__title',)
    list_filter = ['order_status', 'discount', 'created_at']
    list_per_page = 10

    # change_list_template = 'change_list_order.html'

    # actions = [export_as_csv]
    # def message_user(self, *args):
    #     pass

    # def save_model(self, request, obj, form, change):
    #     messages.add_message(request, messages.INFO, 'order created')
    #     super(OrderAdmin, self).save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def quantity_of_product(self, obj):
        return "\n\n\n\n".join([str(p.quantity) for p in obj.product.all()])

    def view(self, obj):
        return "عرض الطلب"

    def product_ordered(self, obj):
        my_str = ""
        for pro in obj.product.all():
            my_str += f"{pro.title}\n\n الكمية: {pro.quantity_ordered} * {pro.selling_price} = {pro.quantity_ordered * pro.selling_price} \n\n الالوان:  {pro.colors}\n\n الاحجام :{pro.sizes} \n"
            my_str += '...........................................\n'
        return my_str

    def quantity_of_product_ordered(self, obj):
        total = 0
        for pro in obj.product.all():
            total += pro.quantity_ordered
        return str(total)

    def since(self, obj):
        date_time_dif = datetime.now(timezone.utc) - obj.created_at
        return str(date_time_dif)[:-6]

    def points(self, obj):
        return obj.ordered_by.points

    def user_name(self, obj):
        return obj.ordered_by.username

    def shop(self, obj):
        return obj.owner.shop_name

    def user_phone(self, obj):
        return obj.ordered_by.phone_number

    def full_name(self, obj):
        # return f"<h1>{obj.ordered_by.first_name}   {obj.ordered_by.last_name}</h1>"
        return f"{obj.ordered_by.first_name}   {obj.ordered_by.last_name}"

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
    list_filter = ['user', 'product', 'review_rating']
    # list_display = ['user', 'review_rating']
    list_per_page = 20

    list_filter = ['review_rating']

    view_on_site = False

    def has_add_permission(self, request, obj=None):
        return False


class WishListAdmin(admin.ModelAdmin):
    list_display = ['user']


class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'sizes', 'colors', 'quantity_ordered']


class ComplaintAdmin(admin.ModelAdmin):
    readonly_fields = ['user', 'created_at']
    list_display = ['user', 'created_at']
    list_filter = ['created_at']
    list_per_page = 10

    def has_add_permission(self, request, obj=None):
        return False


class ColorAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'the_color']
    list_per_page = 20

    change_list_template = 'change_list_color.html'

    view_on_site = False


class SizeAdmin(admin.ModelAdmin):
    list_display = ['size_name']
    list_per_page = 20

    view_on_site = False

    change_list_template = 'change_list_size.html'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_per_page = 20
    view_on_site = False

    change_list_template = 'change_list_category.html'


admin.site.register(CustomUser, UserAdminConfig)
# admin.site.register(CustomUser)

admin.site.register(Size, SizeAdmin)
# admin.site.register(ProductOrder, ProductOrderAdmin)
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(WishList, WishListAdmin)
