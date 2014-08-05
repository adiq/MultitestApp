from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from multitest.models import Test, Question, Answer


class AdminViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='admin', is_active=True, is_staff=True, is_superuser=True)
        self.user.set_password('admin')
        self.user.save()

        self.c = Client()
        self.c.login(username='admin', password='admin')
        self.stest = Test.objects.create(title='Test, test')
        self.squestion = Question.objects.create(question='Is that true?', test=self.stest)
        self.sanswer = Answer.objects.create(answer='Yes', is_correct=True, question=self.squestion)
        self.sanswer2 = Answer.objects.create(answer='No', is_correct=False, question=self.squestion)

    def test_only_staff_access(self):
        guest = Client()
        response = guest.get(reverse('admin:index'))
        self.assertTemplateNotUsed(response, 'multitest_admin/index.html')
        response = guest.get(reverse('admin:test', kwargs={'test_id': self.stest.id}))
        self.assertTemplateNotUsed(response, 'multitest_admin/test.html')
        response = guest.get(reverse('admin:question', kwargs={'question_id': self.squestion.id}))
        self.assertTemplateNotUsed(response, 'multitest_admin/question.html')

    def test_list_all_tests(self):
        response = self.c.get(reverse('admin:index'))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, self.stest.title)

    def test_list_all_questions(self):
        response = self.c.get(reverse('admin:test', kwargs={'test_id': self.stest.id}))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, self.squestion.question)

    def test_list_all_answers(self):
        response = self.c.get(reverse('admin:question', kwargs={'question_id': self.squestion.id}))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, self.sanswer.answer)
        self.assertContains(response, self.sanswer2.answer)


    def test_create_actions_new_test(self):
        """
        crate_actions(request, *args, **kwargs) should create Test
        depends on view_name from request arg and POST param
        """

        tests = Test.objects.count()

        response = self.c.post(reverse('admin:index'), {'new': '1'})
        self.failUnlessEqual(response.status_code, 200)
        self.assertEquals(Test.objects.count(), tests+1)

    def test_create_actions_new_question(self):
        """
        crate_actions(request, *args, **kwargs) should create Question
        depends on view_name from request arg and POST param
        """

        questions = Question.objects.count()

        response = self.c.post(reverse('admin:test', kwargs={'test_id': self.stest.id}), {'new': '1'})
        self.failUnlessEqual(response.status_code, 200)
        self.assertEquals(Question.objects.count(), questions+1)

    def test_create_actions_new_answer(self):
        """
        crate_actions(request, *args, **kwargs) should create Answer
        depends on view_name from request arg and POST param
        """

        answers = Answer.objects.count()

        response = self.c.post(reverse('admin:question', kwargs={'question_id': self.squestion.id}), {'new': '1'})
        self.failUnlessEqual(response.status_code, 200)
        self.assertEquals(Answer.objects.count(), answers+1)

    def test_create_actions_delete_test(self):
        """
        crate_actions(request, *args, **kwargs) should delete Test
        depends on view_name from request arg and POST param
        """

        tests = Test.objects.count()

        response = self.c.post(reverse('admin:index'), {'delete': self.stest.id})
        self.failUnlessEqual(response.status_code, 200)
        self.assertEquals(Test.objects.count(), tests-1)

    def test_create_actions_delete_question(self):
        """
        crate_actions(request, *args, **kwargs) should delete Question
        depends on view_name from request arg and POST param
        """

        questions = Question.objects.count()

        response = self.c.post(reverse('admin:test', kwargs={'test_id': self.stest.id}), {'delete': self.squestion.id})
        self.failUnlessEqual(response.status_code, 200)
        self.assertEquals(Question.objects.count(), questions-1)

    def test_create_actions_delete_answer(self):
        """
        crate_actions(request, *args, **kwargs) should delete Answern
        depends on view_name from request arg and POST param
        """

        answers = Answer.objects.count()

        response = self.c.post(reverse('admin:question', kwargs={'question_id': self.squestion.id}), {'delete': self.sanswer.id})
        self.failUnlessEqual(response.status_code, 200)
        self.assertEquals(Answer.objects.count(), answers-1)