from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import hypernews.settings as st
from django.views import View
from django.utils import timezone

# Create your views here.
def index(request):
    # context = {'coming_soon': 'Coming soon'}
    # return render(request, 'news/index.html', context)
    return redirect('/news/')

def json_news(request, news_id):

    with open(st.NEWS_JSON_PATH, 'r') as f:
        news_by_id = json.load(f)

    context = news_by_id[news_id - 1]
    return render(request, 'news/json_news.html', context)

def news_main(request):
    title_filter = request.GET.get('q') if request.GET.get('q') else ''

    with open(st.NEWS_JSON_PATH, 'r') as f:
        news_by_id = json.load(f)
    sorted_dates = sorted(list(set(n['created'][:-9] for n in news_by_id)), reverse=True)
    news_grouped = {}  # List of lists
    for d in sorted_dates:
            date_group = []  # Inner list
            for n in news_by_id:
                if n['created'][:-9] == d and title_filter.lower() in n['title'].lower():
                    date_group.append(n)
            if date_group:
                news_grouped[d] = date_group

    context = {'news_grouped': news_grouped}
    return render(request, 'news/news_main.html', context)

class NewsCreate(View):
    def get(self, request):
        return render(request, 'news/news_create.html')
    def post(self, request, *args, **kwargs):
        with open(st.NEWS_JSON_PATH, 'r') as f:
            news_by_id = json.load(f)
        next_link = max([int(n['link']) for n in news_by_id]) + 1
        title = request.POST.get('title')
        text = request.POST.get('text')
        created = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        news = {'created': created, 'title': title, 'text': text, 'link':next_link}
        news_by_id.append(news)
        with open(st.NEWS_JSON_PATH, 'tw') as f:
            json.dump(news_by_id, f)
        return redirect('/news/')


