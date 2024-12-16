import os
from setuptools import setup, find_packages

DEPENDENCIES = ( 'google_auth_oauthlib', 'requests_oauthlib', 'alive_progress' )

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'google_photos_upload',
    version = '0.3.0',
    author = "Michael Pratt",
    author_email = "author@michaelpratt.dev",
    description = ( "Upload media files to Google Photos" ),
    license = "MIT",
    keywords = "Google Photos Upload client albums media",
    include_package_data=True,
    url = "https://github.com/mpratt/google-photos-upload",
    packages = find_packages(),
    package_dir = { '' : 'src' },
    long_description = read('README.md'),
    long_description_content_type="text/markdown",
    install_requires=DEPENDENCIES,
    entry_points = {
        'console_scripts': [ 'google-photos-upload = google_photos_upload.cli:start' ],
    },
)
