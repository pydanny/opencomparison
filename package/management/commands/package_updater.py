import logging
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand

from github3 import login as github_login

from package.models import Package
from core.utils import healthcheck

logger = logging.getLogger(__name__)


class PackageUpdaterException(Exception):
    def __init__(self, error, title):
        log_message = f"For {title}, {type(error)}: {error}"
        logging.critical(log_message)
        logging.exception(error)


class Command(BaseCommand):

    help = "Updates all the packages in the system. Commands belongs to django-packages.package"

    def handle(self, *args, **options):

        github = github_login(token=settings.GITHUB_TOKEN)

        for package in Package.objects.iterator():

            # Simple attempt to deal with Github rate limiting
            while True:
                print(f"github.ratelimit_remaining=={github.ratelimit_remaining}")
                if github.ratelimit_remaining < 50:
                    print(f"{__file__}::handle::sleep(120)")
                    sleep(120)
                break

            try:
                try:
                    package.fetch_metadata(fetch_pypi=False, fetch_repo=True)
                    package.fetch_commits()
                except Exception as e:
                    logger.error(
                        f"Error while fetching package details for {package.title}."
                    )
                    raise PackageUpdaterException(e, package.title)
            except PackageUpdaterException:
                logger.error(f"Unable to update {package.title}", exc_info=True)

            print(f"{__file__}::handle::sleep(1)")
            sleep(1)
        healthcheck(settings.PACKAGE_HEALTHCHECK_URL)
