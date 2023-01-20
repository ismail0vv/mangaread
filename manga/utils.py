from uuid import uuid4


class MangaUtils:
    def manga_photo_path(instance, filename):
        ext = filename.split('.')[-1]
        return 'manga/{}.{}'.format(uuid4().hex, ext)
