from app.services.fastapi import App
from app.models.static_dir import StaticDir
from app.routers.router import users

def main():
    app = App(
    routers=[
        users.router
    ],
    static_dirs=[
        StaticDir(name='public', path='public')
    ]
    ).get_app()

    return app
if __name__ == '__main__':
    app = main()
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=3001)
