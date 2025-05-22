from fastapi.openapi.utils import get_openapi

def custom_openapi():
    from main import app

    PUBLIC_ENDPOINTS = [
        ("/user/login", "post"),
        ("/user/register", "post"),
        ("/user/token/refresh", "post"),
        ("/hello-world", "get"),
    ]

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
        for method in path_item:
            if (path, method) not in PUBLIC_ENDPOINTS:
                path_item[method]["security"] = [{"BearerAuth": []}]
            else:
                path_item[method].pop("security", None)

    app.openapi_schema = openapi_schema
    return app.openapi_schema