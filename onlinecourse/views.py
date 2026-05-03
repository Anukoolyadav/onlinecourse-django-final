from django.shortcuts import render, get_object_or_404
from .models import Course, Enrollment, Submission, Choice

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)

    selected_choices = request.POST.getlist('choice')

    submission = Submission.objects.create(enrollment=enrollment)

    for choice_id in selected_choices:
        choice = Choice.objects.get(id=int(choice_id))
        submission.choices.add(choice)

    return show_exam_result(request, course_id)

def show_exam_result(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)

    submission = Submission.objects.filter(enrollment=enrollment).last()

    correct_choices = Choice.objects.filter(is_correct=True)
    selected_choices = submission.choices.all()

    score = 0
    total = correct_choices.count()

    for choice in selected_choices:
        if choice in correct_choices:
            score += 1

    percentage = (score / total) * 100 if total > 0 else 0

    return render(request, 'onlinecourse/result.html', {
        'course': course,
        'score': percentage,
        'total': total
    })
