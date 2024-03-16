from fastapi import HTTPException
from app.services.db import check_db

async def delete_user(user_id: int):
    
    get_user = check_db.fetch_one(
        sql='SELECT id, name, email, domicilio, telefono, empresa, created_at FROM users WHERE id = %s',
        params=(user_id,)
    )
    if not get_user:
        raise HTTPException(status_code=404, detail='User not found')

    check_db.execute(
        sql='DELETE FROM users WHERE id = %s',
        params=(user_id,)
    )

    return {
        'status': 'success',
        'message': f'User deleted, id: {get_user["id"]}, name: {get_user["name"]}, email: {get_user["email"]}, domicilio: {get_user["domicilio"]}, telefono: {get_user["telefono"]}, empresa: {get_user["empresa"]}, created_at: {get_user["created_at"]}'
        }