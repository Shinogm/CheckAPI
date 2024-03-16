from fastapi import HTTPException, Depends
from app.models.user import User
from app.services.db import check_db
import bcrypt
async def create_user(user: User = Depends(User.as_form), hora: str | None = None, fecha: str | None = None):

    pre_sql = f'Tu horario es el siguiente: de {hora} de los días {fecha}' if (hora and fecha) else 'No se ha establecido un horario.'

    try:
        user_id = check_db.insert(
            table='users',
            data={
                'name': user.name,
                'domicilio': user.domicilio,
                'telefono': user.telefono,
                'empresa': user.empresa,
                'email': user.email,
                'horario': pre_sql,
                'password': bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()) if user.password else ''
            }
        )


        get_user = check_db.fetch_one(
            sql="SELECT * FROM users WHERE id = %s",
            params=(user_id,)
        )

        if not get_user:
            raise HTTPException(
                status_code=404, 
                detail='User not found'
            )

        if get_user['password'] and get_user:
            user_permission = check_db.insert(
                table='user_perms',
                data={
                    'user_id': user_id,
                    'perm_id': 1
                }
            )

        else:
            user_permission = check_db.insert(
                table='user_perms',
                data={
                    'user_id': user_id,
                    'perm_id': 2
                }
            )

        selec_user_all_data_and_perm_type = check_db.fetch_all(
            sql="SELECT u.id, u.name, u.domicilio, u.telefono, u.horario, u.empresa, u.email, p.name AS perm_type FROM users u INNER JOIN user_perms up ON u.id = up.user_id INNER JOIN permissions p ON up.perm_id = p.id WHERE u.id = %s",
            params=(user_id,)
        )


    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, 
            detail='Error creating user'
        )
    return {
        'status': 'success',
        'message': 'User created successfully',
        'user': selec_user_all_data_and_perm_type
    }