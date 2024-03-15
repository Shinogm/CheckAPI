from fastapi import HTTPException
from app.services.db import check_db

async def get_all_users():
    users_and_perm = check_db.fetch_all(
        sql='''
            SELECT
                user.id,
                user.created_at,
                user.name,
                user.domicilio,
                user.telefono,
                user.empresa,
                user.email
                permissions.name AS permission
            FROM users user
            JOIN permissions ON permissions.id = user.permission_id
            '''
    )

    if not users_and_perm:
        raise HTTPException(status_code=404, detail='Users not found')
    
    return {
        'status': 'success',
        'users': users_and_perm,
    }

async def get_all_user_by_perm_id(perrm_id: int | None = 2):
    users_and_perm = check_db.fetch_all(
        sql='''
            SELECT
                user.id,
                user.created_at,
                user.name,
                user.domicilio,
                user.telefono,
                user.empresa,
                user.email
                permissions.name AS permission
            FROM users user
            JOIN permissions ON permissions.id = user.permission_id
            WHERE user.permission_id = %s
            ''',
        params=(perrm_id,)
    )

    if not users_and_perm:
        raise HTTPException(status_code=404, detail='Users not found')
    
    return {
        'status': 'success',
        'users': users_and_perm,
    }