from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django import forms
from home import forms,models
import time
import datetime
from django.db.models import Q
# Create your views here.

def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

#首页管理员视图
def index(request):
    context = {}
    context['current_time'] = get_current_time()
    user_type = request.session["user_name"]
    context['user_type'] = user_type
    return render(request,'index.html',context)

#读者信息
def user_info(request):
    context = {}
    context['current_time'] = get_current_time()
    user_name = request.session["user_name"]
    user_info = models.student_user.objects.filter(s_no=user_name).values('s_name','s_sex','s_xi','s_time_created','s_no','s_email','s_borrow_count','s_cell_phone')
    user_display = user_info[0]['s_name']
    s_cell_phone = user_info[0]['s_cell_phone']
    s_email = user_info[0]['s_email']
    s_xi = user_info[0]['s_xi']
    s_time_created = user_info[0]['s_time_created']
    if request.method == 'POST':
        xi = request.POST.get("xi")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        models.student_user.objects.filter(s_no=user_name).update(s_xi=xi,s_email=email,s_cell_phone=mobile)
        return redirect('user_index')
    context['user_name'] = user_name
    context['user_display'] = user_display
    context['mobile'] = s_cell_phone
    context['email'] = s_email
    context['xi'] = s_xi
    context['register_time'] = s_time_created
    return render(request, 'user_info.html', context)

#首页读者视图
def user_index(request):
    context = {}
    context['current_time'] = get_current_time()
    user_name = request.session["user_name"]
    context['user_name'] = user_name
    return render(request,'user_index.html',context)

#读者注册视图
def register(request):
    context = {}
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.data.get('username')
            s_name = register_form.data.get('s_name')
            s_xi = register_form.data.get('s_xi')
            password = register_form.data.get('password')
            email = register_form.data.get('email')
            s_sex = register_form.data.get('s_sex')
            models.student_user.objects.create(s_no=username, s_name=s_name, s_sex=s_sex,s_xi=s_xi,s_pwd=password, s_email=email)
            return redirect('index.html')
    else:
        register_form = forms.RegisterForm()
    context['register_form'] = register_form
    return render(request,'register.html',context)

#管理员登录视图
def admin_login(request):
    if request.method == 'POST':
        admin_login_form = forms.AdminLoginForm(request.POST)
        if admin_login_form.is_valid():
            return redirect('index.html')
    else:
        admin_login_form = forms.AdminLoginForm()
    context = {}
    context['admin_login_form'] = admin_login_form
    return render(request,'admin_login.html',context)

#读者登录视图
def login(request):
    if request.method == 'POST':
        login_form = forms.UserLoginForm(request.POST)
        if login_form.is_valid():
            request.session['user_type']= 1
            request.session['user_name']= login_form.cleaned_data['username']
            return redirect('user_index.html')
    else:
        login_form = forms.UserLoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request,'login.html',context)

def delete_user(request):
    return HttpResponse("删除用户")

def update_user(request):
    return render(request,'update_user.html')

#读者列表视图
def user_list(request):
    key=request.GET.get("search_keys")
    if key:
        user_list = models.student_user.objects.values('s_no','s_name','s_status','s_email','s_xi').filter(Q(s_no=key)|Q(s_name=key))
    else:
        try:
            user_list = models.student_user.objects.values('s_no','s_name','s_status','s_email','s_xi')
        except Exception as e:
            user_list = {}
    context = {}
    context['current_time'] = get_current_time()
    context['user_list'] = user_list
    if user_list:
        for l in user_list:
            if l.get('s_status') == 1:
                l['s_status'] = '正常'
            elif l.get("s_status") == 2:
                l['s_status'] ='已禁用'
    return render(request,'user_list.html',context)

#读者详情
def user_detail(request,s_no):
    try:
        user_detail = models.student_user.objects.values('s_name','s_sex','s_xi','s_status','s_no','s_email','s_borrow_count','s_cell_phone','s_time_created').get(s_no=s_no)
    except Exception as e:
        user_detail = {}
    context={}
    context['user_detail']= user_detail
    if user_detail:
        if user_detail.get('s_status') == 1:
            user_detail['s_status'] = '正常'
        elif user_detail.get("s_status") == 2:
            user_detail['s_status'] = '已禁用'
        if user_detail.get('s_sex') == 0:
            user_detail['s_sex'] = '男'
        elif user_detail.get('s_sex') == 1:
            user_detail['s_sex'] = '女'
    return render(request,'user_detail.html',context)

#管理员重置读者密码
def reset_pwd(request,s_no):
    models.student_user.objects.filter(s_no=s_no).update(s_pwd="123456")
    return redirect("user_list")

#管理员更新读者账号正常
def account_normal(request,s_no):
    models.student_user.objects.filter(s_no=s_no).update(s_status=1)
    return redirect("user_list")

