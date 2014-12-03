import os
import shutil
import zipfile

from django.conf import settings
from django.core.management.base import BaseCommand

from clint.textui import progress
import requests
import sunlight


class Command(BaseCommand):
    help = u'Download the raw JSON data from Open States.'

    def handle(self, *args, **kwargs):
        self.clean_download_folder()
        self.download_file()
        self.unzip_file()

    def clean_download_folder(self):
        try:
            shutil.rmtree(settings.DOWNLOAD_DIR)
        except OSError:
            self.stderr.write('Data folder doesn\'t exist! Creating now.')

        os.mkdir(settings.DOWNLOAD_DIR)

    def get_latest_download_url(self):
        return sunlight.openstates.state_metadata('tx')['latest_json_url']

    def download_file(self):
        """
        Download the ZIP file.
        """

        req = requests.get(self.get_latest_download_url(), stream=True)
        file_length = int(req.headers.get('content-length'))

        self.stdout.write('Downloading ZIP file...')
        with open(settings.DOWNLOAD_PATH, 'wb') as fo:
            for chunk in progress.bar(req.iter_content(1024),
                                      expected_size=(file_length/1024) + 1):
                if chunk:
                    fo.write(chunk)
                    fo.flush()

    def unzip_file(self):
        """
        Unzip the downloaded ZIP file.
        """
        self.stdout.write('Unzipping file...')

        zfile = zipfile.ZipFile(settings.DOWNLOAD_PATH)
        extract_path = os.path.join(settings.DOWNLOAD_DIR)

        zfile.extractall(extract_path)

        self.stdout.write('Done!')
