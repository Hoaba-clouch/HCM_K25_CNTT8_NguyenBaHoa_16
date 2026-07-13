from datetime import datetime
from typing import Any, Optional
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

def create_response(status_code: int, message: str, data: Any = None, error: Any = None, path: str = ""):
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "error": error,
            "message": message,
            "data": data,
          
        }
    )

class TaskBase(BaseModel):
    title: str = Field(..., description="Tiêu đề công việc")
    assignee_name: str = Field(..., description="Người phụ trách")
    priority: str = Field(..., description="Mức độ ưu tiên")
    status: str = Field(..., description="Trạng thái công việc")

    @field_validator("title", "assignee_name", "priority", "status")
    @classmethod
    def prevent_empty_or_whitespace(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Trường thông tin không được để trống hoặc chỉ chứa khoảng trắng")
        return stripped

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskResponse(BaseModel):
    id: int
    title: str
    assignee_name: str
    priority: str
    status: str

    model_config = ConfigDict(from_attributes=True)
