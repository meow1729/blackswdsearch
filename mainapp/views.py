from django.shortcuts import render,get_object_or_404
from mainapp.models import Student,Comment
from django.shortcuts import redirect
import random

def lenn(text):
    to_return = 0
    for i in text:
        if i!=' ':
            to_return+=1
    return to_return

def home(request):
    # this shit may be shifted to "baseview" as it will be common to all website pages
    # OR MAYBE NOT
    recent_comments = Comment.objects.all().order_by('-created')[0:10]
    top_profiles = Student.objects.all().order_by('-views')[0:10]
    dick={'recent_comments':recent_comments,'top_profiles':top_profiles}
    dick['search_results']=[]

    if request.method =='POST':
        #1.) capture the values correctly and
        #2.) render the result accordingly
        idno = request.POST['idno']
        name = request.POST['name']
        hostel = request.POST['hostel']
        room = request.POST['room']

        sortby=request.POST['sortby']

        try:
            m=request.POST['sex1']
            m=True
        except:
            m=False

        try:
            f=request.POST['sex2']
            f=True
        except:
            f=False

        dick['idno']=idno
        dick['name']=name
        dick['hostel']=hostel
        dick['room']=room
        dick['m']=m
        dick['f']=f
        dick['sortby']=sortby



        search_results=Student.objects.all()

        # list of all Student objects will keep on filtering based on user options
        if room!='' and room.isdigit():
            search_results= search_results.filter(room=int(room))
        if hostel!='ALL':
            search_results=search_results.filter(hostel=hostel)
        if m==False:
            search_results=search_results.filter(sex=False)
        if f==False:
            search_results=search_results.filter(sex=True)

        if sortby=='popularity':
            search_results = search_results.order_by('-views')
        if sortby=='number_of_comments':
            search_results = search_results.order_by('-number_of_comments')
        if sortby=='room':
            search_results = search_results.order_by('room')

        if name!='':
            temp =[]
            for i in search_results:
                if name.lower() in i.name.lower():
                    temp.append(i)
            search_results=temp

        if idno!='':
            temp =[]
            for i in search_results:
                if idno.lower() in i.idno.lower():
                    temp.append(i)
            search_results=temp

        #print(sortby)


        '''
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        4th july, 2016
        PAGINATION on home page. my requirement is different than what's done in official docs
        (which btw can be directly implemented in profile page for comments)
        because when next button is clicked, a GET request is sent and results are only computed on post request.
        so I tried this, :-
        replacing next and previous Hyperlinks with input (type=submit)boxes and using a form with method=POST
        and action="URL" so that i can send both GET and POST request.
        for some reason it didn't work
        so I'll have to
        1.)develop custom solution from scratch(without using Paginator class)
        2.)or some more modifications on document stuff ??
        3.)or maybe some frontend solution ??
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '''

        dick['search_results']=search_results
        n=str(len(search_results))
        dick['n']=n

    # because default values should be both sexes ticked..
    if 'm' not in dick:
        dick['m']=True
    if 'f' not in dick:
        dick['f']=True


    return render(request,'home.html',dick)

# meow is something recieved from url
def profile(request,meow):
    errors=[]

    student = get_object_or_404(Student,idno=meow)
    student.views+=1
    student.save()
    #student = get_object_or_404(Student,idno=meow)

    if request.method=='POST':
        title = request.POST['title']
        content = request.POST['content']
        # verify weather what user has typed is "correct" or not, where "correct" is what I define here
        # no restrictions on db
        everything_correct=True
        if len(title)>100:
            everything_correct=False
            errors.append('length of title should be less than 100 characters')
        if lenn(title)==0:
            everything_correct=False
            errors.append('type something in the title box')
        if len(content)>10000:
            everything_correct=False
            errors.append('length of title cannot be more than 10000 characters')
        if lenn(content)==0:
            everything_correct=False
            errors.append('type something in the content box')


        if everything_correct:
            c= Comment(student=student,title=title,content=content)
            c.save()
            student.number_of_comments+=1
            student.save()
        print(len(title))


    first=''
    for i in student.name:
        if i==' ':
            break
        else:
            first+=i

    comments = Comment.objects.filter(student=student).order_by('-created')
    n=len(comments)

    recent_comments = Comment.objects.all().order_by('-created')[0:10]
    top_profiles = Student.objects.all().order_by('-views')[0:10]

    dick = {'student':student,
    'first':first,
    'comments':comments,
    'n':n,
    'errors':errors,
    'recent_comments':recent_comments,
    'top_profiles':top_profiles
    }

    return render(request,'profile.html',dick)

def about(request):
    recent_comments = Comment.objects.all().order_by('-created')[0:10]
    top_profiles = Student.objects.all().order_by('-views')[0:10]

    return render(request,'about.html',{'recent_comments':recent_comments,'top_profiles':top_profiles})

def randomm(request):
    top = list(Student.objects.all().order_by('-views')[0:100])
    std = random.choice(top)
    idd = std.idno
    return redirect('/'+idd)
