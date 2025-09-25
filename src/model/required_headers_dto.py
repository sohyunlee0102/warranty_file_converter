from dataclasses import dataclass


@dataclass
class RequiredHeadersDto:
    MBMU: list[str]
    SBMU: list[str]
