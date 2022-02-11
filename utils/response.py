from fastapi.responses import JSONResponse, HTMLResponse
from typing import Union, overload, Dict
import os


@overload
def response(data: Dict[str, str], status: int = ...) -> JSONResponse:
    ...


@overload
def response(data: str, status: int = ...) -> HTMLResponse:
    ...


def response(
    data: Union[Dict[str, str], str], status: int = 200
) -> Union[JSONResponse, HTMLResponse]:

    if isinstance(data, dict):
        data.update({"status": status})
        return JSONResponse(data, status_code=status)

    if isinstance(data, str):
        with open(os.path.join("templates", data)) as f:
            return HTMLResponse(f.read(), status_code=status)
