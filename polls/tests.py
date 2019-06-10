from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question, Choice
from django.urls import reverse
from .serializers import QuestionResultPageSerializer, VoteSerializer
from rest_framework.test import APIClient, APITestCase#, #APIRequestFactory
from rest_framework import status
import json
from django.shortcuts import get_object_or_404

# Create your tests here.
#Create test before writing class, in order to better understand different potential scenarios/issues
#Get the number of votes for some choice, use the API to cast another vote for that choice, get the new number of votes
#for that choice, and verify that the new number is one more than the old one.

class VoteNumberTests(APITestCase):
    #     #In order for this test to be run, the boolean fields had to be disabled: was_published_recently
    def setUp(self):
        q_obj = Question.objects.create(
            question_text='Foobar',
            pub_date='2019-06-05T14:18:26-04:00'
            )
        q = Question.objects.get(question_text__startswith='Foobar')
        q.choice_set.create(choice_text='Foo', votes=0)


    def test_valid_votes(self):
        fullc = Choice.objects.all()
        c = fullc[0]
        q = Question.objects.get(question_text__startswith='Foobar')

        # print(str(c.id) + ', CHOICE')
        # print(str(q.id) + ', QUESTION')
        c.votes += 1
        c.save()
        client = APIClient()
        new_votes = client.get('/polls/questions/1/result/')
        # print(new_votes.data)
        js = json.dumps(new_votes.data)
        # print(js)
        json_before = json.loads(js)
        choice_before = json_before['choices']
        string_choice = str(choice_before[0])
        final_choice_list = string_choice[1:-1].split()
        choice_value = final_choice_list[1]
        votes_after = final_choice_list[5]
        # print(str(votes_after) + ', VOTES')

        add_v = client.patch('/polls/questions/1/add_votes/', {'choice_id': '1'}, format='json')
        # print(str(add_v.data) + ', NEW VOTES')
        actual_test_for_votes = add_v.data
        #This is the voting process used in apiviews; the only change is that the method of collecting the Choice model is bypassed
        # choice_votes = c.votes
        self.assertEqual(int(votes_after)+1, actual_test_for_votes)
        #This test tests that both the mechanism for voting and the API request work correctly!

    def test_invalid_vote(self):
        fullc = Choice.objects.all()
        c = fullc[0]
        q = Question.objects.get(question_text__startswith='Foobar')

        # print(str(c.id) + ', CHOICE')
        # print(str(q.id) + ', QUESTION')
        c.votes += 1
        c.save()
        client = APIClient()
        new_votes = client.get('/polls/questions/1/result/')
        # print(new_votes.data)
        js = json.dumps(new_votes.data)
        # print(js)
        json_before = json.loads(js)
        choice_before = json_before['choices']
        string_choice = str(choice_before[0])
        final_choice_list = string_choice[1:-1].split()
        choice_value = final_choice_list[1]
        votes_after = final_choice_list[5]
        # print(str(votes_after) + ', VOTES')
        try:
            add_v = client.patch('/polls/questions/1/add_votes/', {'choice_id': '2'}, format='json') #choice_ID 2 does not exist
        except:
            add_v = client.patch('/polls/questions/1/add_votes/', {'choice_id': '2'}, format='json')
            self.assertEqual(add_v.status_code, 400)
            #Because choice_id 2 did not exist, a status code 400 was to be raised


    def test_create_single_question(self):
        client = APIClient()
        question = client.post('/polls/questions/', {"id":"313","question_text":"Foo","pub_date":"2019-05-29T10:23:26-04:00","choices":[{"choice_text":"Bar"},{"choice_text":"Foobar"}]}, format = 'json')
        check_question = client.get('/polls/questions/313/qdetail/')
        print(check_question)
        self.assertEqual(check_question.status_code, 200)

    def test_invalid_no_question_text(self):
        client = APIClient()
        question = client.post('/polls/questions/', {"id":"314","question_text":"","pub_date":"2019-05-29T10:23:26-04:00","choices":[{"choice_text":"Bar"},{"choice_text":"Foobar"}]}, format = 'json')
        check_question = client.get('/polls/questions/314/qdetail/')
        print(check_question)
        self.assertEqual(check_question.status_code, 404)

    def test_invalid_no_choice_text(self):
        client = APIClient()
        try:
            c_input = client.post('/polls/questions/', {"id":"314","question_text":"Foobar","pub_date":"2019-05-29T10:23:26-04:00"}, format = 'json')
        except:
            check_input = client.get('/polls/questions/314/qdetail/')
            print(check_input)
        self.assertEqual(check_input.status_code, 404)

    def test_not_enough_choices(self):
        client = APIClient()
        try:
            inc_input = client.post('/polls/questions/', {"id":"314","question_text":"Foobar","pub_date":"2019-05-29T10:23:26-04:00","choices":[{"choice_text":"Bar"}]}, format = 'json')

        except:
            check_input = client.get('/polls/questions/314/qdetail/')
            print(check_input)

        self.assertEqual(check_input.status_code, 404)

#        Because the page was not created, trying to go to that q_id page will give a 404 error!
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
    # was_published_recently returns False for future questions
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
    #Should return false for questions w/ pub_date >= 1 day
        time = timezone.now() - datetime.timedelta(days = 1, seconds = 1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours = 23, minutes = 59, seconds = 59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(question_text = question_text, pub_date = time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        #if no questions exist
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        #Questions with past pubdate are on index page
        create_question(question_text = "Future question.", days = 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_future_question_and_past_question(self):
        #Even if both past and future questions exist
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )


    def test_two_past_questions(self):
        #Questions index can display multiple questions
        create_question(question_text = "Past question 1.", days = -30)
        create_question(question_text = "Past question 2.", days = -5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question 2.>', '<Question: Past question 1.>'])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        #The detail view of a question with future pub date gives a 404 not found
        future_question = create_question(question_text = 'Future question.', days = 5)
        url = reverse('polls:detail', args = (future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_past_question(self):
        past_question = create_question(question_text = 'Past Question.', days = -5)
        url = reverse('polls:detail', args = (past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
