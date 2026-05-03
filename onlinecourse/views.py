def show_exam_result(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)
    submission = Submission.objects.filter(enrollment=enrollment).last()

    selected_choices = submission.choices.all()

    total_score = 0
    possible_score = 0

    for question in course.question_set.all():
        possible_score += question.grade
        correct_choices = question.choice_set.filter(is_correct=True)
        selected = selected_choices.filter(question=question)

        if set(correct_choices) == set(selected):
            total_score += question.grade

    grade = (total_score / possible_score) * 100 if possible_score > 0 else 0

    return render(request, 'onlinecourse/result.html', {
        'course': course,
        'selected_ids': [c.id for c in selected_choices],
        'grade': grade,
        'total': total_score,
        'possible': possible_score
    })
