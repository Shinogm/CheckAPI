from fastapi import HTTPException
from app.services.db import check_db

async def get_perms():
    perms = check_db.fetch_all(
        sql='''
            SELECT
                id, name
            FROM permissions
            '''
    )

    if not perms:
        raise HTTPException(status_code=404, detail='Permissions not found')
    
    return {
        'status': 'success',
        'permissions': perms,
    }