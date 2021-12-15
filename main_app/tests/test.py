from django.test import TestCase
from ..models import CustomUser, Staff, Course, Subject, FeedbackStaff, LeaveReportStaff
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
        staff = Staff.objects.get(admin_id=custom_user.id)
        f = FeedbackStaff.objects.create(feedback=self.text, staff_id=staff.id, reply='Thanks!')
        f.save()

    def test_feedback(self):
        f = FeedbackStaff.objects.get(feedback=self.text)
        self.assertEqual(f.feedback, self.text)

    def test_staff_id(self):
        f = FeedbackStaff.objects.get(feedback=self.text)
        custom_user = CustomUser.objects.get(email='testemail@mail.ru')
        staff = Staff.objects.get(admin_id=custom_user.id)
        self.assertEqual(f.staff_id, staff.id)

class LeaveReportStaffTestCase(TestCase):
    def setUp(self):
        self.date = '2021-11-11'
        self.message = 'I\'m leaving'

        custom_user = CustomUser.objects.create_user(email='testemail@mail.ru',
                                                     password='12345',
                                                     user_type=2, first_name='first',
                                                     last_name='second', gender='M')
        custom_user.save()
        staff = Staff.objects.get(admin_id=custom_user.id)
        l = LeaveReportStaff.objects.create(date=self.date, message=self.message,
                                            staff_id=staff.id)
        l.save()

    def test_message(self):
        l = LeaveReportStaff.objects.get(date=self.date)
        self.assertEqual(l.message, self.message)


    def test_status_default(self):
        l = LeaveReportStaff.objects.get(date=self.date)
        self.assertEqual(l.status, 0)