#管理员更新读者账号禁用
def account_unnormal(request,s_no):
    models.student_user.objects.filter(s_no=s_no).update(s_status=2)
    return redirect("user_list")

#图书列表视图
def book_list(request):
    key = request.GET.get("search_keys")
    if key:
        book_list = models.book_info.objects.values('bi_number', 'bi_name', 'bi_publish_name', 'bi_price', 'bi_author',
                                                    'bi_publish_date', 'bi_category', 'bi_sn_number', 'bi_status',
                                                    'bi_state').filter(
            Q(bi_number=key) | Q(bi_name=key))
        # borrow_list = models.book_borrow_back.objects.values('bb_number', 'bb_people', 'bb_borrow_date', 'bb_back_date', 'bb_comment','bb_state').filter(Q(bb_number=key) | Q(bb_people=key))
    else:
        try:
            book_list = models.book_info.objects.values('bi_number', 'bi_name', 'bi_publish_name', 'bi_price', 'bi_author','bi_publish_date','bi_category','bi_sn_number','bi_status','bi_state')

            # borrow_list = models.book_borrow_back.objects.values('bb_number', 'bb_people', 'bb_borrow_date', 'bb_back_date', 'bb_comment','bb_state')
        except Exception as e:
            borrow_list = {}
    context = {}
    context['current_time'] = get_current_time()
    context['book_list'] = book_list
    if book_list:
        for l in book_list:
            if l.get('bi_status') == 1:
                l['bi_status'] = '正常'
            elif l.get("bi_status") == 2:
                l['bi_status'] = '已损坏'
            if l.get('bi_state') == 0:
                l['bi_state'] = '不在馆'
            elif l.get('bi_state') ==1:
                l['bi_state'] = '在馆'
    return render(request, 'book_list.html', context)

#读者借书列表视图
def user_book_list(request):
    key = request.GET.get("search_keys")
    if key:
        book_list = models.book_info.objects.values('bi_number', 'bi_name', 'bi_publish_name', 'bi_price', 'bi_author','bi_publish_date','bi_category','bi_sn_number','bi_status','bi_state').filter(
                Q(bi_number=key) | Q(bi_name=key))
    else:
        try:
            book_list = models.book_info.objects.values('bi_number', 'bi_name', 'bi_publish_name', 'bi_price', 'bi_author','bi_publish_date','bi_category','bi_sn_number','bi_status','bi_state')
        except Exception as e:
            book_list = {}
    context = {}
    context['current_time'] = get_current_time()
    context['book_list'] = book_list
    if book_list:
        for l in book_list:
            if l.get('bi_status') == 1:
                l['bi_status'] = '正常'
            elif l.get("bi_status") == 2:
                l['bi_status'] = '已损坏'
            if l.get('bi_state') == 0:
                l['bi_state'] = '不在馆'
            elif l.get('bi_state') ==1:
                l['bi_state'] = '在馆'
            #书能借的条件1-正常 2-在馆 3-状态显示为0或2
            status=models.book_borrow_back.objects.filter(Q(bb_number=l.get('bi_number'),bb_state=1)|Q(bb_number=l.get('bi_number'),bb_state=3)|Q(bb_number=l.get('bi_number'),bb_state=0)|Q(bb_number=l.get('bi_number'),bb_state=4))
            if l.get('bi_status') == '正常' and l.get('bi_state') =='在馆' and not status:
                l['borrow_status'] =1
            else:
                l['borrow_status'] =0
    return render(request, 'user_book_list.html', context)

#读者申请借书
def user_borrow(request,book_id):
    user_name = request.session["user_name"]
    end_date = datetime.datetime.now()+datetime.timedelta(days=10)
    models.book_borrow_back.objects.create(bb_number=book_id,bb_people=user_name,bb_back_date=end_date,bb_state=4)
    return redirect('user_book_list')

#管理员审核借书
def borrow_list(request):
    key = request.GET.get("search_keys")
    if key:
        borrow_list = models.book_borrow_back.objects.values('id','bb_number', 'bb_people', 'bb_borrow_date', 'bb_back_date', 'bb_comment','bb_state').filter(Q(bb_number=key) | Q(bb_people=key))
    else:
        try:
            borrow_list = models.book_borrow_back.objects.values('id','bb_number', 'bb_people', 'bb_borrow_date', 'bb_back_date', 'bb_comment','bb_state')
        except Exception as e:
            borrow_list = {}
    context = {}
    context['current_time'] = get_current_time()
    context['borrow_list'] = borrow_list
    if borrow_list:
        for l in borrow_list:
            if l.get('bb_state') == 0:
                l['bb_state'] = '待借阅'
            elif l.get("bb_state") == 1:
                l['bb_state'] = '借阅中'
            elif l.get('bb_state') == 2:
                l['bb_state'] = '已归还'
            elif l.get('bb_state') == 3:
                l['bb_state'] = '续借'
            elif l.get('bb_state') == 4:
                l['bb_state'] = '申请中'
            #只有待借阅的有确认借书
    return render(request, 'borrow_list.html', context)

