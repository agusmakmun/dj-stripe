"""
sync_customer command.
"""

from django.core.management.base import BaseCommand

from ...settings import djstripe_settings
from ...sync import sync_subscriber


class Command(BaseCommand):
    """Sync subscriber data with stripe."""

    help = "Sync subscriber data with stripe."

    def handle(self, *args, **options):
        """Call sync_subscriber on Subscribers without customers associated to them."""
        qs = djstripe_settings.get_subscriber_model().objects.filter(
            djstripe_customers__isnull=True
        )
        count = 0
        total = qs.count()
        for subscriber in qs:
            count += 1
            pc = int(round(100 * (float(count) / float(total))))
            print(
                f"[{count}/{total} {pc}%] Syncing {subscriber.email} [{subscriber.pk}]"
            )
            sync_subscriber(subscriber)
