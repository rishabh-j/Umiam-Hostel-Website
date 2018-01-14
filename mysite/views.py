from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
# Create your views here.
from .models import Announcement,Award,About,Boarder,Doctake,Filler,Note,Messmenu,Canteenmenu
from .forms import UserForm,AboutForm,AnnouncementForm,AwardForm,DocForm,BoarderForm,FillerForm,NoteForm,MessmenuForm,CanteenmenuForm
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
from django.contrib.auth.models import User
import PyPDF2
import os
from collections import OrderedDict as od
import datetime

def aboutus(request):
    info2=About.objects.all().filter(authentication_key="secretary")
    context={'info2':info2}
    return render(request,'mysite/aboutus.html',context)



def pay(request):
    info=Doctake.objects.filter(user=request.user)
    dic={}

    ac=os.getcwd()
    b=ac+'/Umiam-Hostel-Website'
    for x in info:
        a=x.hostel
        file_name = x.doc.url
        file_name=b+file_name
        pdf_file = open(file_name)
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        cost=read_pdf.getNumPages()      
        if a in dic.keys():
            dic[a]=dic[a]+cost
        else:
            dic[a]=cost
        x.paid="yes"
        x.save()

    context={
        "dic":dic
    }
    return render(request,'mysite/confirmpayment.html',context)


def boarder(request):
    info = Boarder.objects.all()
    if request.user.is_authenticated():
        temp = Filler.objects.filter(user=request.user)
    if request.user.is_authenticated() and temp.count()==0:
        abo=About.objects.filter(user=request.user)
        for x in abo:
            abou=x.authentication_key     
        context = {
            "info": info,
            "abou" : abou
        }
    else:
        context = {
            "info": info,
         }
    return render(request, 'mysite/boarder.html', context)

def upload_file(request):
    if not request.user.is_authenticated():
        return render(request, 'mysite/login.html')
    temp = Filler.objects.filter(user=request.user)
    if temp.count()!=0:
        return redirect('/getprints/')

    else:
        form = DocForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            info = form.save(commit=False)
            info.user = request.user
            info.doc = request.FILES['doc']
            info.title = info.doc.name

            index = form.cleaned_data.get('hostel')
            info.hostel = dict(form.fields['hostel'].choices)[index]
            # file_type = info.image.url.split('.')[-1]
            # file_type = file_type.lower()
            # if file_type not in IMAGE_FILE_TYPES:
            #     context = {
            #         'info': info,
            #         'form': form,
            #         'error_message': 'Image file must be PNG, JPG, or JPEG',
            #     }
            #     return render(request, 'mysite/aboutform.html', context)
            info.save()
            return redirect('/upload/')
        context = {
            "form": form,
        }
        return render(request, 'mysite/uploadform.html', context)

def getprints(request):
    fir=Filler.objects.get(user=request.user)
    lis = Doctake.objects.filter(hostel=fir.hostel).filter(paid="yes")
    context={
        "lis":lis,
    }
    return render(request,'mysite/orders.html',context)

def deleteforprinter(request,pk):
    fir=Doctake.objects.get(id=pk)
    fir.paid="No"
    fir.save()
    return redirect('/getprints/')

def delprints(request):
    fir = Filler.objects.get(user=request.user)
    lis = Doctake.objects.filter(hostel=fir.hostel)
    for x in lis:
        x.paid="no"
        x.save()
    return redirect('/getprints/')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'mysite/login.html', context)

def index(request):
    dat = datetime.date.today()
    use = About.objects.all()
    d = {}
    for x in use:
        dat_user = x.birth_date
        if dat.day == dat_user.day and dat.month == dat_user.month:
            d[(dat.year-dat_user.year)]=x.name
    context = {
        "d" : d,
    }
    return render(request,'mysite/index.html',context)

def announcement(request):
    info1=Announcement.objects.all()
    if request.user.is_authenticated():
        temp = Filler.objects.filter(user=request.user)
    if request.user.is_authenticated() and temp.count()==0:
        abo=About.objects.filter(user=request.user)
        for x in abo:
            abou=x.authentication_key

        context={
            "info1":info1,
            "abou":abou
        }
    else:
        context = {
		  "info1": info1,
	   }
    return render(request,'mysite/announcement.html', context)

