from fastapi import APIRouter

router = APIRouter(prefix="/counter")


@router.get(path='/')
def get_all():
    pass
