import os

class FileFinder:
    def __init__(self, path, allowed_extensions = [ 'jpg', 'jpeg', 'png', 'gif', 'avi', 'mov', 'mp4', '3gp', 'm4v', 'bmp', 'm2ts']) -> None:
        if not os.path.isdir(path):
            print("\nERROR: {} is not a directory.".format(path))
            exit(1)

        self.path = path
        self.allowed_extensions = allowed_extensions

    def find_media_files(self):
        files = []
        for dirname, dirnames, filenames in sorted(os.walk(self.path)):

            if os.path.basename(dirname).startswith('_'):
                continue

            for filename in filenames:
                file = os.path.join(dirname, filename)
                ext = str(os.path.splitext(file)[1]).lower().replace('.', '')
                if ext in self.allowed_extensions:
                    files.append(
                        {
                            'name': os.path.basename(file),
                            'path': file,
                            'extension': ext,
                            'album': os.path.basename(dirname),
                            'album_path': dirname,
                            'date_modified': os.path.getmtime(file),
                        }
                    )


        return sorted(files, key=lambda k: k['date_modified'], reverse=True)
