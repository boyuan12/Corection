from django.shortcuts import redirect, render
from .models import MCOption, MCQuestion, Course, Standard

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
    return render(request, "dashboard/add-question.html")
