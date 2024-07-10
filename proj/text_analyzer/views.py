# views.py
from django.shortcuts import render, redirect
from django.views import View
from .forms import TextForm
from .models import Text
from textblob import TextBlob


class TextListView(View):
    def get(self, request):
        texts = Text.objects.all()
        return render(request, 'text_list.html', {'texts': texts})


class TextInputView(View):
    def get(self, request):
        form = TextForm()
        return render(request, 'text_input.html', {'form': form})

    def post(self, request):
        form = TextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['content']
            sentiment_score = self.analyze_sentiment(text)
            new_text = Text(content=text, sentiment_score=sentiment_score)
            new_text.save()
            return redirect('text_detail', pk=new_text.pk)
        return render(request, 'text_input.html', {'form': form})

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        return sentiment_score


class TextDetailView(View):
    def get(self, request, pk):
        text = Text.objects.get(pk=pk)
        sentiment = text.sentiment_score
        context = {
            'text': text,
            'sentiment': sentiment,
        }
        return render(request, 'text_detail.html', context)
