
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^user_index', views.user_index, name='user_index'),
    url(r'^user_info', views.user_info, name='user_info'),

    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^admin_login', views.admin_login, name='admin_login'),
    url(r'^register', views.register, name='register'),

    url(r'^user_list', views.user_list, name='user_list'),
    url(r'^user_detail/(?P<s_no>\d+)/$', views.user_detail, name='user_detail'),
    url(r'^reset_pwd/(?P<s_no>\d+)/$', views.reset_pwd, name='reset_pwd'),
    url(r'^account_normal/(?P<s_no>\d+)/$', views.account_normal, name='account_normal'),
    url(r'^account_unnormal/(?P<s_no>\d+)/$', views.account_unnormal, name='account_unnormal'),
    url(r'^delete_user', views.delete_user, name='delete_user'),
    url(r'^update_user', views.update_user, name='update_user'),

    url(r'^book_list', views.book_list, name='book_list'),
    url(r'^book_history', views.book_history, name='book_history'),
    url(r'^borrow_list', views.borrow_list, name='borrow_list'),
    url(r'^user_book_list', views.user_book_list, name='user_book_list'),
    url(r'^send_email', views.send_email, name='send_email'),
    url(r'^notify_user', views.notify_user, name='notify_user'),
    url(r'^refuse_user', views.refuse_user, name='refuse_user'),
    url(r'^user_apply_list', views.user_apply_list, name='user_apply_list'),
    url(r'^cancel_apply/(?P<id>\d+)/$', views.cancel_apply, name='cancel_apply'),
    url(r'^alter_apply_status/(?P<id>\d+)/$', views.alter_apply_status, name='alter_apply_status'),
    url(r'^purchase', views.purchase, name='purchase'),
    url(r'^user_borrow/(?P<book_id>\d+)/$', views.user_borrow, name='user_borrow'),
    url(r'^add_book', views.add_book, name='add_book'),
    url(r'^add_apply', views.add_apply, name='add_apply'),
    url(r'^book_detail/(?P<binumber>\d+)/$', views.book_detail, name='book_detail'),
    url(r'^borrow_book/(?P<book_id>\d+)/$', views.borrow_book, name='borrow_book'),
    url(r'^delay_book/(?P<book_id>\d+)/$', views.delay_book, name='delay_book'),
    url(r'^back_book/(?P<borrow_id>\d+)/$', views.back_book, name='back_book'),
    url(r'^modify_book/(?P<binumber>\d+)/$', views.modify_book, name='modify_book'),

    url(r'^category_list', views.category_list, name='category_list'),
    url(r'^add_category', views.add_category, name='add_category'),
    url(r'^del_category/(?P<id>\d+)/$', views.del_category, name='del_category'),
    url(r'^alter_category/(?P<id>\d+)/$', views.alter_category, name='alter_category'),

    url(r'^notice_list', views.notice_list, name='notice_list'),
    url(r'^user_notice', views.user_notice, name='user_notice'),
    url(r'^notice_detail/(?P<id>\d+)/$', views.notice_detail, name='notice_detail'),
    url(r'^add_notice', views.add_notice, name='add_notice'),
    url(r'^delete_notice/(?P<id>\d+)/$', views.delete_notice, name='delete_notice'),
]