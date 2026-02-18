import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Interview
from .ai import evaluate_full_interview, get_random_question_by_language


@login_required
def home(request):
    languages = {
        "Frontend": ["HTML", "CSS", "JavaScript"],
        "Backend": ["Python", "Django"],
        "Database": ["MySQL", "MongoDB"],
    }
    return render(request, "interview/home.html", {"languages": languages})


@login_required
def start_interview_by_language(request, language):
    request.session["language"] = language

    selected_questions = get_random_question_by_language(language, 10)

    if not selected_questions:
        return redirect("home")

    request.session["questions"] = selected_questions
    request.session["current_index"] = 0
    request.session["answers"] = []

    return redirect("question_page")


@login_required
def question_page(request):
    questions = request.session.get("questions")
    index = request.session.get("current_index", 0)

    if not questions:
        return redirect("home")

    if index >= len(questions):
        return redirect("result")

    question = questions[index]

    return render(request, "interview/question.html", {
        "question": question,
        "number": index + 1,
        "total": len(questions)
    })


@login_required
def submit_answer(request):
    if request.method != "POST":
        return redirect("home")

    questions = request.session.get("questions")
    index = request.session.get("current_index", 0)
    answer = request.POST.get("answer")

    if not questions:
        return redirect("home")

    answers = request.session.get("answers", [])
    answers.append(answer)

    request.session["answers"] = answers
    request.session["current_index"] = index + 1

    if index + 1 >= len(questions):
        return redirect("result")

    return redirect("question_page")


@login_required
def result(request):
    questions = request.session.get("questions", [])
    answers = request.session.get("answers", [])
    language = request.session.get("language")

    if not questions or not answers:
        return redirect("home")

    evaluation_text = evaluate_full_interview(questions, answers)

    if not evaluation_text:
        evaluation_text = "AI evaluation failed."
        total_score = 0
        average_score = 0
    else:
        scores = [int(s) for s in re.findall(r"Score:\s*(\d+)", evaluation_text)]
        total_score = sum(scores)
        average_score = total_score / len(scores) if scores else 0

    Interview.objects.create(
        user=request.user,
        language=language,
        total_score=total_score,
        feedback=evaluation_text
    )

    request.session.flush()

    return render(request, "interview/result.html", {
        "total_score": total_score,
        "average_score": round(average_score, 2),
        "feedback": evaluation_text
    })