class Permission:
    def __init__(self, **attributes) -> None:
        self.id = attributes.get('id', '')
        self.policy_id = attributes['policy_id']
        self.resource_id = attributes['resource_id']
