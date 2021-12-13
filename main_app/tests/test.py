from django.test import TestCase
from ..models import CustomUser, Admin, Staff, Student, Course, Subject, FeedbackStaff
from ..views import *

class CourseTestCase(TestCase):
    def setUp(self):
        c = Course.objects.create(name='TestCourse')
        c.save()

    def test_name(self):
        c = Course.objects.get(name='TestCourse')
        self.assertEqual(c.name, 'TestCourse')

class StaffTestCase(TestCase):
    def setUp(self):
        c = Course.objects.create(name='TestCourse')
        c.save()
        custom_user = CustomUser.objects.create_user(email='testemail@mail.ru',
                                                     password='12345',
                                                     user_type=2, first_name='first',
                                                     last_name='second', gender='M')
        custom_user.staff.course = c
        custom_user.save()

    def test_user_type(self):
        custom_user = CustomUser.objects.get(email='testemail@mail.ru')
        self.assertEqual(custom_user.user_type, '2')

    def test_name(self):
        custom_user = CustomUser.objects.get(email='testemail@mail.ru')
        self.assertEqual(custom_user.first_name, 'first')

    def test_staff_course(self):
        custom_user = CustomUser.objects.get(email='testemail@mail.ru')
        staff = Staff.objects.get(admin_id=custom_user.id)
        course = Course.objects.get(id=staff.course_id)
        self.assertEqual(course.name, 'TestCourse')

    def test_is_superuser(self):
        custom_user = CustomUser.objects.get(email='testemail@mail.ru')
        self.assertFalse(custom_user.is_superuser)

class StaffFeedbackTestCase(TestCase):
    def setUp(self):
        self.text = 'Nice system!'
        custom_user = CustomUser.objects.create_user(email='testemail@mail.ru',
                                                     password='12345',
                                                     user_type=2, first_name='first',
                                                     last_name='second', gender='M')
        custom_user.save()
        staff = Staff.objects.get(custom_user.id)
        f = FeedbackStaff.objects.create(feedback=self.text, staff=staff, reply=None)
        f.save()

    def test_(self):
        f = FeedbackStaff.objects.get(text=self.text)
        self.assertEqual(f.feedback, self.text)
