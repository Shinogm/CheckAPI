from app.services.db import check_db
from fastapi import HTTPException

def verify_password( email: str, password: str):
    user_db = check_db.fetch_one(
        sql='SELECT * FROM users WHERE email = %s',
        params=(email,)
    )
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    user_db_all = check_db.fetch_one(
        sql='SELECT id, created_at, name, domicilio, telefono, empresa, email FROM users WHERE email = %s',
        params=(email,)
    )
    try:
        import bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), user_db['password'].encode('utf-8')):
        #password == user_db['password']:
            return {
                'message': 'Password correct',
                'token': user_db_all
            }
        else:
            print(f"{user_db['password']} != {bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())}")
            raise HTTPException(status_code=404, detail='Password incorrect')
    except:
        raise HTTPException(status_code=404, detail='User not found')