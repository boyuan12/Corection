from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import MCOption, MCQuestion, Course, Standard
from django.contrib import messages
from helpers import upload_image
import base64


# Create your views here.
def create_course(request):
    if request.method == "POST":
        course_name = request.POST["name"]
        course = Course.objects.create(name=course_name, user=request.user)
        return redirect(f"/course/{course.id}")

    else:
        return render(request, "dashboard/create-course.html")
    

def create_standard(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == "POST":
        short_name = request.POST["short"]
        long_name = request.POST["long"]
        Standard.objects.create(course=course, short_name=short_name, long_name=long_name)
        return redirect(f"/course/{course.id}")
    
    else:
        return render(request, "dashboard/create-standard.html", {
            "course": course
        })

def dashboard(request):
    courses = Course.objects.filter(user=request.user)
    return render(request, "dashboard/dashboard.html", {
        "courses": courses
    })

def course(request, course_id):
    course = Course.objects.get(user=request.user, id=course_id)
    standards = Standard.objects.filter(course=course)
    return render(request, "dashboard/course.html", {
        "course": course,
        "standards": standards
    })

def add_question_view(request, course_id):
    course = Course.objects.get(user=request.user, id=course_id)
    standards = Standard.objects.filter(course=course)
    
    if request.method == "POST":

        if len(request.FILES) != 0:
            url = upload_image(base64.b64encode(request.FILES["image"].file.read()).decode('utf-8'))
            question = MCQuestion.objects.create(course=course, question=request.POST["question"], image_url=url)
        else:
            question = MCQuestion.objects.create(course=course, question=request.POST["question"])

        for short_name in request.POST.getlist("standard"):
            question.standards.add(Standard.objects.get(course=course, short_name=short_name))
            question.save()

        for opt in ['a', 'b', 'c', 'd', 'e']:
            if opt in request.POST.getlist("correct"):
                opt = MCOption.objects.create(text=request.POST[f"opt-{opt}-val"], is_correct=True)
            else:
                opt = MCOption.objects.create(text=request.POST[f"opt-{opt}-val"], is_correct=False)
            
            print(opt)
            question.choices.add(opt)
            question.save()

        messages.add_message(request, messages.SUCCESS, "Question created successfully")
        return redirect(f"/course/{course.id}/add-question")
    else:
        return render(request, "dashboard/add-question.html", {
            "standards": standards
        })

def view_questions_by_standard(request, course_id, standard_id):
    course = Course.objects.get(id=course_id)
    standard = Standard.objects.get(id=standard_id)
    questions = MCQuestion.objects.filter(standards__in=[standard], course=course)
    print(questions)

    for question in questions:
        for choice in question.choices.all():
            print(choice)
        
    return render(request, "dashboard/view-questions.html", {
        "questions": questions,
        "course": course,
        "standard": standard
    })

def edit_question(request, course_id, question_id):
    course = Course.objects.get(id=course_id)
    standards = Standard.objects.filter(course=course)
    question = MCQuestion.objects.get(course=course, id=question_id)
    
    if request.method == "POST":

        question.question = request.POST["question"]
        if len(request.FILES) != 0:
            url = upload_image(base64.b64encode(request.FILES["image"].file.read()).decode('utf-8'))
            question.image_url = url
        
        question.standards.clear()

        for short_name in request.POST.getlist("standard"):
            question.standards.add(Standard.objects.get(course=course, short_name=short_name))

        question.choices.clear()

        for opt in ['a', 'b', 'c', 'd', 'e']:
            if opt in request.POST.getlist("correct"):
                opt = MCOption.objects.create(text=request.POST[f"opt-{opt}-val"], is_correct=True)
            else:
                opt = MCOption.objects.create(text=request.POST[f"opt-{opt}-val"], is_correct=False)
            
            question.choices.add(opt)
        
        question.save()

        messages.add_message(request, messages.SUCCESS, "Question edited successfully")
        return redirect(f"/course/{course.id}/edit-question/{question.id}")
    else:

        return render(request, "dashboard/edit-question.html", {
            "standards": standards,
            "question": question,
            "choices": question.choices.all(),
            "checked_standards": question.standards.all()
        })

def api_get_standards_statistics(request, course_id):
    course = Course.objects.get(id=course_id)
    standards = Standard.objects.filter(course=course)
    questions = MCQuestion.objects.filter(course=course)
    
    standards_question_counter = {}
    
    for standard in standards:
        standards_question_counter[standard.short_name] = 0
    
    for question in questions:
        for standard in question.standards.all():
            standards_question_counter[standard.short_name] += 1
    
    return JsonResponse({
        "labels": list(standards_question_counter.keys()),
        "datasets": [{
            "label": "Question(s)",
            "data": list(standards_question_counter.values()),
            "backgroundColor": [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)',
                'rgb(54, 76, 255)',
            ],
            "hoverOffset": 4
        }]
    })