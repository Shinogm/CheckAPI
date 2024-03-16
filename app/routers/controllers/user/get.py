from fastapi import HTTPException
from app.services.db import check_db

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