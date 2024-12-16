import os
import json
from alive_progress import alive_it
from argparse import ArgumentParser
from .filefinder import FileFinder
from .database import Database
from .restclient import RestClient

class GphotosUpload:
    def __init__(self) -> None:
        self.parser = self.get_arguments()
        args = self.parser.parse_args()
        self.path = os.path.abspath(args.path)
        self.credentials = os.path.abspath(args.credentials)
        self.timeout = args.timeout

    def get_arguments(self) -> ArgumentParser:
        parser = ArgumentParser(description = __name__)
        parser.add_argument(
            'path',
            help = 'The path where the pictures are stored'
        )

        parser.add_argument(
            '--credentials',
            help = 'Path to credentials.json with oauth information'
        )

        parser.add_argument(
            '--timeout',
            type = int,
            help = 'Timeout for uploading a single item in seconds'
        )

        parser.add_argument(
            '--version', action='version', version='{} {}'.format('Google Photos Uploader', '0.3.0')
        )

        return parser

    def start(self) -> None:
        if None in (self.path, self.credentials):
            self.parser.print_help()
            print("\nERROR: Missing arguments.")
            exit(1)

        if not os.path.isfile(self.credentials):
            self.parser.print_help()
            print("\nERROR: {} is not a credentials file.".format(self.credentials))
            exit(1)

        stats = {
            'files_uploaded': 0,
            'files_failed': 0,
            'files_already_uploaded': 0,
        }

        database = Database(self.path)
        items = FileFinder(self.path).find_media_files()
        rest = RestClient(self.credentials)
        for item in alive_it(items):
            file_data = database.get_file(item.get('path'))
            if file_data is not None:
                stats['files_already_uploaded'] += 1
                continue;

            album_data = database.get_album(item.get('album_path'))
            if album_data is None:
                ret = rest.create_album(item.get('album'))
                if ret.status_code == 200:
                    data = json.loads(ret.content)
                    database.add_album(item.get('album'), item.get('album_path'), data['id'], data['productUrl'])
                    album_data = database.get_album(item.get('album_path'))
                else:
                    print('Error: Album creation failed. {}'.format(ret.content.decode('utf-8')))
                    continue

            album_id = album_data[0][2]
            ret = rest.upload_file(item.get('path'), self.timeout)
            if ret.status_code == 200:
                file_id = str(ret.content.decode('utf-8'))
                ret = rest.add_to_album(item.get('name'), file_id, album_id)
                if ret.status_code == 200:
                    database.add_file(item.get('name'), item.get('path'), item.get('album'), file_id, json.dumps(ret.content.decode('utf-8')))
                    stats['files_uploaded'] += 1
                else:
                    print('Error: Adding file to album failed. {} / {}'.format(item.get('path'), ret.content.decode('utf-8')))
                    stats['files_failed'] += 1
            else:
                print('Error: Uploading file failed. {} / {}'.format(item.get('path'), ret.content.decode('utf-8')))

        print('Files uploaded: {}'.format(stats['files_uploaded']))
        print('Files failed: {}'.format(stats['files_failed']))
        print('Files already uploaded: {}'.format(stats['files_already_uploaded']))
