import base64
import binascii
from domain.interfaces.link_interface import LinkDecoder


class FastAPILinkDecoder(LinkDecoder):
    def decode(self, encoded: str) -> str:
        try:
            decoded_bytes = base64.urlsafe_b64decode(encoded)
            return decoded_bytes.decode("utf-8")
        except (
            binascii.Error,
            UnicodeDecodeError,
            ValueError,
            TypeError,
            OverflowError,
        ):
            raise ValueError("Invalid link format")
