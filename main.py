from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from threading import Thread
from manager import Process_manager

PROCESSED_INFO = None

def start_program():
    global PROCESSED_INFO
    manager = Process_manager()
    PROCESSED_INFO = manager.run_process()


@asynccontextmanager
async def lifespan(app: FastAPI):
    program = Thread(target=start_program, daemon=True)
    program.start()
    yield

app = FastAPI(lifespan=lifespan)


@app.get('/')
def root():
    return {"message:": "API of malicious text, "
                        "by path /documents You will receive the processed documents."}


@app.get('/documents')
async def get_documents():
    if PROCESSED_INFO is not None:
        return PROCESSED_INFO
    else:
        return {"message:": "the documents have not yet been processed. "
                            "wait a few minutes and try again." }


@app.get('/documents_with_some_weapons')
async def get_documents_with_some_weapons():
    if PROCESSED_INFO is not None:
        return PROCESSED_INFO
    else:
        return {"message:": "the documents have not yet been processed. "
                            "wait a few minutes and try again." }



if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8086)

