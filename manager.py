from pathlib import Path

import fire


class DBTools:
    async def init(self) -> None:
        from app.api.deps import async_db_context
        from app.command import insert_default_data
        async with async_db_context() as session:
            await insert_default_data(session)


class Tools:
    def __init__(self) -> None:
        self.db = DBTools()

    def runserver(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            workers=1,
            reload=True,
            reload_dirs=[Path('app').absolute().as_posix()]
        )


if __name__ == '__main__':
    fire.Fire(Tools)