def notesupload(request):
    if not request.user.is_authenticated():
        return render(request, 'mysite/login.html')
    else:
        temp = Filler.objects.filter(user=request.user)
        if temp.count()==0 :
            form = NoteForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                info = form.save(commit=False)
                info.user = request.user
                info.material = request.FILES['material']
                info.title=info.material.name
                info.save()
                return redirect('/notes/')
            context = {
                "form": form,
            }
            return render(request, 'mysite/aboutform.html', context)
        else :
            return HttpResponse('SORRY NOTE HUB UPLOAD FEATURE NOT FOR PRINTERS!!!!!')

def award(request):
    info1=Award.objects.all()
    if request.user.is_authenticated():
        temp = Filler.objects.filter(user=request.user)
    if request.user.is_authenticated() and temp.count()==0:
        abo=About.objects.filter(user=request.user)
        for x in abo:
            abou=x.authentication_key
        
        context = {
    		"info1": info1,
            "abou" : abou
    	}
    else:
        context = {
            "info1": info1,
         }

    return render(request,'mysite/award.html', context)

def addannouncement(request):
    if not request.user.is_authenticated():
        return render(request, 'mysite/login.html')
    else:
        form = AnnouncementForm(request.POST or None)
        if form.is_valid():
            info = form.save(commit=False)
            #info.user = request.user
            info.save()
            return redirect('/announcement/')
        context = {
            "form": form,
        }
        return render(request, 'mysite/aboutform.html', context)

def addboarder(request):
    if not request.user.is_authenticated():
        return render(request, 'mysite/login.html')
    else:
        form = BoarderForm(request.POST or None)
        if form.is_valid():
            info = form.save(commit=False)
            #info.user = request.user
            info.save()
            return redirect('/boarder/')
        context = {
            "form": form,
        }
        return render(request, 'mysite/aboutform.html', context)

def addaward(request):
    if not request.user.is_authenticated():
        return render(request, 'mysite/login.html')
    else:

        form = AwardForm(request.POST or None)
        if form.is_valid():
            info = form.save(commit=False)
            #info.user = request.user
            info.save()
            return redirect('/award/')
        context = {
            "form": form,
        }
        return render(request, 'mysite/aboutform.html', context)

def deleteannouncement(request,pk):
    instance = Announcement.objects.get(id=pk)
    instance.delete()
    return redirect('/announcement/')

def deleteaward(request,pk):
    instance = Award.objects.get(id=pk)
    instance.delete()
    return redirect('/award/')

def deleteboarder(request,pk):
    instance = Boarder.objects.get(id=pk)
    instance.delete()
    return redirect('/boarder/')

def deletefile(request,pk):
    instance = Doctake.objects.get(id=pk)
    instance.doc.delete()
    instance.delete()
    return redirect('/printer/')

