from typing import Dict, List, Literal

from pydantic import BaseModel, Field


class AjaxSearch(BaseModel):
    value: str
    regex: bool


class AjaxOrder(BaseModel):
    column: int
    dir: Literal["asc", "desc"]


class AjaxColumn(BaseModel):
    data: str
    name: str
    orderable: bool
    searchable: bool
    search: AjaxSearch
    order: AjaxOrder


class AjaxRequest(BaseModel):
    draw: int
    start: int
    length: int
    order: AjaxOrder
    columns: List[AjaxColumn]


class AjaxResponse(BaseModel):
    draw: int
    records_filtered: int = Field(..., alias="recordsFiltered")
    records_total: int = Field(..., alias="recordsTotal")
    data: List[Dict]
