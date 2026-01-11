from django.contrib import admin
from .models import Order, Product, Category
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum, Count  # 导入聚合函数用于统计
from django.template.response import TemplateResponse
from django.urls import path

# 1. 定义订单发货动作
@admin.action(description='确认发货并向客户发送邮件')
def ship_selected_orders(modeladmin, request, queryset):
    for order in queryset:
        order.status = '已发货'
        order.save()
        send_mail(
            subject=f'您的订单 #{order.id} 已发货！',
            message=f'您好 {order.customer_name}，商品 {order.product.name} 已经发货。',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['test@example.com'], 
        )

# 2. 注册 Order 模型
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer_name', 'status', 'created_at')
    actions = [ship_selected_orders]
    
    # 指定自定义的后台列表模板
    change_list_template = "admin/order_changelist.html"
    # --- 销售统计报表核心功能 ---
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales-stats/', self.admin_site.admin_view(self.sales_stats_view), name='sales_stats'),
        ]
        return custom_urls + urls

    def sales_stats_view(self, request):
        # 统计逻辑：计算总单数、各商品销量及总额
        total_orders = Order.objects.count()
        product_stats = Order.objects.values('product__name').annotate(
            quantity=Count('id'),
            total_price=Sum('product__price')
        ).order_by('-quantity')

        context = dict(
           self.admin_site.each_context(request),
           total_orders=total_orders,
           product_stats=product_stats,
           title="销售统计报表"
        )
        return TemplateResponse(request, "admin/sales_stats.html", context)

# 3. 注册 Product 模型
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')

# 4. 注册 Category 模型
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)