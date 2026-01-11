from django.db import models
from django.contrib.auth.models import User

# 1. 商品分类
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="分类名称")
    
    def __str__(self):
        return self.name

# 2. 商品信息 (对应功能：展示产品列表、管理商品目录)
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, verbose_name="产品名称")
    description = models.TextField(verbose_name="描述")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    stock = models.IntegerField(default=0, verbose_name="库存")
    image = models.ImageField(upload_to='products/', verbose_name="产品图片")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    # 允许 user 为空，这样旧订单不会报错
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="下单用户")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    customer_name = models.CharField(max_length=100, verbose_name="收货人姓名", default="匿名")
    address = models.TextField(verbose_name="收货地址", default="未填写")
    status = models.CharField(max_length=20, default='待发货', verbose_name="订单状态")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 定义状态常量
    STATUS_CHOICES = (
        ('待发货', '待发货'),
        ('已发货', '已发货'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='待发货', verbose_name="订单状态")

    def __str__(self):
        return f"订单 #{self.id} - {self.product.name} ({self.status})"

class OrderItem(models.Model):
    # 记录这笔订单里具体的每一项商品
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

# Create your models here.
