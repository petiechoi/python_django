from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from ..models import Question


def index(request):
    """
    목록 출력
    """
    # 입력인자
    page = request.GET.get('page','1')  # 페이지
    kw = request.GET.get('kw', '')      # 검색어

    # 조회
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10)    # 페이지당 10개씩 보여 주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page':page, 'kw' : kw}
    return render(request,'community/question_list.html', context)

def detail(request, question_id):
    """
    내용 출력
    """
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context ={'question' : question}
    return render(request, 'community/question_detail.html', context)
