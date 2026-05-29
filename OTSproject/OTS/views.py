from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from OTS.models import *
import random
def welcome(request):
    template=loader.get_template('welcome.html')
    return HttpResponse(template.render())
    
def condidateRegistrationForm(request):
    res=render(request,'registration_form.html')
    return res

def candidateRegistration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')

        # ✅ Empty check
        if not username or not password or not name:
            userStatus = 4   # custom status for empty fields

        elif Candidate.objects.filter(username=username).exists():
            userStatus = 1   # already exists

        else:
            candidate = Candidate()
            candidate.username = username
            candidate.password = password
            candidate.name = name
            candidate.save()
            userStatus = 2   # success

    else:
        userStatus = 3

    return render(request, 'registration.html', {'userStatus': userStatus})       


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ✅ Check empty fields
        if not username or not password:
            loginError = "Username and Password cannot be empty"
            return render(request, 'login.html', {'loginError': loginError})

        # ✅ Check user exists
        candidate = Candidate.objects.filter(username=username, password=password)

        if len(candidate) == 0:
            return render(request, 'login.html', {
                'loginError': "Invalid Username or Password"
            })

        # ✅ Login success
        request.session['username'] = candidate[0].username
        request.session['name'] = candidate[0].name

        return HttpResponseRedirect('home')

    return render(request, 'login.html')
def candidateHome(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect("login")
    else:
         res=render(request,'home.html')
    return res

def testpaper(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect("login")
        return res
        #fetch quwstions from databases table 
    n=int(request.GET['n'])
    question_pool=list(Question.objects.all())
    random.shuffle(question_pool)
    questions_list=question_pool[:n]
    context={'questions':questions_list}
    res=render(request,'test_paper.html',context)
    return res

def calculateTestResult(request):
    if 'name' not in request.session.keys():
        return HttpResponseRedirect('login')

    total_attempt=0
    total_right=0
    total_wrong=0
    qid_list=[]
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))
    for n in qid_list:
        question=Question.objects.get(qid=n)
        try:
            if question.ans==request.POST['q'+str(n)]:
                total_right+=1
            else:
                total_wrong+=1
            total_attempt+=1
        except:   
            pass
    points=(total_right-total_wrong)/len(qid_list)*10  
    #store result in result
    result=Result()
    result.username=Candidate.objects.get(username=request.session['username']) 
    result.attempt=total_attempt
    result.right=total_right
    result.wrong=total_wrong
    result.points=points
    result.save()
    print("result saved")

    #update candiadte result
    candidate=Candidate.objects.get(username=request.session['username'])
    candidate.test_attempted+=1
    candidate.points=(candidate.points*(candidate.test_attempted-1)+points)/candidate.test_attempted  
    candidate.save()
    return HttpResponseRedirect('result')



def testresultHistory(request):
     if 'name' not in request.session.keys():
        res=HttpResponseRedirect('login')
        return res

     candidate=Candidate.objects.filter(username=request.session['username'])
     results=Result.objects.filter(username_id=candidate[0].username)
     context={'candidate':candidate[0],'results':results}  
     res=render(request,'candidate_history.html',context)
     return res 
    
def showTestResult(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect('login')
        return res
    #fetch latest result 
    result=Result.objects.filter(resultid=Result.objects.latest('resultid').resultid,username_id=request.session['username'])
    context={'results':result}    
    res=render(request,'show_result.html',context)
    return res

def logoutView(request):
    if 'name'  in request.session.keys():
        del request.session['username']
        del request.session['name']
    return HttpResponseRedirect("login")
