from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from multitest.models import Test, Question, Answer


class MultitestViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', is_active=True, is_staff=False, is_superuser=False)
        self.user.set_password('user')
        self.user.save()

        self.c = Client()
        self.c.login(username='user', password='user')
        self.stest = Test.objects.create(title='Test, test')
        self.squestion = Question.objects.create(question='Is that true?', test=self.stest)
        self.sanswer = Answer.objects.create(answer='Yes', is_correct=True, question=self.squestion)
        self.sanswer2 = Answer.objects.create(answer='No', is_correct=False, question=self.squestion)

    def test_views_guest_access(self):
        guest = Client()
        response = guest.get(reverse('index'))
        self.assertTemplateUsed(response, 'multitest/index.html')
        response = guest.get(reverse('login'))
        self.assertTemplateUsed(response, 'multitest/login.html')
        response = guest.get(reverse('register'))
        self.assertTemplateUsed(response, 'multitest/register.html')

    def test_only_users_access(self):
        guest = Client()
        response = guest.get(reverse('test', kwargs={'test_id': self.stest.id}))
        self.assertTemplateNotUsed(response, 'multitest/test.html')

    def test_list_all_tests(self):
        response = self.c.get(reverse('index'))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, self.stest.title)

    def test_display_test(self):
        response = self.c.get(reverse('test', kwargs={'test_id': self.stest.id}))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, self.squestion.question)
        self.assertContains(response, self.sanswer.answer)
        self.assertContains(response, self.sanswer2.answer)

    def test_display_correct_result(self):
        response = self.c.post(reverse('test', kwargs={'test_id': self.stest.id}), {
            'question'+str(self.squestion.id)+'[]': self.sanswer.id,
        })
        self.assertEqual(response.context['points'], 1)
        self.assertEqual(response.context['max_points'], 1)

        response = self.c.post(reverse('test', kwargs={'test_id': self.stest.id}), {
            'question'+str(self.squestion.id)+'[]': self.sanswer2.id,
        })
        self.assertEqual(response.context['points'], 0)
        self.assertEqual(response.context['max_points'], 1)

        response = self.c.post(reverse('test', kwargs={'test_id': self.stest.id}), {
            'question'+str(self.squestion.id)+'[]': (self.sanswer2.id, self.sanswer.id),
        })
        self.assertEqual(response.context['points'], 0)
        self.assertEqual(response.context['max_points'], 1)

    def test_user_login(self):
        guest = Client()
        response = guest.post(reverse('login'), {'login': 'user', 'password': 'user'})
        self.failUnless(response.status_code, 302)
        response = guest.get(reverse('index'))
        self.assertContains(response, 'Wyloguj')

    def test_user_register(self):
        users = User.objects.count()

        guest = Client()
        response = guest.post(reverse('register'),
                              {'login': 'test2', 'email': 'test2@wp.pl', 'password': 'test2', 'verify': 'warszawa'})
        self.failUnless(response.status_code, 302)
        self.assertEqual(User.objects.count(), users+1)