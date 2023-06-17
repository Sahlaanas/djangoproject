from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import Account, UserOTP
from django.contrib import messages,auth
from django.core.mail import send_mail
from django.conf import settings
import random
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import authenticate, login
from . mixins import MessageHandler
from . import mixins
from .models import MobileOTP



def validateEmail( email ):
    from django.core.validators import validate_email
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False
    

def validate_name(value):
    
    if not re.match(r'^[a-zA-Z\s]*$', value):
        return 'Name should only contain alphabets and spaces'
    
    elif value.strip() == '':
        return 'Name field cannot be empty or contain only spaces' 
    else:
        return False
    

# Create your views here.



def register(request):

    """ OTP VERIFICATION """

    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            usr=Account.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                auth.login(request,usr)
                messages.success(request,f'Account is created for {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return redirect('home')
            else:
                messages.warning(request,'You Entered a wrong OTP')
                return render(request,'user_account/register.html',{'otp':True,'usr':usr})
            
        # User rigistration validation
        else:
            firstname = request.POST['firstname']    
            lastname = request.POST['lastname']  
            name = request.POST['name']
            email = request.POST['email']
            mobile = request.POST['mobile']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            
#             # null values checking
            check = [name,email,password1,password2]
            for values in check:
                if values == '':
                    context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                    messages.info(request,'some fields are empty')
                    return render(request,'user_account/register.html',context)
                else:
                    pass

            result = validate_name(name)
            if result is not False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,result)
                return render(request,'user_account/register.html',context)
            else:
                pass

            result = validateEmail(email)
            if result is False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,'Enter valid email')
                return render(request,'user_account/register.html',context)
            else:
                pass
            

            
            Pass = ValidatePassword(password1)
            if Pass is False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,'Enter Strong Password')
                return render(request,'user_account/register.html',context)
            else:
                pass
            if password1 == password2:
                if Account.objects.filter(email=email).exists():
                    messages.error(request,'Email already exist')
                    return redirect('register')
            
                elif Account.objects.filter(username=name).exists():
                    messages.error(request,'user already exist')
                    return redirect('register')
              
                elif Account.objects.filter(phone_number=mobile).exists():
                    messages.error(request,'Mobile number already registered')
                    return redirect('register')
            
                try:
                    Account.objects.get(email=email)
                except:
                    usr = Account.objects.create_user(first_name=firstname, last_name=lastname, username=name,email=email,phone_number=mobile,password=password1)
                    usr.is_active=False
                    usr.save()
                    
                    user_otp=random.randint(100000,999999)
                    UserOTP.objects.create(user=usr,otp=user_otp)
                    MobileOTP.objects.create(user=usr)
                    mess=f'Hello\t{usr.username},\nYour OTP to verify your account for beatandbase is {user_otp}\nThanks!'
                    send_mail(
                            "welcome to Lapkart Verify your Email",
                            mess,
                            settings.EMAIL_HOST_USER,
                            [usr.email],
                            fail_silently=False
                        )
                    return render(request,'user_account/register.html',{'otp':True,'usr':usr})
                else:
                    context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                    messages.error(request,'user already exist')
                    return render(request,'user_account/register.html',context)
            else:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.error(request,'password mismatch')
                return render(request,'user_account/register.html',context)
    else:
        return render(request,'user_account/register.html')

    


    
    

def signin(request):
   
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)
        
        if email == '':
            messages.info(request,'some fields is empty')
            return redirect(signin)
        elif password == '':
            messages.info(request,'some fields is empty')
            return redirect(signin)
        
        try:
            Account.objects.get(email=email)
        except:
            messages.info(request,'No account found')
            return redirect(signin)

        if Account.objects.get(email=email).is_blocked:
            messages.info(request,"Your account is blocked, Please try later")
            return redirect(signin)
       
        if user is not None:
            auth.login(request,user)
            return redirect('home')              
        else:
            messages.info(request,'credential mismatch')
            return redirect(signin)
    else:
        return render(request,'user_account/login.html')
    
    
def logout(request):
    auth.logout(request)
    return redirect('home')




def forgetpassword(request):
    if request.method == 'POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            usr=Account.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                auth.login(request,usr)
                messages.success(request,f'Now you can reset your password {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return render(request, 'user_account/resetpassword.html',{'user':usr})
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request, 'user_account/forgetpassword.html',{'otp':True,'usr':usr})
            
        # User rigistration validation
        else:
            email = request.POST.get('email')
            if Account.objects.filter(email=email).exists():
                usr = Account.objects.get(email__exact=email)
                user_otp=random.randint(1000,9999)
                UserOTP.objects.create(user=usr,otp=user_otp)
                mess=f'Hello\t{usr.username},\nYour OTP to forgot password is {user_otp}\nThanks!'
                send_mail(
                        "welcome to Beatandbase Verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [usr.email],
                        fail_silently=False
                    )
                messages.success(request, 'OTP sent to you email')
                return render(request, 'user_account/forgetpassword.html',{'otp':True,'usr':usr})

            else:
                messages.error(request, 'Account does not exist!')
                return redirect('forgetpassword')
    return render(request, 'user_account/forgetpassword.html')




def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False

    
def resetpassword(request):
    if request.method=='POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = request.POST.get('fjkha67UTAnh?"}[njkGTFCXD#A@!21^^*87ghjuguy67')
            user = Account.objects.get(id=user)
            Pass = ValidatePassword(password)
            if Pass is False:
                messages.success(request, 'Enter Strong password')
                message = 'Enter Strong password'
                return redirect('resetpassword')
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset succesfull')
            return redirect(signin)
        else:
            messages.error(request, 'Password doesnot match')
            return redirect('resetpassword')

    return render(request, 'user_account/resetpassword.html')

def mobile_login(request):
    if request.method == 'POST':
        phone_number = request.POST.get('mobile')
        c_mobile = '+91' + phone_number

        try:
            profile = MobileOTP.objects.get(user__phone_number=phone_number)
        except MobileOTP.DoesNotExist:
            return redirect(register)

        profile.mobile_otp = random.randint(1000, 9999)
        print(profile.mobile_otp, '===================')
        profile.save()
        message_handler = MessageHandler(c_mobile, profile.mobile_otp).send_otp_on_phone()
        return redirect(f'/login/otp/{profile.uid}')

    return render(request, 'user_account/mobile_otp.html')


def otp(request, uid):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = MobileOTP.objects.get(uid=uid)
        if otp == profile.mobile_otp:
            login(request,profile.user)
            return redirect('home')
        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'user_account/otp.html')

