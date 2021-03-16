from django.db import models

# Create your models here.
#学生用户表
class student_user(models.Model):
    s_no=models.CharField(max_length=18,verbose_name="学号",primary_key=True)
    s_name=models.CharField(max_length=20,verbose_name="姓名")
    s_sex=models.IntegerField(default=0,verbose_name="性别 0男 1女")
    s_xi=models.CharField(max_length=30,verbose_name="院系")
    s_pwd=models.CharField(max_length=12,verbose_name="密码")
    s_email=models.CharField(max_length=50,verbose_name="邮箱")
    s_borrow_count=models.IntegerField(default=0,verbose_name="借书数量,最多不能超过10")
    s_status=models.IntegerField(default=1,verbose_name="状态 1正常 2禁用")
    s_cell_phone=models.CharField(max_length=11,verbose_name="读者联系电话",blank=False)
    s_time_created=models.DateTimeField(auto_now=True,verbose_name="读者注册时间")

    def __str__(self):
        return self.s_name+'--'+self.s_no

    class Meta:
        verbose_name = "读者管理"
        verbose_name_plural = verbose_name


#管理员用户表
class admin_user(models.Model):
    as_work_id=models.CharField(max_length=20,verbose_name="工作证号")
    as_username=models.CharField(max_length=11,verbose_name="姓名")
    as_password=models.CharField(max_length=20,verbose_name="密码")
    as_cell_phone=models.CharField(max_length=11,verbose_name="联系电话")
    as_status=models.IntegerField(default=1,verbose_name="状态 1正常 2禁用")

    def __str__(self):
        return self.as_username

    class Meta:
        verbose_name="管理员用户管理"
        verbose_name_plural = verbose_name

#公告栏列表
class notice_man(models.Model):
    nm_title=models.CharField(max_length=50,verbose_name="公告标题")
    nm_content=models.CharField(max_length=2000,verbose_name="公告内容")
    nm_time_created=models.DateTimeField(auto_now=True,verbose_name="发布时间")

    def __str__(self):
        return self.nm_title

    class Meta:
        verbose_name="公告管理"
        verbose_name_plural = verbose_name

#图书分类表
class book_category(models.Model):
    bc_id = models.IntegerField(verbose_name="图书分类id",primary_key=True)
    bc_info = models.CharField(verbose_name="图书分类描述",max_length=20)

    def __str__(self):
        return self.bc_info

    class Meta:
        verbose_name = "图书分类管理"
        verbose_name_plural = verbose_name

#图书信息表
class book_info(models.Model):
    bi_number = models.CharField(max_length=20,verbose_name="图书编号",primary_key=True)
    bi_name = models.CharField(max_length=100,verbose_name='图书名称')
    bi_publish_name = models.CharField(max_length=30,verbose_name='出版社名称')
    bi_price = models.DecimalField(max_digits=10,decimal_places=1,verbose_name="图书价格")
    bi_author = models.CharField(max_length=10,verbose_name="作者")
    bi_publish_date = models.DateField(verbose_name="出版日期")
    bi_category = models.ForeignKey(book_category,on_delete=models.CASCADE,verbose_name="类别")
    bi_sn_number = models.CharField(max_length=30,verbose_name="SN号")
    bi_status = models.IntegerField(default=1,verbose_name="图书状态：1-正常 2-损坏")
    bi_caseid = models.CharField(max_length=20,verbose_name="书架编号",blank=False)
    bi_time_created = models.DateTimeField(verbose_name="入馆时间",auto_now=True)
    bi_state = models.IntegerField(default=1,verbose_name="是否借出 0不在馆 1在馆")

    class Meta:
        verbose_name = "图书信息管理"
        verbose_name_plural = verbose_name

#图书借阅表记录
class book_borrow_back(models.Model):
    bb_number = models.CharField(max_length=20, verbose_name="图书编号")
    bb_people = models.CharField(max_length=20,verbose_name="借用人学号")
    bb_borrow_date = models.DateTimeField(verbose_name="借书日期")
    bb_back_date = models.DateTimeField(max_length=20,verbose_name="还书日期")
    bb_state = models.IntegerField(default=1,verbose_name="借书状态:0-待借阅 1-正在借阅 2-已归还  3-续借")
    bb_comment = models.CharField(max_length=200,verbose_name="备注")

    class Meta:
        verbose_name = "图书借阅管理"
        verbose_name_plural = verbose_name

