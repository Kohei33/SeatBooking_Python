import datetime
from django.test import TestCase
from reserve.models import Seat, Schedule
from django.contrib.auth.models import User

# Create your tests here.
class SeatModelTests(TestCase):
    # 共通
    def test_is_empty(self):
        saved_seats = Seat.objects.all()
        self.assertEqual(saved_seats.count(), 0)
    
    # Seat
    def test_is_count_one_seat(self):
        seat = Seat(name='A')
        seat.save()
        saved_seats = Seat.objects.all()
        self.assertEqual(saved_seats.count(), 1)
    
    def test_saving_and_retrieving_seat(self):
        seat = Seat()
        name = "A"
        seat.name = name
        seat.save()

        saved_seats = Seat.objects.all()
        actual_seat = saved_seats[0]

        self.assertEqual(actual_seat.name, name)

    # Schedule
    def test_is_count_one_schedule(self):
        user = User.objects.create()
        user.save()
        seat = Seat(name='A')
        seat.save()
        schedule = Schedule(date='2023-06-09', seat=seat, user=user, created_date='2023-06-09')
        schedule.save()
        saved_schedules = Schedule.objects.all()
        self.assertEqual(saved_schedules.count(), 1)
    
    def test_saving_and_retrieving_schedule(self):
        user = User.objects.create()
        username = 'testuser'
        user.username = username
        user.save()

        seat = Seat()
        name = "A"
        seat.name = name
        seat.save()
        
        date_1 = datetime.date(year=2023, month=6, day=9)
        date_2 = datetime.datetime(year=2023, month=6, day=8, tzinfo=datetime.timezone.utc)
        schedule = Schedule(date=date_1, seat=seat, user=user, created_date=date_2)
        schedule.save()

        saved_schedules = Schedule.objects.all()
        actual_schedule = saved_schedules[0]

        self.assertEqual(actual_schedule.date, date_1)
        self.assertEqual(actual_schedule.seat.name, name)
        self.assertEqual(actual_schedule.user.username, username)
        self.assertEqual(actual_schedule.created_date, date_2)
