

class NoExifDataError(Exception):
    """
    Thrown when an image does not have exif data
    """
    def __init__(self, message):
        self.message = message
