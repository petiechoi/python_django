from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.utils import timezone
# Create your views here.

def index(request):
    """
    목록 출력
    """
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    #return HttpResponse("안녕하세요 Python 입문 환영합니다.")
    return render(request,'community/question_list.html', context)

def detail(request, question_id):
    """
    내용 출력
    """
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context ={'question' : question}
    return render(request, 'community/question_detail.html', context)

def answer_create(request, question_id):
    """
    답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'),
                               create_date=timezone.now())
    return redirect('community:detail', question_id = question_id)