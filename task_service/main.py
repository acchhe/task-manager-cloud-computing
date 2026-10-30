from fastapi import FastAPI,HTTPException
from models import TaskCreate
import uuid
from database import tasks_collection
from bson import ObjectId 
# Allows us to search for tasks using their id


app = FastAPI()
tasks = []

@app.get("/")
def control():
    return {"message": "Welcome"}

@app.get("/tasks")
def return_tasks():
    tasks = []

    for task in tasks_collection.find():
        task["id"] = str(task.pop("_id"))
        tasks.append(task)
    return tasks
 
    

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    dict_task = task.model_dump()

    result = tasks_collection.insert_one(dict_task)

    dict_task.pop("_id")
    dict_task["id"] = str(result.inserted_id)

    return dict_task


@app.get("/tasks/{task_id}")
def get_task(task_id: str):

    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=404,detail="ID not valid")

    mongo_id = ObjectId(task_id)


    result = tasks_collection.find_one({"_id" : mongo_id})

    if result is None:
        raise HTTPException(status_code=404,detail="Task not found")

    result["id"] = str(result.pop("_id"))

    return result




@app.put("/tasks/{task_id}")
def put_task(task_id: str, updated_task: TaskCreate):

    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=404, detail="Invalid input")

    updated_data = updated_task.model_dump()

    mongo_id = ObjectId(task_id)

    result = tasks_collection.update_one(
        {"_id": mongo_id},
        {"$set": updated_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    task = tasks_collection.find_one({"_id": mongo_id})

    task["id"] = str(task.pop("_id"))

    return task


@app.delete("/tasks/{task_id}",status_code=204)
def del_task(task_id: str):

    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=404,detail="Task not found")

    mongo_id = ObjectId(task_id)

    result = tasks_collection.delete_one({"_id" : mongo_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404,detail="Task not found")

    return
        



    




