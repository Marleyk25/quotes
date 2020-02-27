from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    validationErrors = User.objects.registrationValidator(request.POST)
    print(validationErrors)
    if len(validationErrors)>0:
        for key, value in validationErrors.items():
            messages.error(request, value)
        return redirect("/")
    hashedPw = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
    newuser = User.objects.create(firstName = request.POST['fname'], lastName = request.POST['lname'], 
    email = request.POST ['email'], password = hashedPw)
    request.session ['loggedInUserID'] = newuser.id 

    return redirect("/success")

def login(request):
    loginerrors = User.objects.loginValidator(request.POST)
    if len(loginerrors)>0:
        for key, value in loginerrors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        loggedinuser = User.objects.filter(email= request.POST['email'])
        loggedinuser = loggedinuser[0]
        request.session['loggedInUserID'] = loggedinuser.id
        return redirect("/quote")

def success(request):
    if 'loggedInUserID' not in request.session:
        return redirect("/")
    loggedInUser = User.objects.get(id = request.session['loggedInUserID'])
    context = {
        'loggedinuser' : loggedInUser,

    }
    return render(request, 'success.html', context) 

def quote(request):
    if 'loggedInUserID' not in request.session:
        return redirect("/")
    loggedInUser = User.objects.get(id = request.session['loggedInUserID'])
    context = {
        'loggedinuser': loggedInUser,
        'quotelist' : Quote.objects.all(),
        'allquote' :Quote.objects.exclude(favQuote = loggedInUser),
        'myfavquote': Quote.objects.filter(favQuote = loggedInUser),

    }
    return render(request,"quote.html", context) 

def addquote(request):
    quoteerrors = User.objects.quoteValidator(request.POST)
    print(quoteerrors) 
    if len(quoteerrors)>0:
        for key, value in quoteerrors.items():
            messages.error(request, value)
        return redirect("/quote")
    else:
        loggedInUser = User.objects.get(id = request.session ['loggedInUserID'])
        newquote = Quote.objects.create(quotedBy= request.POST['form_by'], quoteDesc = request.POST['form_desc'], postedBy =loggedInUser)
        return redirect("/quote")     

def favquote(request, qobjID):
    loggedInUser = User.objects.get(id = request.session ['loggedInUserID'])
    quotetoFav = Quote.objects.get(id = qobjID)
    quotetoFav.favQuote.add(loggedInUser)
    return redirect("/quote")

def removefav(request, favqobjID):
    loggedInUser = User.objects.get(id = request.session ['loggedInUserID'])
    quotetoFav = Quote.objects.get(id = favqobjID)
    quotetoFav.favQuote.remove(loggedInUser)
    return redirect("/quote")

def showuser(request, userID):
    context = {
        "user": User.objects.get(id = userID),
        "quotes":Quote.objects.filter(postedBy = userID),
        # string = Quote.objects.filter(postedBy = userID),
        # "posted":Quote.objects.get(poster = userID),
        # "poster": Quote.objects.get(id = userID, related_name='poster')
        # 'allgoing': 
    }
    return render(request, "showuser.html", context)

def showquote(request, quoteID):
    context = {
        "quoteinfo": Quote.objects.get(id = quoteID),

    }
    return render(request, "showquote.html", context)

def editquote(request,quoteid):
    loggedInUser = User.objects.get(id = request.session ['loggedInUserID'])
    editquote = Quote.objects.get(id = quoteid)
    editquote.quotedBy = request.POST['form_byedit']
    editquote.quoteDesc = request.POST['form_descedit']
    editquote.save()
    return redirect("/quote")     




def logout(request):
    request.session.clear()
    return redirect("/")
