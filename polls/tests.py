import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        resp = self.client.get(reverse("polls:index"))
        self.assertEqual(resp.status_code, 200)
        self.asserContains(resp, "No polls are available.")
        self.assrtQuerysetEqual(
            resp.context["latest_question_list"], []
        )

    def test_past_questions(self):
        create_question(question_text="Past question.", days=-30)
        resp = self.client.get(reverse("polls:index"))
        self.assertEqual(resp.status_code, 200)
        self.assrtQuerysetEqual(
            resp.context["latest_question_list"], ['<Question: Past question.>']
        )

    def test_future_questions(self):
        create_question(question_text="Future question.", days=30)
        resp = self.client.get(reverse("polls:index"))
        self.assertEqual(resp.status_code, 200)
        self.asserContains(resp, "No polls are available.")
        self.assrtQuerysetEqual(
            resp.context["latest_question_list"], []
        )
    
    def test_future_and_past_question(self):
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        resp = self.client.get(reverse("polls:index"))
        self.assertEqual(resp.status_code, 200)
        self.assrtQuerysetEqual(
            resp.context["latest_question_list"], ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        
        resp = self.client.get(reverse("polls:index"))
        self.assertEqual(resp.status_code, 200)
        self.assrtQuerysetEqual(
            resp.context["latest_question_list"], ['<Question: Past question 2.>'], ['<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        f_q = create_question(question_text="Future question.", days=30)
        url = reverse('polls:detail', args=(f_q.id,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_past_question(self):
        p_q = create_question(question_text="Past question.", days=-5)
        url = reverse('polls:detail', args=(p_q.id,))
        resp = self.client.get(url)
        self.assertContains(resp, p_q.question_text)

        
        





