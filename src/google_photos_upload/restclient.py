from .oauth import OAuth

class RestClient:
    def __init__(self, credentials) -> None:
        self.auth = OAuth(credentials)
        self.auth.authorize()

    def upload_file(self, file_path):
        return self.auth.make_upload('POST', 'https://photoslibrary.googleapis.com/v1/uploads', file_path )

    def create_album(self, album_title):
        return self.auth.make_request('POST', 'https://photoslibrary.googleapis.com/v1/albums', { 'album': { 'title': album_title}})

    def add_to_album(self, file_name, file_id, album_id):
        data = {
            'albumId': album_id,
            'newMediaItems': [{
                'description': '',
                'simpleMediaItem': { 'uploadToken': file_id, 'fileName': file_name}
            }]
        }

        return self.auth.make_request('POST', 'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate', data)
