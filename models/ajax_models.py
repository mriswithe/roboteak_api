from typing import Dict, List, Optional

from pydantic import BaseModel, constr, Field


class AjaxSearch(BaseModel):
    value: str
    regex: bool


class AjaxOrder(BaseModel):
    column: int
    dir: constr(regex=r"^(asc|desc)$")


class AjaxColumn(BaseModel):
    data: Optional[str]
    name: str
    orderable: bool
    searchable: bool
    search: AjaxSearch


class AjaxRequest(BaseModel):
    draw: int
    start: int
    length: int
    order: List[AjaxOrder]
    columns: List[AjaxColumn]


class AjaxResponse(BaseModel):
    draw: int
    records_filtered: int = Field(..., alias="recordsFiltered")
    records_total: int = Field(..., alias="recordsTotal")
    data: List[Dict]
