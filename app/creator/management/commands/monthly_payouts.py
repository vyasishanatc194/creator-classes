from datetime import date, timedelta
from django.db.models import Sum
import stripe

from django.core.management.base import BaseCommand
from django.conf import settings

# from core.utils import send_sendgrid_email
from creator.models import CreatorTransferredMoney, Creator, CreatorAffiliation, PayoutErrorLog
from customadmin.models import CreatorClassCommission
from user.models import SessionBooking, StreamBooking
from creator_class.helpers import send_templated_email

# Date Format

today = date.today()
yesterday = today - timedelta(days=0)

yesterday_date = today - timedelta(days=31)
start_date_month = f"{yesterday_date} 00:00:00"
end_date = f"{yesterday} 23:59:00"


class Command(BaseCommand):
    help = "Transfer Fund"

    def handle(self, *args, **options):
        try:
            creator_class_commission = CreatorClassCommission.objects.all().first()
            if not creator_class_commission:
                creator_class_commission = CreatorClassCommission()
                creator_class_commission.affiliation_deduction = 10
                creator_class_commission.creator_class_deduction = 10
                creator_class_commission.save()

            creators = Creator.objects.filter(is_active=True)
            affiliation_deduction = creator_class_commission.affiliation_deduction

            for creator in creators:

                """ Check Creator stripe """

                if creator.stripe_account_id:
                    connected_stripe_status = stripe.Account.retrieve(
                        str(creator.stripe_account_id)
                    )

                    """ Check creator stripe card  details"""

                    # PayoutErrorLog.objects.create(
                    #    error_text = str(connected_stripe_status.details_submitted)
                    # )

                    if connected_stripe_status.details_submitted:

                        """ Check creator account to any transaction this week"""

                        transfer = CreatorTransferredMoney.objects.filter(
                            creator__id=creator.id,
                            created_at__range=[start_date_month, end_date],
                        )

                        if not transfer:
                            streams_booked = StreamBooking.objects.filter(stream__creator=creator.pk,
                                                                          created_at__range=[start_date_month,
                                                                                             end_date])
                            stream_earnings = streams_booked.aggregate(Sum('stream__stream_amount'))[
                                'stream__stream_amount__sum']
                            if stream_earnings is None:
                                stream_earnings = 0

                            session_booked = SessionBooking.objects.filter(creator=creator.pk,
                                                                           created_at__range=[start_date_month,
                                                                                              end_date])
                            session_earnings = session_booked.aggregate(Sum('transaction_detail__amount'))[
                                'transaction_detail__amount__sum']
                            if session_earnings is None:
                                session_earnings = 0

                            creator_earnings = (stream_earnings if stream_earnings else 0) + (
                                session_earnings if session_earnings else 0)

                            stream_amount_received = stream_earnings - (float(
                                float(stream_earnings) * creator_class_commission.creator_class_deduction) / 100)
                            session_amount_received = session_earnings - (float(
                                float(session_earnings) * creator_class_commission.creator_class_deduction) / 100)

                            affiliations = CreatorAffiliation.objects.filter(user__affiliated_with=creator)
                            affiliation_commission_total = affiliations.aggregate(Sum('amount'))['amount__sum']

                            if creator_earnings or affiliation_commission_total:
                                final_earning_amount = 0
                                if creator_earnings:
                                    creator_class_deduction = float(float(
                                        creator_earnings) * creator_class_commission.creator_class_deduction) / 100
                                    final_earning_amount = creator_earnings - creator_class_deduction

                                # Affiliation amount
                                final_commission_amount = 0
                                if affiliation_commission_total:
                                    final_commission_amount = float(float(
                                        affiliation_commission_total) * creator_class_commission.affiliation_deduction) / 100

                                transfer_amount = final_earning_amount + final_commission_amount
                                final_amount = round(transfer_amount, 2)
                                try:
                                    transaction = stripe.Transfer.create(
                                        amount=int(final_amount),
                                        currency="usd",
                                        destination=str(creator.stripe_account_id),
                                    )

                                    CreatorTransferredMoney.objects.create(creator=creator, status="success",
                                                                           transaction_id=transaction.id,
                                                                           creator_earnings=creator_earnings,
                                                                           creator_class_deduction=creator_class_deduction,
                                                                           affiliation_commission_total=affiliation_commission_total,
                                                                           affiliation_deduction=affiliation_deduction,
                                                                           final_earning_amount=final_earning_amount,
                                                                           final_commission_amount=final_commission_amount,
                                                                           transferred_amount=final_amount,
                                                                           stream_amount_total=stream_earnings,
                                                                           session_amount_total=session_earnings,
                                                                           session_amount_received=session_amount_received,
                                                                           stream_amount_received=stream_amount_received
                                                                           )
                                    print(".........................................success")
                                    # Send Email
                                    email_data = {
                                        'name': f"{creator.first_name} {creator.last_name}",
                                        'amount': int(final_amount) * 100
                                    }
                                    send_templated_email(creator.email, settings.CREATOR_SIGNUP_TEMPLATE, email_data)


                                except Exception as e:
                                    print("....................................................Error", e)

            print(".........................................success")
            self.stdout.write(self.style.SUCCESS("Successfully transfer amount"))

        except Exception as inst:
            # PayoutErrorLog.objects.create(
            #     error_text = str(inst)
            # )
            print(".........................................Error")
            self.stdout.write(self.style.ERROR("Error in transfer amount"))
