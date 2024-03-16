from fastapi import HTTPException
from app.services.db import check_db
from app.routers.controllers.user.identify import indentity

async def get_all_users():
    users_and_perm = check_db.fetch_all(
        sql='''
            SELECT
                u.id,
                u.created_at,
                u.name,
                u.domicilio,
                u.telefono,
                u.empresa,
                u.email,
                p.name AS permission
            FROM
                users AS u
            JOIN
                user_perms AS up ON u.id = up.user_id
            JOIN
                permissions AS p ON up.perm_id = p.id
            '''
    )


    if not users_and_perm:
        raise HTTPException(status_code=404, detail='Users not found')
    
    return {
        'status': 'success',
        'users': users_and_perm,
    }

async def get_all_user_by_perm_id(perm_id: int):
    users_and_perm = check_db.fetch_all(
        sql='''
            SELECT
                u.id,
                u.created_at,
                u.name,
                u.domicilio,
                u.telefono,
                u.empresa,
                u.horario,
                u.email,
                p.name AS permission
            FROM 
                users AS u
            JOIN 
                user_perms AS up ON u.id = up.user_id
            JOIN 
                permissions AS p ON up.perm_id = p.id
            WHERE 
                up.perm_id = %s
            ''',
        params=(perm_id,)
    )

    if not users_and_perm:
        raise HTTPException(status_code=404, detail='Users not found')
    
    return {
        'status': 'success',
        'users': users_and_perm,
    }
from typing import Dict, Any

async def get_horario_by_scan() -> Dict[str, Any]:
    try:
        user = await indentity()
        if user is None:
            raise HTTPException(status_code=404, detail='User not found')
        
        if not isinstance(user, dict):
            raise TypeError("Expected 'user' to be a dictionary")

        user_data = user.get('user')
        if not user_data:
            raise HTTPException(status_code=404, detail='User data not found')

        if not isinstance(user_data, dict):
            raise TypeError("Expected 'user_data' to be a dictionary")

        user_id = user_data.get('id')
        if not user_id:
            raise HTTPException(status_code=404, detail='User ID not found')

        select = check_db.fetch_one(
            sql='SELECT horario FROM users WHERE id = %s',
            params=(user_id,)  
        )
        
        if not select:
            raise HTTPException(status_code=404, detail='User not found')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Internal server error getting horario by scan.')
    return {
        'status': 'success',
        'horario': select,
        'user': user_data
    }





