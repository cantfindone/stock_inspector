from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic, View

from webapp.models import Question, Choice, Stock


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'webapp/index.html', context)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'webapp/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'webapp/results.html'


class StockCreateView(View):
    def get(self, request, id, name):
        data = {'id': id, 'name': name}
        return JsonResponse(data)

    def post(self, request):
        data = {}
        try:
            id = request.POST.get('id')
            name = request.POST.get('name')
            stock = Stock(id=id, name=name, xchg='sz' if id[0] < '6' else 'sh')
            stock.save()
            data['res'] = 'success'
        except Exception as e:
            data['res'] = e.__cause__
        return JsonResponse(data)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'webapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('webapp:results', args=(question.id,)))
