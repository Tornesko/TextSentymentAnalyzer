from django.urls import path
from .views import TextInputView, TextDetailView, TextListView

urlpatterns = [
    path('', TextListView.as_view(), name='text_list'),
    path('input/', TextInputView.as_view(), name='text_input'),
    path('text/<int:pk>/', TextDetailView.as_view(), name='text_detail'),
]