def del_database(request):
    files = Doctake.objects.filter(user=request.user)
    for f in files:
        f.doc.delete()
        f.delete()
    return redirect('/printer/')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/home/')
            else:
                return render(request, 'mysite/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'mysite/login.html', {'error_message': 'Invalid login'})
    return render(request, 'mysite/login.html')


def notes(request):
    if not request.user.is_authenticated():
        return render(request, 'mysite/login.html')    
    if request.method == "POST":
        search=request.POST.get('code',None)
        info=Note.objects.filter(Course_code=search)
        l = od()
        for x in info:
            use = About.objects.filter(user=x.user)
            for j in use:
                l[x]=j

        context={
            "info":info,
            'l' : l,
        }
        return render(request,'mysite/notesform.html',context)
    return render(request, 'mysite/notesform.html')

def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        # form.email = request.POST['Email']
        # form.password = request.POST['password']
        # form.username = request.POST['username']
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    #info = About.objects.filter(user=request.user)
                    return redirect('/createabout/')
    return render(request, 'mysite/registerform.html')

def registerprinter(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        # form.email = request.POST['Email']
        # form.password = request.POST['password']
        # form.username = request.POST['username']
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    #info = About.objects.filter(user=request.user)
                    return redirect('/createprinter/')
    return render(request, 'mysite/registerprinter.html')

def createabout(request):
    if not request.user.is_authenticated():
        return render(request, 'mysite/login.html')
    else:
        form = AboutForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            info = form.save(commit=False)
            info.user = request.user
            z=form.cleaned_data.get('authentication_key')
            if z=="normal":
                info.authentication_key="student"
            elif z=="secy":
                info.authentication_key="secretary"
            else :
                u = User.objects.get(username = request.user)
                u.delete()
                return redirect('/register/')
         
            info.image = request.FILES['image']
            file_type = info.image.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'info': info,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'mysite/aboutform.html', context)
            info.save()
            return redirect('/home/')
        context = {
            "form": form,
        }
        return render(request, 'mysite/aboutform.html', context)


def createprinter(request):
    if not request.user.is_authenticated():
        return render(request, 'mysite/login.html')
    else:
        form = FillerForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            info = form.save(commit=False)
            info.user = request.user
            index = form.cleaned_data.get('hostel')
            info.hostel = dict(form.fields['hostel'].choices)[index]
            info.save()
            return redirect('/home/')
        context = {
            "form": form,
        }
        return render(request, 'mysite/aboutform.html', context)        

def printer(request):
    info = Doctake.objects.all().filter(user=request.user)
    context = {
        "info" : info,
    }
    return render(request,'mysite/printer.html',context)

def upvote(request,pk):
    instance = Note.objects.get(id=pk)
    instance.votes += 1
    instance.save()
    use = About.objects.filter(user=instance.user)
    for x in use:
        x.votes += 1
        x.save()
    return redirect('/notes/')

def downvote(request,pk):
    instance = Note.objects.get(id=pk)
    instance.votes -= 1
    instance.save()
    use = About.objects.filter(user=instance.user)
    for x in use:
        x.votes -= 1
        x.save()
    return redirect('/notes/')

def messmenu(request):
    if not request.user.is_authenticated():
        info = Messmenu.objects.all()
        context = {'info': info}
        return render(request, 'mysite/messmenu.html', context)        

    fil=Filler.objects.filter(user=request.user)
    if request.user.is_authenticated() and fil.count()==0:
        abx=About.objects.filter(user=request.user)
        for x in abx:
            abo = x.authentication_key
        info=Messmenu.objects.all()
        context={'abo':abo,'info':info}
        return render(request,'mysite/messmenu.html',context)
    else:
        info = Messmenu.objects.all()
        context = {'info': info}
        return render(request, 'mysite/messmenu.html', context)

def addmessmenu(request):
    if not request.user.is_authenticated():
        return render(request, 'mysite/login.html')
    else:
        form = MessmenuForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            info = form.save(commit=False)
            info.user = request.user
            info.image = request.FILES['image']
            file_type = info.image.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'info': info,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'mysite/messmenu.html', context)
            info.save()
            return redirect('/messmenu/')
        context = {
            "form": form,
        }
        return render(request, 'mysite/aboutform.html', context)

def deletemessmenu(request,pk):
    instance = Messmenu.objects.get(id=pk)
    instance.delete()
    return redirect('/messmenu/')

def addcanteenmenu(request):
    if not request.user.is_authenticated():
        return render(request, 'mysite/login.html')
    else:
        form = CanteenmenuForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            info = form.save(commit=False)
            info.user = request.user
            info.image = request.FILES['image']
            file_type = info.image.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'info': info,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'mysite/canteenmenu.html', context)
            info.save()
            return redirect('/canteenmenu/')
        context = {
            "form": form,
        }
        return render(request, 'mysite/aboutform.html', context)

def deletecanteenmenu(request,pk):
    instance = Canteenmenu.objects.get(id=pk)
    instance.delete()
    return redirect('/canteenmenu/')

def canteenmenu(request):
    if not request.user.is_authenticated():
        info = Canteenmenu.objects.all()
        context = {'info': info}
        return render(request, 'mysite/canteenmenu.html', context)   
    
    fil=Filler.objects.filter(user=request.user)
    if request.user.is_authenticated() and fil.count()==0:
        abx=About.objects.filter(user=request.user)
        for x in abx:
            abo = x.authentication_key
        info=Canteenmenu.objects.all()
        context={'abo':abo,'info':info}
        return render(request,'mysite/canteenmenu.html',context)
    else:
        info = Canteenmenu.objects.all()
        context = {'info': info}
        return render(request, 'mysite/canteenmenu.html', context)

def blog(request):
    return render(request,'mysite/blog.html')



