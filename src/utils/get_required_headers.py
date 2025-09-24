from typing import Any


def getRequiredHeaders(driverConfig: dict[str, Any]) -> dict[str, list[str]]:
    mbmuDriverConfig = driverConfig.get("MBMU", {})
    sbmuDriverConfig = driverConfig.get("SBMU", {})

    requiredMbmuHeaders: list[str] = []
    for key, value in mbmuDriverConfig.items():
        if isinstance(value, dict) and value.get("required") is True:
            requiredMbmuHeaders.append(key.upper())

    requiredSbmuHeaders: list[str] = []
    for key, value in sbmuDriverConfig.items():
        if isinstance(value, dict) and value.get("required") is True:
            requiredSbmuHeaders.append(key.upper())

    return {
        "MBMU": requiredMbmuHeaders,
        "SBMU": requiredSbmuHeaders,
    }
