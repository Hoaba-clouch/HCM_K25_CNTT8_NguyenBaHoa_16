from fastapi import FastAPI, Depends, Request, Query
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from database import get_db
from schema import create_response, TaskCreate, TaskUpdate, TaskResponse
import task_service

app = FastAPI(
    title="Task Management API",
    description="Hệ thống quản lý công việc trong dự án",
    version="1.0.0"
)
@app.get("/")
def check_server(request: Request):
    return create_response(
        status_code=200,
        message="API đang chạy",
        data=None,
        error=None,
    )

@app.get("/tasks")
def get_tasks(request: Request, db: Session = Depends(get_db)):
    try:
        tasks = task_service.get_all_tasks(db)
        data_list = [TaskResponse.model_validate(t).model_dump() for t in tasks]
    except Exception as exc:
        db.rollback()
        return create_response(
            status_code=500,
            message="Lỗi hệ thống khi lấy danh sách công việc",
            data=None,
            error=str(exc),
        )
    else:
        return create_response(
            status_code=200,
            message="Lấy danh sách công việc thành công",
            data=data_list,
            error=None,
        )


@app.get("/tasks/search")
def search_tasks(
    request: Request, 
    status: str = Query(..., description="Từ khóa trạng thái cần tìm kiếm gần đúng"), 
    db: Session = Depends(get_db)
):
    try:
        tasks = task_service.search_tasks_by_status(db, status)
        data_list = [TaskResponse.model_validate(t).model_dump() for t in tasks]
    except Exception as exc:
        db.rollback()
        return create_response(
            status_code=500,
            message="Lỗi hệ thống khi tìm kiếm công việc",
            data=None,
            error=str(exc),
         
        )
    else:
        return create_response(
            status_code=200,
            message="Tìm kiếm công việc thành công",
            data=data_list,
            error=None,
        )
@app.get("/tasks/{task_id}")
def get_task_detail(request: Request, task_id: int, db: Session = Depends(get_db)):
    try:
        task = task_service.get_task_by_id(db, task_id)
    except Exception as exc:
        db.rollback()
        return create_response(
            status_code=500,
            message="Lỗi hệ thống khi lấy chi tiết công việc",
            data=None,
            error=str(exc)
            
        )
    else:
        if not task:
            return create_response(
                status_code=404,
                message="Không tìm thấy công việc",
                data=None,
                error="Not Found"
            )
        return create_response(
            status_code=200,
            message="Lấy chi tiết công việc thành công",
            data=TaskResponse.model_validate(task).model_dump(),
            error=None
        )

@app.post("/tasks")
def create_new_task(request: Request, payload: TaskCreate, db: Session = Depends(get_db)):
    try:
        db_task = task_service.create_task(db, payload)
    except Exception as exc:
        db.rollback()
        return create_response(
            status_code=500,
            message="Lỗi hệ thống khi thêm công việc",
            data=None,
            error=str(exc)
        )
    else:
        db.commit()
        db.refresh(db_task)
        return create_response(
            status_code=201,
            message="Thêm công việc thành công",
            data=TaskResponse.model_validate(db_task).model_dump(),
            error=None
        )

@app.put("/tasks/{task_id}")
def update_existing_task(request: Request, task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    try:
        task = task_service.get_task_by_id(db, task_id)
        if not task:
            return create_response(
                status_code=404,
                message="Không tìm thấy công việc",
                data=None,
                error="Not Found"
            )
        db_task = task_service.update_task(db, task, payload)
    except Exception as exc:
        db.rollback()
        return create_response(
            status_code=500,
            message="Lỗi hệ thống khi cập nhật công việc",
            data=None,
            error=str(exc)
        )
    else:
        db.commit()
        db.refresh(db_task)
        return create_response(
            status_code=200,
            message="Cập nhật công việc thành công",
            data=TaskResponse.model_validate(db_task).model_dump(),
            error=None
        )

@app.delete("/tasks/{task_id}")
def delete_existing_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    try:
        task = task_service.get_task_by_id(db, task_id)
        if not task:
            return create_response(
                status_code=404,
                message="Không tìm thấy công việc",
                data=None,
                error="Not Found"
            )
        task_service.delete_task(db, task)
    except Exception as exc:
        db.rollback()
        return create_response(
            status_code=500,
            message="Lỗi hệ thống khi xóa công việc",
            data=None,
            error=str(exc)
        )
    else:
        db.commit()
        return create_response(
            status_code=200,
            message="Xóa công việc thành công",
            data=None,
            error=None
          
        )
