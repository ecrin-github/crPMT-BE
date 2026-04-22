from django.core.management.base import BaseCommand
from context.services.ctu_service import sync_ctus_from_sharepoint


class Command(BaseCommand):
    help = "Synchronize CTUs from SharePoint"

    def handle(self, *args, **options):
        # NOTE:
        # This CSV-based synchronization has been temporarily disabled.
        # It was originally used to bulk import and keep the CTU database
        # in sync with SharePoint data (via a CSV export from SAS Tracker).
        #
        # The system now relies on an on-demand synchronization approach:
        # CTUs are fetched directly from SharePoint in the frontend and
        # resolved/updated in the database at save time.
        #
        # This command is kept for potential future use (e.g., full resync or fallback).
        
        # result = sync_ctus_from_sharepoint()
        # self.stdout.write(self.style.SUCCESS(f"Done: {result}"))

        self.stdout.write("CSV sync temporarily disabled.")