from fastapi import HTTPException, Depends
from app.models.user import User
from app.services.db import check_db

async def create_user(user: User = Depends(User.as_form)):
    try:
        user_id = check_db.insert(
            table='users',
            data={
                'name': user.name,
                'domicilio': user.domicilio,
                'telefono': user.telefono,
                'empresa': user.empresa,
                'email': user.email,
                'password': user.password if user.password else ''
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, 
            detail='An error occurred while creating the development.'
        )
    return {
        'id': user_id,
        'name': user.name,
        'domicilio': user.domicilio,
        'telefono': user.telefono,
        'empresa': user.empresa,
        'email': user.email
    }