from django.core.management.base import BaseCommand
from django.utils import timezone

from user.models import StreamBooking

from creator_class.settings import TIME_ZONE
from creator_class.helpers import send_email


class Command(BaseCommand):
    help = "Custom Notification set by User to get notified before the Session"

    def handle(self, *args, **options):
        notifications = StreamBooking.objects.filter(stream__stream_datetime__gte=timezone.datetime.now(),
                                                      active=True)
        try:
            for book in notifications:
                datetime_session = book.stream.stream_datetime
                datetime_session = datetime_session - timezone.timedelta(hours=2)
                datetime_session = timezone.make_aware(datetime_session,
                                                       timezone=timezone.now().astimezone().tzinfo)
                past_time = timezone.now().astimezone().replace(microsecond=0) - timezone.timedelta(seconds=62)
                if past_time < datetime_session < timezone.now().astimezone().replace(microsecond=0):
                    subject = "[CreatorClasses] Reminder Of Stream Booking"
                    text_content = f"Hello {book.user.first_name}, \n This is the reminder about your session booking today at {book.stream.stream_datetime.date()} on {book.stream.stream_datetime.time()}"
                    send_email(user=book.user, subject=subject, text_content=text_content)

                self.stdout.write(self.style.SUCCESS("Default notification sent"))
            self.stdout.write(self.style.SUCCESS("Successfully sent custom notification"))
        except Exception as inst:
            self.stdout.write(self.style.ERROR(inst))
