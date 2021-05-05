from django.core.management.base import BaseCommand
from django.utils import timezone

from user.models import SessionBooking

from creator_class.settings import TIME_ZONE, USER_SESSION_REMINDER_TEMPLATE
from creator_class.helpers import send_templated_email



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
                    name = notifications[0].user.username if notifications[
                        0].user.username else f"{notifications[0].user.first_name} {notifications[0].user.last_name}"
                    creator_name = notifications[0].creator.username if notifications[
                        0].creator.username else f"{notifications[0].creator.first_name} {notifications[0].creator.last_name}"
                    if notifications[0].user.email:
                        data = {'name': name,
                                'date': book.time_slot.slot_datetime.date().strftime('%m/%d/%Y'),
                                'time': book.time_slot.slot_datetime.time().strftime("%H:%M"),
                                'creator_name': creator_name,
                                }
                        send_templated_email(book.user.email, USER_SESSION_REMINDER_TEMPLATEN_REMINDER, data)
                self.stdout.write(self.style.SUCCESS("Default notification sent"))
            self.stdout.write(self.style.SUCCESS("Successfully sent custom notification"))
        except Exception as inst:
            self.stdout.write(self.style.ERROR(inst))
