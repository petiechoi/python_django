from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..models import Question, Answer

from ..forms import AnswerForm


@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('community:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form' : form}
    return render(request, 'community/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    답변 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('community:detail', Answer_id=answer.question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('community:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context ={'answer':answer, 'form' : form}
    return render(request, 'community/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    답변 삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('community:detail', question_id = answer.question.id)
