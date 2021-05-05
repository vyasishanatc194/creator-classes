from django.core.management.base import BaseCommand
from django.utils import timezone

from user.models import StreamBooking

from creator_class.settings import TIME_ZONE, USER_STREAM_REMINDER_TEMPLATE
from creator_class.helpers import send_templated_email


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
                    name = notifications[0].user.username if notifications[
                        0].user.username else f"{notifications[0].user.first_name} {notifications[0].user.last_name}"
                    creator_name = notifications[0].stream.creator.username if notifications[
                        0].stream.creator.username else f"{notifications[0].stream.creator.first_name} {notifications[0].stream.creator.last_name}"
                    if notifications[0].user.email:
                        data = {'name': name,
                                'date': book.stream.stream_datetime.date().strftime('%m/%d/%Y'),
                                'time': book.stream.stream_datetime.time().strftime("%H:%M"),
                                'creator_name': creator_name,
                                }
                        send_templated_email(book.user.email, USER_STREAM_REMINDER_TEMPLATE, data)

                self.stdout.write(self.style.SUCCESS("Default notification sent"))
            self.stdout.write(self.style.SUCCESS("Successfully sent custom notification"))
        except Exception as inst:
            self.stdout.write(self.style.ERROR(inst))
