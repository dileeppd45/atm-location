from django.shortcuts import render

from django.shortcuts import render, HttpResponse, redirect
from django.db import connection
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

import os
# reg.text


def login(request):
	if request.method == "POST":
		userid = request.POST['userid']
		password = request.POST['password']
		cursor = connection.cursor()
		cursor.execute("select * from login where admin_id ='" + str(userid) + "' and password ='"+str(password)+"' ")
		data = cursor.fetchone()
		if data == None:
			cursor.execute("select * from branch where branch_id ='" + str(userid) + "' and password ='" + str(password) + "' and status ='approved' ")
			data = cursor.fetchone()
			if data == None:
				cursor.execute("select * from user_register where user_id ='" + str(userid) + "' and password ='" + str(password) + "' ")
				data = cursor.fetchone()
				if data == None:
					return HttpResponse("<script> alert('invalid id or password');window.location='../login';</script>")
				else:
					request.session['userid'] = userid
					return redirect('user_home')
			else:
				request.session['branchid'] = userid
				return redirect('branch_home')
		else:
			return redirect('admin_home')
	return render(request, 'login.html')



def signin_branch(request):
	if request.method == "POST":
		branchid = request.POST['branchid']
		name = request.POST['name']
		ifsc = request.POST['ifsc']
		start_date = request.POST['start_date']
		district = request.POST['district']
		phone = request.POST['phone']
		lat = request.POST['lat']
		long = request.POST['long']
		password = request.POST['password']
		cursor = connection.cursor()
		cursor.execute("select * from login where admin_id ='"+str(branchid)+"' ")
		data = cursor.fetchone()
		if data == None:
			cursor.execute("select * from user_register where user_id ='" + str(branchid) + "' ")
			data = cursor.fetchone()
			if data == None:
				cursor.execute("select * from branch where branch_id ='" + str(branchid) + "' ")
				data = cursor.fetchone()
				if data == None:
					cursor.execute("select * from branch where ifsc_code ='" + str(ifsc) + "' ")
					data = cursor.fetchone()
					if data == None:
						cursor.execute("insert into branch values('"+str(branchid)+"', '"+str(name)+"', '"+str(ifsc)+"', '"+str(start_date)+"', 'pending', '"+str(district)+"', '"+str(phone)+"', '"+str(password)+"','pending', '"+str(lat)+"', '"+str(long)+"')")
						return HttpResponse("<script> alert('registered branch successfully');window.location='../signin_branch';</script>")
					else:
						return HttpResponse("<script> alert('ifsc code already exist');window.location='../signin_branch';</script>")
				else:
					return HttpResponse("<script> alert('branch id already exist');window.location='../signin_branch';</script>")
			else:
				return HttpResponse("<script> alert('user id already exist');window.location='../signin_branch';</script>")
		else:
			return HttpResponse("<script> alert('id already exist');window.location='../signin_branch';</script>")
	cursor = connection.cursor()
	cursor.execute("select * from district")
	data = cursor.fetchall()
	cursor.execute("select * from bank")
	bank = cursor.fetchall()
	return render(request,'signin_branch.html',{'data':data,'bank':bank})



def signin(request):
	if request.method == "POST":
		userid = request.POST['userid']
		name = request.POST['name']
		address = request.POST['address']
		phone = request.POST['phone']
		email = request.POST['email']
		password = request.POST['password']
		cursor = connection.cursor()
		cursor.execute("select * from login where admin_id ='" + str(userid) + "' ")
		data = cursor.fetchone()
		if data == None:
			cursor.execute("select * from user_register where user_id ='" + str(userid) + "' ")
			data = cursor.fetchone()
			if data == None:
				cursor.execute("select * from branch where branch_id ='" + str(userid) + "' ")
				data = cursor.fetchone()
				if data == None:
					cursor.execute("insert into user_register values('" + str(userid) + "', '" + str(name) + "', '" + str(address) + "', '" + str(phone) + "', '" + str(email) + "', '" + str(password) + "')")
					return HttpResponse("<script> alert('registered  successfully');window.location='../signin';</script>")
				else:
					return HttpResponse("<script> alert('branch id already exist');window.location='../signin';</script>")
			else:
				return HttpResponse("<script> alert('user id already exist');window.location='../signin';</script>")
		else:
			return HttpResponse("<script> alert('id already exist');window.location='../signin';</script>")
	return render(request,'signin.html')


def home_page(request):
	return render(request, 'index.html')


def branch_home(request):
	branch = request.session['branchid']
	return render(request,'branch_home.html',{'branch': branch})

def user_home(request):
	return render(request,'user_home.html')

def admin_home(request):
	return render(request,'admin_home.html')

def approved_branches(request):
	cursor = connection.cursor()
	cursor.execute("select branch.*, bank.bank_name from branch join bank where branch.status ='approved' and branch.bank_id = bank.bankid ")
	data = cursor.fetchall()
	return render(request,'admin_approved_branches.html',{'data':data})
def admin_view_branchwise_atm(request,id):
	cursor = connection.cursor()
	cursor.execute("select * from atm where branch_id = '" + str(id) + "' ")
	data = cursor.fetchall()
	return render(request, 'admin_view_branchwise_atm.html', {'data': data,'branch':id})
def pending_branches(request):
	cursor = connection.cursor()
	cursor.execute("select * from branch where status ='pending' ")
	data = cursor.fetchall()
	return render(request,'admin_pending_branches.html',{'data':data})

def approve_branch(request,id):
	cursor = connection.cursor()
	cursor.execute("update branch set status ='approved' where branch_id ='"+str(id)+"' ")
	return redirect('pending_branches')




