from typing import TYPE_CHECKING
from fastapi_pagination import Page as BasePage
from fastapi_pagination.customization import CustomizedPage, UseParamsFields

if TYPE_CHECKING:
    Page = BasePage
else:
    Page = CustomizedPage[
        BasePage, 
        UseParamsFields(size=10)
    ]