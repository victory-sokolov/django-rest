from copy import deepcopy
from typing import Any


def remove_schema_endpoints(
    result: dict[str, Any],
    generator: Any,
    request: Any,
    public: Any,
) -> dict[str, Any]:
    exclude_paths = [
        "/api/schema/",
        "/schema/",
        "/schema.json",
        "/v1/schema.json",
        "/v2/schema.json",
        "/api/v1/schema.json",
        "/api/v2/schema.json",
    ]
    swagger_doc = deepcopy(result)

    for key, _ in result["paths"].items():
        if key in exclude_paths:
            swagger_doc["paths"].pop(key)

    return swagger_doc
