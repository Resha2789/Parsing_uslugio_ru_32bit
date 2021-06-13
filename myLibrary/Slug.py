import re
import unidecode


class Slugify:
    def __init__(self):
        self.slug_text = ''

    def slugify(self, text):
        self.slug_text = unidecode.unidecode(text).lower()
        return re.sub(r'[\W_]+', '-', self.slug_text)
