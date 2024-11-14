from typing import Any, Optional

from pydantic import BaseModel, Field, create_model


class BaseResponseMeta(BaseModel):
    code: int
    message: str

class PaginationResponseMeta(BaseResponseMeta):
    page: Optional[int] = Field(1, gt=0)
    size: Optional[int] = Field(10, ge=0)
    total: Optional[int] = Field(10, ge=0)


class ServiceResponse:

    def __init__(self, model: Any, auth: bool = False) -> None:
        self.model = model
        self.auth = auth

    def basic(self, route: str) -> dict:
        return {
            400: {
                "model": create_model(
                    route, code=(int, 400), message=(str, "Bad Request")
                ),
                "description": "Occurs when the request you make does not match or is invalid",
            },
            500: {
                "model": create_model(
                    route,
                    code=(int, 500),
                    message=(str, "Internal Server Error"),
                ),
                "description": "Occurs when there is an engine or lib error in the engine",
            },
        }

    def get(self, route: str, model: Any = None, obj: str = "Data", auth: bool = False, exclude_codes: list = [], **kwargs) -> dict:
        response: dict = {
            200: {
                "model": create_model(
                    route,
                    code=(int, 200),
                    message=(str, "Success"),
                    data=(model if model else self.model, ...),
                ),
                "description": "Success get data",
            },
            404: {
                "model": create_model(
                    route, code=(int, 404), message=(str, f"{obj} not found")
                ),
            },
            **self.basic(route),
            **kwargs
        }

        if exclude_codes:
            for code in exclude_codes:
                del response[code]
            

        if auth or self.auth:
            response[401] = {
                "model": create_model(
                    route, code=(int, 401), message=(str, "Unauthorized")
                )
            }
        
        return response



    def pagination(self, route: str, model: Any = None, obj: str = "Data", auth: bool = False, exclude_codes: list = [], **kwargs) -> dict:
        response: dict = {
            200: {
                "model": create_model(
                    route,
                    code=(int, 200),
                    message=(str, f"Success get all {obj}"),
                    data=(model if model else self.model, ...),
                    page=(int, 1),
                    size=(int, 10),
                    total=(int, 10),
                ),
            },
            404: {
                "model": create_model(
                    route, code=(int, 404), message=(str, f"{obj} not found")
                ),
            },
            **self.basic(route),
            **kwargs
        }

        if exclude_codes:
            for code in exclude_codes:
                del response[code]
            

        if auth or self.auth:
            response[401] = {
                "model": create_model(
                    route, code=(int, 401), message=(str, "Unauthorized")
                )
            }
        
        return response

    def creation(self, route: str, model: Any = None, obj: str = "Data", auth: bool = False, exclude_codes: list = [], **kwargs) -> dict:
        response: dict =  {
            201: {
                "model": create_model(
                    route,
                    code=(int, 201),
                    message=(str, f"{obj} created successfully"),
                    data=(model if model else self.model, ...),
                ),
            },
            **self.basic(route),
            **kwargs
        }

        if exclude_codes:
            for code in exclude_codes:
                del response[code]
            

        if auth or self.auth:
            response[401] = {
                "model": create_model(
                    route, code=(int, 401), message=(str, "Unauthorized")
                )
            }
        
        return response

    def update(self, route: str, model: Any = None, obj: str = "Data", auth: bool = False, exclude_codes: list = [], **kwargs) -> dict:
        response: dict =  {
            200: {
                "model": create_model(
                    route,
                    code=(int, 200),
                    message=(str, f"{obj} updated successfully"),
                    data=(model if model else self.model, ...),
                ),
            },
            204: {
                "model": create_model(
                    route,
                    code=(int, 204),
                    message=(str, f"{obj} updated successfully"),
                ),
            },
            **self.basic(route),
            **kwargs
        }

        if exclude_codes:
            for code in exclude_codes:
                del response[code]
            

        if auth or self.auth:
            response[401] = {
                "model": create_model(
                    route, code=(int, 401), message=(str, "Unauthorized")
                )
            }
        
        return response

    def delete(self, route: str, model: Any = None, obj: str = "Data", auth: bool = False, exclude_codes: list = [], **kwargs) -> dict:
        response: dict =  {
            200: {
                "model": create_model(
                    route,
                    code=(int, 200),
                    message=(str, f"{obj} delete successfully"),
                    data=(model if model else self.model, ...),
                ),
            },
            204: {
                "model": create_model(
                    route,
                    code=(int, 204),
                    message=(str, f"{obj} delete successfully"),
                ),
            },
            **self.basic(route),
            **kwargs
        }

        if exclude_codes:
            for code in exclude_codes:
                del response[code]
            

        if auth or self.auth:
            response[401] = {
                "model": create_model(
                    route, code=(int, 401), message=(str, "Unauthorized")
                )
            }
        
        return response
    