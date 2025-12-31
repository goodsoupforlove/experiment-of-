#!/bin/bash
echo "正在创建Django项目结构..."

# 创建目录结构
mkdir -p shop/templates/shop
mkdir -p shop/templates/shop/admin
mkdir -p static/css static/js static/images
mkdir -p media/products

# 创建空文件
touch shop/urls.py
touch shop/forms.py
touch shop/context_processors.py
touch static/css/style.css
touch static/js/main.js

# 创建配置文件
cat > .gitignore << 'GITIGNORE'
# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/
venv2/
env/

# Django
*.log
*.pot
*.pyc
db.sqlite3
media/
staticfiles/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
GITIGNORE

cat > requirements.txt << 'REQUIREMENTS'
Django==4.2.7
mysqlclient==2.2.0
Pillow==10.0.0
django-crispy-forms==2.0
crispy-bootstrap5==0.7
django-environ==0.10.0
celery==5.3.0
redis==4.5.5
django-celery-results==2.5.0
gunicorn==21.2.0
REQUIREMENTS

cat > .env.example << 'ENVEXAMPLE'
DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
DB_NAME=online_shop
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
REDIS_URL=redis://localhost:6379/0
ENVEXAMPLE

cat > README.md << 'README'
# 在线购物网站 - 课程实验项目

## 项目简介
基于Django + Bootstrap + MySQL的在线购物系统

## 快速开始
1. 激活虚拟环境
2. pip install -r requirements.txt
3. cp .env.example .env
4. 配置.env文件中的数据库信息
5. python manage.py migrate
6. python manage.py runserver

## 访问
- 网站: http://localhost:8000
- 后台: http://localhost:8000/admin
README

echo "项目结构创建完成！"
echo "请执行: chmod +x setup_project.sh && ./setup_project.sh"
