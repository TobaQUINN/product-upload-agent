from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from src.api.routes import router


app = FastAPI(
    title="Product Upload Agent",
    description="AI-assisted product listing preparation agent.",
    version="1.0.0",
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    for component in schema.get("components", {}).get("schemas", {}).values():
        for prop in component.get("properties", {}).values():

            # Multiple uploaded files
            if prop.get("type") == "array":
                items = prop.get("items", {})

                if items.get("contentMediaType") == "application/octet-stream":
                    items.pop("contentMediaType", None)
                    items["format"] = "binary"

            # Single uploaded file
            if (
                prop.get("type") == "string"
                and prop.get("contentMediaType")
                == "application/octet-stream"
            ):
                prop.pop("contentMediaType", None)
                prop["format"] = "binary"

    app.openapi_schema = schema

    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(router)
