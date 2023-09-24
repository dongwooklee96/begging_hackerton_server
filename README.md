# Ddip - Backend


### How to Start Server
```bash
# EC2 ssh 접속
# pem키 받아서 저장한 위치로 이동 후 접속
$ sudo ssh -i "ddip.pem" ubuntu@ec2-13-125-131-81.ap-northeast-2.compute.amazonaws.com

# root 계정으로 전환 후 서버 코드있는 디렉토리로 이동
## ERROR:    Error loading ASGI app. Could not import module "main". 오류발생시 현재 디렉토리 확인하기
$ sudo -i 
$ cd ddip-server/

# 서버 실행
$ uvicorn main:app

################# 참고 #################
# CI/CD 미구현으로 서버 코드 git 변동 사항 발생 시 pull 받아줘야함
$ git pull

# nginx 중지
$ service nginx restart

# nginx 환경설정 파일
$ cd
$ vi /etc/nginx/sites-enabled/default

# fast api 환경설정 파일
$ cd
$ vi /etc/nginx/sites-enabled/fastapi_nginx

```











# vinyl_search_server

```python
from fastapi import APIRouter, Path, Query, HTTPException, status


todo_router = APIRouter()

todo_list = []


@todo_router.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(todo: TodoItem) -> dict:
    todo_list.append(todo)
    return {
        "message": "Todo added successfully"
    }


@todo_router.get("/todo", response_model=TodoItems)
async def retrieve_todos() -> dict:
    return {
        "todos": todo_list
    }


@todo_router.get("/todo/{todo_id}")
async def get_single_todo(todo_id: int = Path(..., title="The ID of the todo to retrieve.")) -> dict:
    # for todo in todo_list:
    #     if todo.id == todo_id:
    #         return {
    #             "todo": todo
    #         }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Todo with supplied ID doesn't exist")


@todo_router.put("/todo/{todo_id}")
async def update_todo(todo_data: TodoItem, todo_id: int = Path(..., title="The ID of the todo to update.")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return {
                "message": "Todo updated successfully"
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Todo with supplied ID doesn't exist")


@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(todo_id: int) -> dict:
    for index in range(len(todo_list)):
        todo = todo_list[index]
        if todo.id == todo_id:
            todo_list.pop(index)
            return {
                "message": "Todo deleted successfully"
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Todo with supplied ID doesn't exist")


```
