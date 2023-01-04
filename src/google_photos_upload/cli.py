from .main import GphotosUpload

def start():
    uploader = GphotosUpload()
    uploader.start()

if __name__ == "__main__":
    start()
