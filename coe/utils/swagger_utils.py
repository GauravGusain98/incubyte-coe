from fastapi.openapi.utils import get_openapi

def custom_openapi():
    from main import app

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="COE App API Docs",
        version="1.0.0",
        routes=app.routes,
    )

    # Define cookie-based authentication
    openapi_schema["components"]["securitySchemes"] = {
        "CookieAuth": {
            "type": "apiKey",
            "in": "cookie",
            "name": "access_token",
        }
    }

    # Apply security scheme to all non-public routes
    for path, path_item in openapi_schema["paths"].items():
        for method, operation in path_item.items():
            is_public = operation.get("is_public", False)
            if not is_public:
                operation["security"] = [{"CookieAuth": []}]
            else:
                operation.pop("security", None)

    app.openapi_schema = openapi_schema
    return app.openapi_schema