#读者借阅历史
def book_history(request):
    context = {}
    context['current_time'] = get_current_time()
    user_name = request.session["user_name"]
    history=models.book_borrow_back.objects.filter(bb_people=user_name).values('id','bb_number','bb_borrow_date','bb_back_date','bb_comment','bb_state','frequency')
    context['history']=history
    if history:
        for l in history:
            if l.get('bb_state') == 0:
                l['bb_state'] = '待借阅'
            elif l.get("bb_state") == 1:
                l['bb_state'] = '借阅中'
            elif l.get('bb_state') == 2:
                l['bb_state'] = '已归还'
            elif l.get('bb_state') == 3:
                l['bb_state'] = '续借'
            elif l.get('bb_state') == 4:
                l['bb_state'] = '申请中'
            book_name=models.book_info.objects.filter(bi_number=l.get('bb_number')).values('bi_name')[0]['bi_name']
            l['book_name']=book_name
    return render(request,'book_history.html',context)

#读者申请续借
def delay_book(request,book_id):
    #更改应还日期+10,续借次数为1，状态为续借
    date=models.book_borrow_back.objects.filter(id=book_id).values('bb_back_date')
    back_time =datetime.timedelta(days=10)+date[0]['bb_back_date']
    models.book_borrow_back.objects.filter(id=book_id).update(bb_back_date=back_time,frequency=1,bb_state=3)
    return redirect('book_history')

#管理员确认借书
def borrow_book(request,book_id):
    #1.更改借书的状态为1
    #2.更改图书的状态为不在馆
    models.book_borrow_back.objects.filter(bb_number=book_id,bb_state=4).update(bb_state=1)
    models.book_info.objects.filter(bi_number=book_id).update(bi_state=0)
    return redirect('borrow_list')

#管理员确认还书
def back_book(request,borrow_id):
    # 1.更改借书的状态为2
    # 2.更改图书的状态为在馆
    models.book_borrow_back.objects.filter(id=borrow_id).update(bb_state=2)
    book_id = models.book_borrow_back.objects.filter(id=borrow_id).values('bb_number')[0]['bb_number']
    models.book_info.objects.filter(bi_number=book_id).update(bi_state=1)
    return redirect('borrow_list')

#新增图书
def add_book(request):
    context = {}
    context['current_time'] = get_current_time()
    if request.method == 'POST':
        add_book_form = forms.AddBookForm(request.POST)
        if add_book_form.is_valid():
            book_id = add_book_form.data.get('book_id')
            book_name = add_book_form.data.get('book_name')
            book_publish = add_book_form.data.get('book_publish')
            book_price = add_book_form.data.get('book_price')
            book_author = add_book_form.data.get('book_author')
            book_publish_date = add_book_form.data.get('book_publish_date')
            book_sn = add_book_form.data.get('book_sn')
            book_work_id = add_book_form.data.get('book_work_id')
            book_category = add_book_form.data.get('book_category')
            book_category_id = models.book_category(models.book_category.objects.filter(bc_id=book_category).values('bc_id'))
            models.book_info.objects.create(bi_number=book_id, bi_name=book_name,bi_publish_name=book_publish,bi_price=book_price,bi_author=book_author,bi_publish_date=book_publish_date,bi_category=book_category_id,bi_caseid=book_work_id,bi_sn_number=book_sn)
            return redirect('book_list')
    else:
        add_book_form = forms.AddBookForm()
    context['add_book_form'] = add_book_form
    return render(request,'add_book.html',context)

#图书详情
def book_detail(request,binumber):
    book_detail = models.book_info.objects.values('bi_number', 'bi_name', 'bi_publish_name', 'bi_price', 'bi_author',
                                                'bi_publish_date', 'bi_category', 'bi_sn_number', 'bi_status','bi_caseid',
                                                'bi_time_created','bi_state').filter(bi_number=binumber)
    context = {}
    context['current_time'] = get_current_time()
    context['book_detail'] = book_detail
    if book_detail:
        for l in book_detail:
            if l.get('bi_status') == 1:
                l['bi_status'] = '正常'
            elif l.get("bi_status") == 2:
                l['bi_status'] = '已损坏'
            if l.get('bi_state') == 0:
                l['bi_state'] = '不在馆'
            elif l.get('bi_state') == 1:
                l['bi_state'] = '在馆'
            bc_info = models.book_category.objects.filter(bc_id=l.get('bi_category')).values('bc_info')[0]['bc_info']
            l['bi_category'] = bc_info
    return render(request,'book_detail.html',context)

