from django.contrib import admin
from home.models import student_user,admin_user,book_info,book_category,notice_man,book_borrow_back,book_apply


class student_user_admin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('s_no', 's_name','s_pwd', 's_sex','s_xi','s_pwd','s_email','s_status','s_cell_phone')

class adminaa_user_admin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('id', 'as_work_id', 'as_username', 'as_password','as_status','as_cell_phone')


class notice_manage_admin(admin.ModelAdmin):
    list_display = ('id','nm_title','nm_content','nm_created')

class book_info_admin(admin.ModelAdmin):
    list_display = ('bi_name','bi_publish_name','bi_price','bi_author','bi_number','bi_publish_date','bi_category')

class book_category_admin(admin.ModelAdmin):
    list_display = ('bc_id','bc_info')

class notice_manage_admin(admin.ModelAdmin):
    list_display = ('id','nm_title','nm_content','nm_time_created')

class book_borrow_admin(admin.ModelAdmin):
    list_display = ('id','bb_number','bb_people','bb_state','bb_comment')

class book_applay_admin(admin.ModelAdmin):
    list_display = ('id','ba_name','ba_author','ba_publish','ba_price','ba_status')

# 注册时，在第二个参数写上 admin model
admin.site.register(student_user, student_user_admin)
admin.site.register(admin_user,adminaa_user_admin)
admin.site.register(book_info,book_info_admin)
admin.site.register(book_category,book_category_admin)
admin.site.register(notice_man,notice_manage_admin)
admin.site.register(book_borrow_back,book_borrow_admin)
admin.site.register(book_apply,book_applay_admin)
