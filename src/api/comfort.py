from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.comfort import ComfortAdd

router = APIRouter(prefix="/facilities", tags=['Удобства'])

@router.get('', summary="Получить список всех удобств")
async def get_all_facilities(db: DBDep):
    return await db.comfort.get_all()

@router.post('', summary="Добавить новое удобство")
async def add_facility(db: DBDep, ComfortData: ComfortAdd = Body()):
    comfort = await db.comfort.add(ComfortData)
    await db.commit()
    return {"status": "200", "data": comfort}