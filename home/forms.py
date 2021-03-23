from django import forms
from home import models

#用户登录表单验证
class UserLoginForm(forms.Form):
    username = forms.CharField(min_length=2,label="用户名",max_length=20,widget=forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':'学号'}))
    pwd = forms.CharField(min_length=6,max_length=20,label="密码",widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg','placeholder':'密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        pwd = self.cleaned_data['pwd']
        verify_user = models.student_user.objects.filter(s_no=username, s_pwd=pwd,s_status=1)
        if not verify_user:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = username
        return self.cleaned_data


#管理员登录表单验证
class AdminLoginForm(forms.Form):
    username = forms.CharField(min_length=2,label="用户名",max_length=20,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'工作号'}))
    pwd = forms.CharField(min_length=2,max_length=20,label="密码",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        pwd = self.cleaned_data['pwd']
        verify_user = models.admin_user.objects.filter(as_work_id=username, as_password=pwd,as_status=1)
        if not verify_user:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = username
        return self.cleaned_data

#用户注册表单验证
class RegisterForm(forms.Form):
    username = forms.CharField(min_length=2,label="学号",max_length=20,widget=forms.TextInput(attrs={'class':'form-control'}))
    s_name = forms.CharField(min_length=2,max_length=20,label="姓名",widget=forms.TextInput(attrs={'class':'form-control'}))
    s_xi = forms.CharField(min_length=2,max_length=20,label="院系",widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(min_length=2,max_length=20,label="密码",widget=forms.TextInput(attrs={'class':'form-control'}))
    password_again = forms.CharField(min_length=2,max_length=20,label="确认密码",widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(min_length=2,max_length=20,label="邮箱",widget=forms.EmailInput(attrs={'class':'form-control'}))
    s_sex = forms.ChoiceField(label="性别",choices=((0,'男'),(1,'女')))

    def clean_username(self):
        username = self.cleaned_data['username']
        verify_user = models.student_user.objects.filter(s_no=username,s_status=1)
        if verify_user:
            raise forms.ValidationError("该学号已被注册过")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        verify_user = models.student_user.objects.filter(s_email=email,s_status=1)
        if verify_user:
            raise forms.ValidationError("该邮箱已被注册过")
        return email

    def clean_password(self):
        password = self.data.get('password')
        password_again = self.data.get('password_again')
        if password != password_again:
            raise forms.ValidationError('两次输入密码不一致')
        return password_again

#公告栏添加表单验证
class NoticeForm(forms.Form):
    title = forms.CharField(min_length=2, label="公告栏标题", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(min_length=2, label="公告栏内容", max_length=2000, widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean_title(self):
        title = self.data.get('title')
        verify_title = models.notice_man.objects.filter(nm_title=title)
        if verify_title:
            raise forms.ValidationError('该公告栏已存在')
        return title

    def clean_content(self):
        content = self.data.get('content')
        verify_content = models.notice_man.objects.filter(nm_content=content)
        if verify_content:
            raise forms.ValidationError('该内容已存在')
        return content

#图书分类表单验证
class CategoryForm(forms.Form):
    id = forms.IntegerField(label="图书类别id", min_value=1,max_value=100000, widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(min_length=2, label="图书类别名称", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_name(self):
        name = self.data.get('name')
        verify_name = models.book_category.objects.filter(bc_info=name)
        if verify_name:
            raise forms.ValidationError('已存在该图书分类')
        return name

    def clean_id(self):
        id = self.data.get('id')
        verify_id = models.book_category.objects.filter(bc_id=id)
        if verify_id:
            raise forms.ValidationError('已存在该图书分类id')
        return id

#图书新增表单验证
class AddBookForm(forms.Form):
    book_id = forms.CharField(label="图书编号", min_length=2,max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_name = forms.CharField(min_length=2, label="图书名称", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_publish = forms.CharField(min_length=2, label="出版社名称", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_price = forms.FloatField( label="图书价格", widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_author = forms.CharField(label="作者", widget=forms.TextInput(attrs={'class': 'form-control'}),min_length=1,max_length=30)
    book_publish_date = forms.DateField(label="出版日期", widget=forms.DateInput(attrs={'class': 'form-control','type':'date'}))
    book_sn = forms.CharField(label="SN号", widget=forms.TextInput(attrs={'class': 'form-control'}),min_length=1,max_length=30)
    book_work_id = forms.CharField(label="书架编号", widget=forms.TextInput(attrs={'class': 'form-control'}),required=False,min_length=1,max_length=30)
    book_category = forms.ModelChoiceField(queryset=models.book_category.objects.all(),empty_label="请选择类别",label="图书分类")

    def clean_book_id(self):
        book_id = self.data.get('book_id')
        verify_id = models.book_info.objects.filter(bi_number=book_id)
        if verify_id:
            raise forms.ValidationError('图书编号已存在')
        return book_id

    def clean_book_work_id(self):
        book_work_id = self.data.get('book_work_id')
        verify_work = models.book_info.objects.filter(bi_caseid=book_work_id)
        if verify_work:
            raise forms.ValidationError("该书架已放置了图书，请选择其他的书架")
        return book_work_id


#图书新增表单验证
class AlterBookForm(forms.Form):
    book_id = forms.CharField(label="图书编号", min_length=2,max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    book_name = forms.CharField(min_length=2, label="图书名称", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_publish = forms.CharField(min_length=2, label="出版社名称", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_price = forms.FloatField( label="图书价格", widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_author = forms.CharField(label="作者", widget=forms.TextInput(attrs={'class': 'form-control'}),min_length=1,max_length=30)
    book_sn = forms.CharField(label="SN号", widget=forms.TextInput(attrs={'class': 'form-control'}),min_length=1,max_length=30)
    book_work_id = forms.CharField(label="书架编号", widget=forms.TextInput(attrs={'class': 'form-control'}),required=False,min_length=1,max_length=30)

    def clean_book_id(self):
        book_id = self.data.get('book_id')
        verify_id = models.book_info.objects.filter(bi_number=book_id)
        if verify_id:
            raise forms.ValidationError('图书编号已存在')
        return book_id

    def clean_book_work_id(self):
        book_work_id = self.data.get('book_work_id')
        verify_work = models.book_info.objects.filter(bi_caseid=book_work_id)
        if verify_work:
            raise forms.ValidationError("该书架已放置了图书，请选择其他的书架")
        return book_work_id

#图书申请表单
class ApplyBookForm(forms.Form):
    book_id = forms.CharField(label="图书名称", min_length=2,max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_name = forms.CharField(min_length=2, label="图书作者", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_publish = forms.CharField(min_length=2, label="出版社名称", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_price = forms.FloatField( label="图书价格", widget=forms.TextInput(attrs={'class': 'form-control'}))
