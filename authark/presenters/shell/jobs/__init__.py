from .notify import NotifyJob


JOBS = [value for key, value in globals().items() if key.endswith('Job')]
