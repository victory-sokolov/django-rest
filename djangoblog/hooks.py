from copy import deepcopy

def remove_schema_endpoints(result, generator, request, public):

    exclude_paths = ["/api/schema/"]
    swagger_doc = deepcopy(result)

    for key, value in result["paths"].items():
        if key in exclude_paths:
            swagger_doc["paths"].pop(key)

    return swagger_doc