#修改图书
def modify_book(request,binumber):
    context ={}
    context['current_time'] = get_current_time()
    context['id']=binumber
    result=models.book_info.objects.values('bi_name', 'bi_publish_name', 'bi_price', 'bi_author',
                                                'bi_publish_date', 'bi_category', 'bi_sn_number', 'bi_status','bi_caseid',
                                                'bi_time_created','bi_state').filter(bi_number=binumber)
    context['bi_name']=result[0]['bi_name']
    context['bi_publish_name']=result[0]['bi_publish_name']
    context['bi_price']=result[0]['bi_price']
    context['bi_author']=result[0]['bi_author']
    context['bi_sn_number']=result[0]['bi_sn_number']
    context['bi_caseid']=result[0]['bi_caseid']
    context['bi_status']=result[0]['bi_status']
    if request.method == 'POST':
        category_form = forms.AlterBookForm(request.POST)
        if category_form.is_valid():
            book_name = request.POST.get("book_name")
            book_publish = request.POST.get("book_publish")
            book_price = request.POST.get("book_price")
            book_author = request.POST.get("book_author")
            book_sn = request.POST.get("book_sn")
            book_work_id = request.POST.get("book_work_id")
            bi_status = request.POST.get("bi_status")
            book_state = request.POST.get("book_state")
            models.book_info.objects.filter(bi_number=binumber).update(bi_name=book_name,bi_publish_name=book_publish,bi_price=book_price,bi_author=book_author,
                                                                       bi_sn_number=book_sn,bi_caseid=book_work_id,bi_status=int(bi_status),bi_state=int(book_state))
            return redirect('book_list')
        else:
            category_form.add_error(None,"错误")
    else:
        category_form = forms.AlterBookForm()
    context['category_form']=category_form
    return render(request,'alter_book.html',context)


#图书分类列表
def category_list(request):
    key = request.GET.get("search_keys")
    if key:
        category_list = models.book_category.objects.values('bc_id', 'bc_info').filter(bc_info=key)
    else:
        try:
            category_list = models.book_category.objects.values('bc_id', 'bc_info').order_by('-bc_id')
        except Exception as e:
            category_list = {}
    context = {}
    context['current_time'] = get_current_time()
    context['category_list'] = category_list
    return render(request,'category_list.html',context)

#新增图书分类
def add_category(request):
    context = {}
    context['current_time'] = get_current_time()
    if request.method == 'POST':
        category_form = forms.CategoryForm(request.POST)
        if category_form.is_valid():
            id = category_form.data.get('id')
            name = category_form.data.get('name')
            models.book_category.objects.create(bc_id=id, bc_info=name)
            return redirect('category_list')
    else:
        category_form = forms.CategoryForm()
    context['category_form'] = category_form
    return render(request,'add_category.html',context)

#删除图书分类
def del_category(request,id):
    models.book_category.objects.filter(bc_id=id).delete()
    return redirect('category_list')

#修改图书分类
def alter_category(request,id):
    context ={}
    context['current_time'] = get_current_time()
    context['id']=id
    context['title']=models.book_category.objects.values('bc_info').filter(bc_id=id)[0]['bc_info']
    if request.method == 'POST':
        category_form = forms.CategoryForm(request.POST)
        name = request.POST.get("name")
        models.book_category.objects.filter(bc_id=id).update(bc_info=name)
        return redirect('category_list')
    else:
        category_form = forms.CategoryForm()
    context['category_form']=category_form
    return render(request,'alter_category.html',context)

#公告栏列表视图
def notice_list(request):
    try:
        notice_list = models.notice_man.objects.values('nm_title','nm_time_created','id').order_by('-id')
    except Exception as e:
        notice_list = []
    context = {}
    context['current_time'] = get_current_time()
    context['notice_list'] = notice_list
    return render(request,'notice_list.html',context)

#公告栏详细信息
def notice_detail(request,id):
    notice_detail = models.notice_man.objects.values('id','nm_title','nm_content','nm_time_created').filter(id=id)
    context = {}
    context['current_time'] = get_current_time()
    context['notice_detail'] = notice_detail
    return render(request,'notice_detail.html',context)

#公告栏发布视图
def add_notice(request):
    context = {}
    context['current_time'] = get_current_time()
    if request.method == 'POST':
        notice_form = forms.NoticeForm(request.POST)
        if notice_form.is_valid():
            nm_title = notice_form.data.get('title')
            content = notice_form.data.get('content')
            models.notice_man.objects.create(nm_title=nm_title, nm_content=content)
            return redirect('notice_list')
    else:
        notice_form = forms.NoticeForm()
    context['notice_form'] = notice_form
    return render(request,'add_notice.html',context)

#删除公告
def delete_notice(request,id):
    context = {}
    models.notice_man.objects.filter(id=id).delete()
    return redirect('notice_list')



