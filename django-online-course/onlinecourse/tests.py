from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Choice, Course, Enrollment, Question, Submission


class ExamTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('learner', password='test-password')
        self.other = get_user_model().objects.create_user('other', password='test-password')
        self.course = Course.objects.create(name='Example', description='Example course')
        Enrollment.objects.create(user=self.user, course=self.course)
        self.q = Question.objects.create(course=self.course, question_text='Select both', grade=3)
        self.a = Choice.objects.create(question=self.q, choice_text='A', is_correct=True)
        self.b = Choice.objects.create(question=self.q, choice_text='B', is_correct=True)
        self.bad = Choice.objects.create(question=self.q, choice_text='Wrong', is_correct=False)
        self.client.force_login(self.user)
        self.url = reverse('onlinecourse:submit', args=[self.course.id])

    def submit_choices(self, choices):
        response = self.client.post(self.url, {'choices': [str(c.id) for c in choices]})
        self.assertEqual(response.status_code, 302)
        return self.client.get(response.url)

    def test_model_score_requires_all_and_only_correct_choices(self):
        self.assertTrue(self.q.is_get_score([self.a.id, self.b.id]))
        self.assertFalse(self.q.is_get_score([self.a.id]))
        self.assertFalse(self.q.is_get_score([self.a.id, self.b.id, self.bad.id]))

    def test_all_and_only_correct_choices_pass(self):
        response = self.submit_choices([self.a, self.b])
        self.assertContains(response, '100.0%')
        self.assertContains(response, 'Correct')

    def test_missing_or_extra_choice_fails_question(self):
        self.assertContains(self.submit_choices([self.a]), '0.0%')
        self.assertContains(self.submit_choices([self.a, self.b, self.bad]), '0.0%')

    def test_submissions_are_private(self):
        self.submit_choices([self.a, self.b])
        submission = Submission.objects.latest('id')
        self.client.force_login(self.other)
        url = reverse('onlinecourse:show_exam_result', args=[self.course.id, submission.id])
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.post(self.url).status_code, 404)

    def test_exam_requires_post_and_enrollment(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)
        self.client.logout()
        self.assertEqual(self.client.post(self.url).status_code, 302)

    def test_weighted_scores_and_detail_page(self):
        q2 = Question.objects.create(course=self.course, question_text='One answer', grade=1)
        c2 = Choice.objects.create(question=q2, choice_text='Yes', is_correct=True)
        response = self.client.get(reverse('onlinecourse:course_details', args=[self.course.id]))
        self.assertContains(response, 'Select both')
        self.assertContains(response, 'One answer')
        self.assertContains(self.submit_choices([self.a, self.b, c2]), '100.0%')
        self.assertContains(self.submit_choices([self.a, self.b]), '75.0%')

# Create your tests here.
