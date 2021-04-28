from django.core.management.base import BaseCommand
from django.utils import timezone

from user.models import SessionBooking

from creator_class.settings import TIME_ZONE
from creator_class.helpers import send_email


class Command(BaseCommand):
    help = "Custom Notification set by User to get notified before the Session"

    def handle(self, *args, **options):
        notifications = SessionBooking.objects.filter(time_slot__slot_datetime__gte=timezone.datetime.now(),
                                                      active=True)
        try:
            for book in notifications:
                datetime_session = book.time_slot.slot_datetime
                datetime_session = datetime_session - timezone.timedelta(hours=2)
                datetime_session = timezone.make_aware(datetime_session,
                                                       timezone=timezone.now().astimezone().tzinfo)
                past_time = timezone.now().astimezone().replace(microsecond=0) - timezone.timedelta(seconds=62)
                if past_time < datetime_session < timezone.now().astimezone().replace(microsecond=0):
                    subject = "[CreatorClasses] Reminder Of Session"
                    text_content = f"Hello {book.user.first_name}, \n This is the reminder about your session booking today at {book.time_slot.slot_datetime.date()} on {book.time_slot.slot_datetime.time()}"
                    send_email(user=book.user, subject=subject, text_content=text_content)

                self.stdout.write(self.style.SUCCESS("Default notification sent"))
            self.stdout.write(self.style.SUCCESS("Successfully sent custom notification"))
        except Exception as inst:
            self.stdout.write(self.style.ERROR(inst))