def add_atm(request):
	if request.method == "POST":
		branch = request.session['branchid']
		address = request.POST['address']
		lat = request.POST['lat']
		lon = request.POST['lon']
		cursor = connection.cursor()
		cursor.execute("insert into atm values(null, '"+str(branch)+"','"+str(address)+"','"+str(lat)+"', '"+str(lon)+"','closed' )")
		cursor.execute("select * from atm where branch_id ='" + str(branch) + "'")
		data = cursor.fetchall()
		data=list(data)
		atm_count =int(0)
		for i in data:
			atm_count =atm_count + 1
		cursor.execute("update branch set number_of_atm ='"+str(atm_count)+"' where branch_id ='"+str(branch)+"'")
	branch = request.session['branchid']
	return render(request, 'branch_add_atm.html',{'branch': branch})

def view_atm(request):
	branch = request.session['branchid']
	cursor = connection.cursor()
	cursor.execute("select * from atm where branch_id = '"+str(branch)+"' ")
	data = cursor.fetchall()
	return render(request, 'branch_view_atm.html',{'data':data,'branch': branch})

def open_atm(request,id):
	cursor = connection.cursor()
	cursor.execute("update atm set current_working_status ='opened' where idatm ='"+str(id)+"'")
	return redirect('view_atm')

def close_atm(request,id):
	cursor = connection.cursor()
	cursor.execute("update atm set current_working_status ='closed' where idatm ='"+str(id)+"'")
	return redirect('view_atm')


def profile(request):
	branch = request.session['branchid']
	cursor = connection.cursor()
	cursor.execute("select branch.*, bank.bank_name from branch join bank where branch.branch_id ='"+str(branch)+"' and branch.bank_id = bank.bankid")
	data = cursor.fetchone()
	return render(request, 'branch_profile.html',{'profile': data,'branch': branch})
def user_profile(request):
	user = request.session['userid']
	cursor = connection.cursor()
	cursor.execute("select * from user_register where user_id ='"+str(user)+"'")
	data = cursor.fetchone()
	return render(request, 'user_profile.html',{'profile': data,'user': user})

def change_password(request):
	branch = request.session['branchid']
	return render(request,'branch_change_password.html',{'branch': branch})
def change_password_user(request):
	user = request.session['userid']
	return render(request,'user_change_password.html',{'user': user})

def update_password(request):
	if request.method == "POST":
		id = request.POST['id']
		old = request.POST['old']
		new = request.POST['new']
		new1 = request.POST['new1']
		cursor = connection.cursor()
		cursor.execute("select * from branch where branch_id='"+str(id)+"' and password ='"+str(old)+"' ")
		data = cursor.fetchone()
		if data == None:
			return HttpResponse("<script> alert('Password Incorrect');window.location='../profile';</script>")
		else:
			if new == new1:
				if new == old:
					return HttpResponse("<script> alert('you entered same password as new please enter new password ');window.location='../profile';</script>")
				else:
					cursor.execute("update branch set password ='"+str(new)+"' where branch_id ='"+(id)+"' ")
					return HttpResponse("<script> alert('Password Updated Succesfully');window.location='../profile';</script>")

			else:
				return HttpResponse("<script> alert('New Passwords Conformed Incorrectly ');window.location='../profile';</script>")




def update_password_user(request):
	if request.method == "POST":
		id = request.POST['id']
		old = request.POST['old']
		new = request.POST['new']
		new1 = request.POST['new1']
		cursor = connection.cursor()
		cursor.execute("select * from user_register where user_id='"+str(id)+"' and password ='"+str(old)+"' ")
		data = cursor.fetchone()
		if data == None:
			return HttpResponse("<script> alert('Password Incorrect');window.location='../user_profile';</script>")
		else:
			if new == new1:
				if new == old:
					return HttpResponse("<script> alert('you entered same password as new please enter new password ');window.location='../user_profile';</script>")
				else:
					cursor.execute("update user_register set password ='"+str(new)+"' where user_id ='"+(id)+"' ")
					return HttpResponse("<script> alert('Password Updated Succesfully');window.location='../user_profile';</script>")

			else:
				return HttpResponse("<script> alert('New Passwords Conformed Incorrectly ');window.location='../user_profile';</script>")

def user_home(request):
	user = request.session['userid']
	return render(request,'user_home.html',{'user':user})

def user_view_bank(request):
	user = request.session['userid']
	cursor = connection.cursor()
	cursor.execute("select * from bank ")
	data = cursor.fetchall()
	return render(request,'user_view_bank.html',{'user': user,'data':data})

def user_view_branch(request,id):
	user = request.session['userid']
	cursor = connection.cursor()
	cursor.execute("select bank_name from bank where bankid ='"+str(id)+"' ")
	bank = cursor.fetchone()
	bank = list(bank)
	bank=bank[0]

	cursor.execute("select branch.*, bank.bank_name from branch join bank where branch.status ='approved' and branch.bank_id = bank.bankid and branch.number_of_atm != 'pending' and branch.bank_id ='"+str(id)+"' ")
	data = cursor.fetchall()
	return render(request, 'user_view_branch.html',{'user':user,'data':data,'bank':bank})

def user_view_branchwise_atm(request,id):
	user = request.session['userid']
	cursor = connection.cursor()
	cursor.execute("select * from atm where branch_id = '" + str(id) + "' ")
	data = cursor.fetchall()
	return render(request, 'user_view_branchwise_atm.html', {'data': data,'branch':id,'user':user})

def location(request,id,jd):
    return render(request,"Location.html",{'lat':id,'lon':jd})