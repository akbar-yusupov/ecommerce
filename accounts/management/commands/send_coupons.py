from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from accounts.tasks import send_available_coupons


class Command(BaseCommand):
    help = _("The command sends emails with active coupons to all users")

    def handle(self, *args, **options):
        send_available_coupons.delay()
        self.stdout.write(_("Send Coupons successfully executed"))
