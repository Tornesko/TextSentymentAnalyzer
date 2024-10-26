from django.shortcuts import render, redirect
from django.views import View
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

from .forms import TextForm
from .models import Text


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

    @staticmethod
    def analyze_sentiment(text):
        results = {}

        # TextBlob Analysis
        blob = TextBlob(text)
        results['textblob'] = blob.sentiment.polarity

        # VADER Analysis
        analyzer = SentimentIntensityAnalyzer()
        vader_score = analyzer.polarity_scores(text)
        results['vader'] = vader_score['compound']

        # Hugging Face Transformers Analysis
        sentiment_analysis = pipeline("sentiment-analysis")
        transformer_result = sentiment_analysis(text)
        transformer_score = transformer_result[0]['score'] if transformer_result[0]['label'] == 'POSITIVE' else - \
        transformer_result[0]['score']
        results['transformer'] = transformer_score

        return results


class TextDetailView(View):
    def get(self, request, pk):
        text = Text.objects.get(pk=pk)
        sentiment = text.sentiment_score
        context = {
            'text': text,
            'sentiment': sentiment,
        }
        return render(request, 'text_detail.html', context)
