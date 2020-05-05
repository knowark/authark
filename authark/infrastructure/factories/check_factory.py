from ..core.common import Config
from .crypto_factory import CryptoFactory


class CheckFactory(CryptoFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
