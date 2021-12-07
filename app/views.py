from django.shortcuts import render,redirect
from .models import *
import random
from django.core.mail import send_mail

def register(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        phone=request.POST['phone']
        address=request.POST['address']
        city=request.POST['city']
        state=request.POST['state']
        country=request.POST['country']
        zipcode=request.POST['zipcode']
        if pass1==pass2:
            Register(first_name=fname,last_name=lname,email=email,password=pass1,phone=phone,address=address,city=city,state=state,country=country,zipcode=zipcode).save()
            return redirect('login')
        else:
            return render(request,'register.html',{'error':"Password do not match"})
    return render(request,'register.html')

def login(request):
    if request.method=='POST':
        email=request.POST['email']
        pass1=request.POST['pass1']
        try:
            user_info=Register.objects.get(email=email)
            if pass1==user_info.password:
                request.session['user']=email
                return redirect('home')
            else:
                return render(request,'login.html',{'error':"Invalid Password"})
        except:
            return render(request,'login.html',{'error':"Invalid Email Id"})
    return render(request,'login.html')

def logout(request):
    if 'user' in request.session:
        del request.session['user']
        return redirect('login')

def home(request):
    cat=Category.objects.all()
    slid=Slider.objects.all()
    return render(request,'index.html',{'cat':cat,'slid':slid})

def forgetpassword(request):
    if request.method=='POST':
        email_id=request.POST['email']
        otp=random.randint(11111,99999)
        user=Register.objects.get(email=email_id)
        if user is not None:
            send_mail(
                'OTP Verifications',
                f'Your OTP is {otp}.Do not share your otp with anyone.',
                'webdeveloper0153@gmail.com',
                [email_id],
            )
            request.session['otp']=otp
            request.session['user']=user.email
            return redirect('eotp')
        else:
            return render(request,'forgetpassword.html',{'error':'Invalid Email ID,Please enter registered Email'})
    else:
        return render(request,'forgetpassword.html')

    

def eotp(request):
    otp=request.session['otp']
    if request.method=='POST':
        eotp=request.POST['eotp']
        if otp==int(eotp):
            return redirect('changepassword')
        else:
            return redirect('eotp')
    else:
        return render(request,'eotp.html')

def changepassword(request):
    if request.method=='POST':
        eemail=request.session['user']
        user=Register.objects.get(email=eemail)
        if request.method=='POST':
            pass1=request.POST['pass1']
            pass2=request.POST['pass2']
            if pass1==pass2:
                user.password=pass2
                user.save()
                return redirect('login')
            else:
                return redirect('changepassword')
        else:
            return redirect('eotp')
    else:
        return render(request,'changepassword.html')

def product(request):
    cat=Category.objects.all()
    cid=request.GET.get("cid")
    request.session['catid']=cid
    prod=Product.objects.filter(category_name__id=cid)

    return render(request,'shop.html',{'cat':cat,'prod':prod})

def productdetail(request):
    pid=request.GET.get("pid")
    cat=Category.objects.all()
    catid=request.session['catid']
    prod=Product.objects.get(pk=pid)
    data=Product.objects.filter(category_name=catid)
    return render(request,'product-details.html',{'cat':cat,'prod':prod,'data':data})

def addtocart(request,id):
    cat=Category.objects.all()
    if 'user' in request.session:
        cat=Category.objects.all()
        user=request.session['user']
        user_info=Register.objects.get(email=user)
        pro=Product.objects.get(id=id)
        qty=1
        cartexist=Cart.objects.filter(prod__product_name=pro.product_name)
        if cartexist:
            return redirect('showcart')
        else:
            obj=Cart(user=user_info,prod=pro,quantity=qty,subtotal=pro.product_price,total=pro.product_price)
            obj.save()
            return redirect('showcart')
        
    else:
        return redirect('login')


def showcart(request):
    con={}
    if 'user' in request.session:
        cat=Category.objects.all()
        user=request.session['user']
        user_info=Register.objects.get(email=user)
        c1=Cart.objects.filter(user=user_info)
        list1=[]
        subtotal=0
        for i in c1:
            list1.append(i.prod.product_price)
            subtotal+=i.subtotal
        l1=sum(list1)
        c1.total=subtotal+20
        
        con['total']=subtotal+20
        con['subtotal']=subtotal
        request.session['subtotal']=subtotal
        request.session['total']=subtotal+20
        con['cart']=c1
        con['cat']=cat
        return render(request,'cart.html',con)
    else:
        return redirect('login')

        

def contact(request):
    cont=Contact.objects.all()
    cat=Category.objects.all()
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        msg=request.POST['msg']
        send_mail(
            'Welcome',
            'Message',
            'webdeveloper0153@gmail.com',
            [email],
        )
        SendMsg(name=name,email=email,msg=msg).save()
    return render(request,'contact.html',{'cont':cont,'cat':cat})

def category(request):
    cat=Category.objects.all()
    return render(request,'category.html',{'cat':cat})


def plus(request,id):
    l1=Cart.objects.get(id=id)
    totle=l1.prod.product_price
    l1.quantity+=1
    l1.subtotal=totle*l1.quantity
    l1.save()
    return redirect('showcart')

def minus(request,id):
    m1=Cart.objects.get(id=id)
    totle=m1.prod.product_price
    m1.quantity-=1
    m1.subtotal=totle*m1.quantity
    m1.save()
    return redirect('showcart')

def remove(request,id):
    m1=Cart.objects.get(id=id)
    m1.delete()
    return redirect('showcart')


def checkout(request):
    cat=Category.objects.all()
    if 'user' in request.session:
        user=request.session['user']
        user_info=Register.objects.get(email=user)
        cart=Cart.objects.filter(user=user_info)
        subtotal=request.session['subtotal']
        total=request.session['total']
        add=AddAddress.objects.filter(user=user_info)
        if request.method=='POST':
            cust_id=request.POST.get('cust_id')
            cust=AddAddress.objects.get(id=cust_id)
            list1=[]
            sub_total=0
            for i in cart:
                list1.append(i.prod.product_price)
                subtotal+=subtotal
                Order(user=user_info,prod=i.prod,address=cust,quantity=i.quantity,total=i.subtotal).save()
            return redirect('OrderConform')
        return render(request,'checkout.html',{'add':add,'cart':cart,'subtotal':subtotal,'total':total,'cat':cat})
    else:
        return redirect('login')

def myaccount(request):
    cat=Category.objects.all()
    if 'user' in request.session:
        user=request.session['user']
        user_info=Register.objects.get(email=user)
        order=Order.objects.filter(user=user_info)
    return render(request,'my-account.html',{'user_info':user_info,'cat':cat,'order':order})

def addaddress(request):
    cat=Category.objects.all()
    if 'user' in request.session:
        user=request.session['user']
        user_info=Register.objects.get(email=user)
        if request.method=='POST':
            name=request.POST['name']
            phone=request.POST['phone']
            email=request.POST['email']
            add=request.POST['add']
            city=request.POST['city']
            state=request.POST['state']
            country=request.POST['country']
            zipcode=request.POST['zipcode']

            AddAddress(user=user_info,name=name,email=email,phone=phone,add=add,city=city,state=state,country=country,zipcode=zipcode).save()
            return redirect('checkout')
        return render(request,'address.html',{'cat':cat})
    else:
        return redirect('login')

def about(request):
    cat=Category.objects.all()
    return render(request,'about.html',{'cat':cat})

def OrderConform(request):
    cat=Category.objects.all()
    if 'user' in request.session:
        user=request.session['user']
        user_info=Register.objects.get(email=user)
        c1=Cart.objects.filter(user=user_info)
        msg='Your Order has been successfully Placed'
        send_mail(
            'TITLE',
            f'{msg}',
            'webdeveloper0153@gmail.com',
            [user_info.email],
        )
        c1.delete()
    return render(request,'conformation.html',{'msg':msg,'cat':cat})

