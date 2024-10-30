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
            text_content = form.cleaned_data['content']
            sentiment_scores = self.analyze_sentiment(text_content)
            new_text = Text(
                title=form.cleaned_data.get('title', 'Untitled'),
                content=text_content,
                sentiment_textblob=sentiment_scores['textblob'],
                sentiment_vader=sentiment_scores['vader'],
                sentiment_transformer=sentiment_scores['transformer']
            )
            new_text.save()
            return redirect('text_detail', pk=new_text.pk)
        return render(request, 'text_input.html', {'form': form})

    @staticmethod
    def analyze_sentiment(text):
        results = {}

        # TextBlob Analysis: Score ranges from -1 (negative) to 1 (positive)
        blob = TextBlob(text)
        results['textblob'] = blob.sentiment.polarity
        print(blob.sentiment.polarity)

        # VADER Analysis: Compound score ranges from -1 (negative) to 1 (positive)
        analyzer = SentimentIntensityAnalyzer()
        vader_score = analyzer.polarity_scores(text)
        results['vader'] = vader_score['compound']

        # Hugging Face Transformers Analysis: Model-specific; score range depends on the model
        sentiment_analysis = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        transformer_result = sentiment_analysis(text)
        transformer_score = transformer_result[0]['score'] if transformer_result[0]['label'] == 'POSITIVE' else -transformer_result[0]['score']
        results['transformer'] = transformer_score

        return results


class TextDetailView(View):
    def get(self, request, pk):
        text = Text.objects.get(pk=pk)

        # Define threshold for positive, neutral, and negative sentiment
        def interpret_score(score, model_name):
            # Adjust thresholds as needed
            if model_name == "textblob":
                return "Positive 😊" if score > 0.1 else "Negative 😞" if score < -0.1 else "Neutral 😐"
            elif model_name == "vader":
                return "Positive 😊" if score > 0.05 else "Negative 😞" if score < -0.05 else "Neutral 😐"
            elif model_name == "transformer":
                return "Positive 😊" if score > 0.5 else "Negative 😞" if score < -0.5 else "Neutral 😐"
            return "Neutral 😐"

        # Interpret each sentiment score
        sentiment_interpretations = {
            'textblob': interpret_score(text.sentiment_textblob, "textblob"),
            'vader': interpret_score(text.sentiment_vader, "vader"),
            'transformer': interpret_score(text.sentiment_transformer, "transformer"),
        }

        context = {
            'text': text,
            'sentiment_textblob': text.sentiment_textblob,
            'sentiment_vader': text.sentiment_vader,
            'sentiment_transformer': text.sentiment_transformer,
            'sentiment_interpretations': sentiment_interpretations,
        }
        return render(request, 'text_detail.html', context)
