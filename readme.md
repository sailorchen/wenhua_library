<h4>文华图书馆项目</h4>
项目创建步骤:<br>
1.安装python及django等模块<br>
2.使用django-admin startproject wenhua_library<br>
3.使用python manage.py startapp home创建首页应用,在项目根目录下新建templates文件夹<br>
4.修改settings.py,在INSTALLED_APPS里面添加home,修改LANGUAGE_CODE='zh-Hans',
修改TIME_ZONE='Asia/Shanghai',修改TEMPLATES里面的DIRS,'DIRS': [os.path.join(BASE_DIR,'templates')],<br>
5.在home文件夹下新建一个urls.py，用来在里面写app的路由,在urls.py里面导入include,
url(r'^wenhua/',include('home.urls'))<br>
6.在home文件夹下的views里面写视图<br>
7.在templates新建index.html<br>
8.创建admin账号
python manage.py migrate
python manage.py createsuperuser
9.迁移数据库
python manage.py makemigrations
python manage.py migrate
10.添加模型到admin中
from home.models import student_user,admin_user,notice_publish
admin.site.register(student_user)