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

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path, path_item in openapi_schema["paths"].items():
        for method, operation in path_item.items():
            print(method, operation)
            is_public = operation.get("is_public", False)
            
            if not is_public:
                operation["security"] = [{"BearerAuth": []}]
            else:
                operation.pop("security", None)

    app.openapi_schema = openapi_schema
    return app.openapi_schema