import time


class Tenant:
    def __init__(self, **attributes):
        self.id = attributes.get('id', '')
        self.created_at = int(time.time())
        self.updated_at = int(time.time())
        self.name = attributes['name']
        self.email = attributes.get('email', '')
        self.active = attributes.get('active', True)
        self.slug = self._normalize_slug(attributes.get('slug', self.name))

    @staticmethod
    def _normalize_slug(slug: str) -> str:
        return slug
