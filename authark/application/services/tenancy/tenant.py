
class Tenant:
    def __init__(self, **attributes):
        self.id = attributes.get('id', '')
        self.name = attributes.get('name', '')
        self.email = attributes.get('email', '')
        self.external_id = attributes.get('external_id', '')
        self.external_source = attributes.get('external_source', '')
        self.attributes = attributes.get('attributes', {})
