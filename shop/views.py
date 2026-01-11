from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Order
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm

@login_required # 添加这个装饰器，未登录访问首页会直接跳到登录页
def index(request):
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})

@login_required # 确保购买流程也必须登录
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def order_history(request):
    # 只获取属于当前登录用户的订单
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_history.html', {'orders': orders})


def product_list(request):
    # 从数据库获取所有商品
    products = Product.objects.all()
    # 获取所有分类（用于侧边栏展示）
    categories = Category.objects.all()
    
    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories
    })

# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})

def product_detail(request, pk):  # 确保这里的参数名是 pk
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('shop:cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for p_id, quantity in cart.items():
        product = Product.objects.get(id=p_id)
        items.append({'product': product, 'quantity': quantity, 'subtotal': product.price * quantity})
        total += product.price * quantity
    return render(request, 'shop/cart.html', {'items': items, 'total': total})

def create_order(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        # 模拟创建一个订单
        Order.objects.create(
            product=product,
            customer_name="实验测试用户", 
            address="学校宿舍楼"
        )
        return render(request, 'shop/order_success.html', {'product': product})

@login_required # 关键：确保只有登录用户才能下单，否则 request.user 是匿名用户
def quick_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        # 在创建订单时，将 user 字段设置为当前的 request.user
        order = Order.objects.create(
            product=product,
            user=request.user,  # 核心修改：关联当前登录账号
            customer_name="实验测试用户",
            address="山东省烟台市某校区",
            status="待发货"
        )
        return render(request, 'shop/order_success.html', {'order': order})
    
    # 如果不是 POST 请求，重定向回详情页
    return redirect('shop:product_detail', pk=product_id)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # 注册后立即自动登录
            return redirect('shop:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def ship_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # 1. 更新订单状态
    order.status = 'shipped' # 假设你在模型里定义了状态字段
    order.save()
    
    # 2. 发送邮件通知
    subject = f'您的订单 #{order.id} 已发货！'
    message = f'亲爱的 {order.user.username}，您购买的商品已经发出，请注意查收。'
    recipient_list = [order.user.email] # 发送到注册用户的邮箱
    
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    except Exception as e:
        print(f"邮件发送失败: {e}")
        
    return redirect('shop:order_history')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('shop:index') # 登录成功回到主页
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('shop:index')
