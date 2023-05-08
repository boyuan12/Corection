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
