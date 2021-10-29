from fastapi import APIRouter


router = APIRouter()


@router.head('/health')
def health_check():
    return True
