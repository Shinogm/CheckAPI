from fastapi import HTTPException, Depends
from app.services.db import check_db
from app.models.user import ModifyUser

async def modify_user(user_id: int, user: ModifyUser = Depends(ModifyUser.as_form), hora: str | None = None, fecha: str | None = None):
    try:
        pre_sql = f'Tu horario es el siguiente: de {hora} de los días {fecha}' if (hora and fecha) else 'No se ha establecido un horario.'

        get_user = check_db.fetch_one(
            sql='SELECT id, name, email, domicilio, telefono, empresa, created_at, horario FROM users WHERE id = %s',
            params=(user_id,)
        )
        if not get_user:
            raise HTTPException(status_code=404, detail='User not found')

        new_user = check_db.execute(
            sql='UPDATE users SET name = %s, email = %s, domicilio = %s, telefono = %s, empresa = %s, horario = %s WHERE id = %s',
            params=(user.name if user.name else get_user['name'],
                     user.email if user.email else get_user['email'],
                       user.domicilio if user.domicilio else get_user['domicilio'],
                         user.telefono if user.telefono else get_user['telefono'],
                           user.empresa if user.empresa else get_user['empresa'],
                             pre_sql if pre_sql else get_user['horario'], user_id
                             )
        )

        get_new_user = check_db.fetch_one(
            sql='SELECT id, name, email, domicilio, telefono, empresa, created_at, horario FROM users WHERE id = %s',
            params=(user_id,)
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Internal server error modifying user.')

    return {
        'status': 'success',
        'message': f'User modified: {get_new_user}'
        }
