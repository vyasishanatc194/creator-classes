from django.core.management.base import BaseCommand
from models import User
from creator_class.utils import MyStripe
from django.conf import settings


class Command(BaseCommand):

    help = "Update credit"

    def handle(self, *args, **options):
        check_active_plan = User.objects.filter(plan_id!="", is_active=True, is_creator=False)
        try:
            for obj in check_active_plan:

                if obj.stripe_subscription_id and obj.plan_id:
                    try:
                        stripe = MyStripe()
                        check_stripe_status = stripe.RetrieveSubscription(obj.stripe_subscription_id)
                        check_invoice = stripe.InvoiceStatus(check_stripe_status['latest_invoice'])

                        if check_stripe_status['status']=='past_due':
                            obj.plan_id = None
                            obj.stripe_subscription_id = None
                            stripe.CancelSubscriptionPlan(obj.stripe_subscription_id)
                            obj.save()
                            
                            # TODO Send Email- subscription is canceled

                    except:
                        pass   
                
                self.stdout.write(self.style.SUCCESS("Successfully updated"))
        except:
            self.stdout.write(self.style.ERROR("Error in update"))