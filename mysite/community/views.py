from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    """
    목록 출력
    """
    # 입력인자
    page = request.GET.get('page','1')  # 페이지

    # 조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징 처리
    paginator = Paginator(question_list, 10)    # 페이지당 10개씩 보여 주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
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
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('community:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form' : form}
    return render(request, 'community/question_detail.html', context)



    question.answer_set.create(content=request.POST.get('content'),
                               create_date=timezone.now())
    return redirect('community:detail', question_id = question_id)

def question_create(request):
    """
    질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('community:index')
    else:
        form = QuestionForm()
    context = {'form' : form}
    return render(request, 'community/question_form.html', context)