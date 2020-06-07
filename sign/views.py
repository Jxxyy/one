from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render, get_object_or_404



#auth存放用户数据
# Create your views here.
def index(request):   #request参数代表客户端浏览器向服务器请求的一个信息字符串
    return render(request,"index.html")

#登录动作
def login_action(request): 
	if request.method == 'POST':
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		user = auth.authenticate(username=username,password=password) #authenticate方法验证账号密码，匹配的情况返回一个user对象，否则返回none
		if user is not None:
			auth.login(request,user) #登录
			response = HttpResponseRedirect('/event_manage/')
			#response.set_cookie('user',username,3600)  #增加浏览器cookie
			request.session['user'] = username  #将session信息记录到浏览器
			return response
		else:
			return render(request,'index.html',{'error':'username or password error!'})
#发布会管理
@login_required   #登录才可访问页面
def event_manage(request):
	#username = request.COOKIES.get('user','') #读取浏览器cookie
	event_list = Event.objects.all()
	username = request.session.get('user','') #读取浏览器session
	return render(request,"event_manage.html",{"user":username,"events":event_list})

#发布会名称搜索
@login_required
def search_name(request):
	username = request.session.get('user','')
	search_name = request.GET.get('name','')
	event_list = Event.objects.filter(name__contains=search_name)   #两个下划线表示模糊查询
	return render(request,"event_manage.html",{"user":username,"events":event_list})

#嘉宾管理
@login_required
def guest_manage(request):
	username = request.session.get('user','')
	guest_list = Guest.objects.all()     #查询全部数据
	paginator = Paginator(guest_list,2)  #每页显示两条数据
	page = request.GET.get('page')   #显示第几页数据
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		contacts = paginator.page(1)
	except Examples:
		contacts = paginator.page(paginator.num_pages)  #显示最后一页
	return render(request,"guest_manage.html",{"user":username,"guests":contacts})

#签到页面
@login_required
def sign_index(request, event_id):    #第二个参数接收url路径的参数
	event = get_object_or_404(Event, id=event_id)
	signnum = Guest.objects.filter(event_id = event_id,sign= 1).count()  #统计已签到的人数
	return render(request, 'sign_index.html', {'event':event,'signnum':signnum})

# 签到动作
@login_required
def sign_index_action(request,event_id):
	event = get_object_or_404(Event, id=event_id)
	phone = request.POST.get('phone','')
	result = Guest.objects.filter(phone = phone)
	if not result:
		render(request, 'sign_index.html', {'event': event,'hint': 'phone error.'})
	result = Guest.objects.filter(phone=phone,event_id=event_id)
	if not result:
		return render(request, 'sign_index.html', {'event': event,'hint': 'event id or phone error.'})
	result = Guest.objects.get(phone=phone,event_id=event_id)
	if result.sign:
		return render(request, 'sign_index.html', {'event': event,'hint': "user has sign in."})
	else:
		Guest.objects.filter(phone=phone,event_id=event_id).update(sign = '1')
		return render(request, 'sign_index.html', {'event': event,'hint':'sign in success!','guest': result})

#退出系统
@login_required
def logout(request):
	auth.logout(request) #退出登录
	response = HttpResponseRedirect('/index/')
	return response

