from django.urls import path
#added apiviews and 5th path in list
from . import views, apiviews

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('questions/', apiviews.questions_view, name='questions_view'),
    path('questions/<int:question_id>/result/', apiviews.question_result_view, name='question_result_view'),
    path('questions/<int:question_id>/choices/', apiviews.choices_view, name='choices_view'),
    path('questions/<int:question_id>/qdetail/', apiviews.question_detail_view, name = 'detail_view'),
    path('questions/multiple-questions/', apiviews.multiple_questions_view, name='multiple_questions_view'),
    # path('questions/<int:question_id>/fullinput/', apiviews.multiple_choices_View.as_view(), name = 'fullview'),
    path('questions/<int:question_id>/add_votes/', apiviews.vote_view, name='api_vote'),
]
