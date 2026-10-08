from fastapi import FastAPI

from battle import Camp
from driver import auto_battle
from eltena_master import (
    asashin_master,
    slime_master,
    yusha_master,
)

app = FastAPI()

@app.get("/run_battle")
def run_auto_battle():
    entries = [
        [yusha_master, Camp.PLAYER] ,
        [asashin_master, Camp.PLAYER] ,
        [slime_master, Camp.ENEMY]
    ]

    win_camp, logs = auto_battle(entries)

    return {
        "winner": win_camp.name if win_camp is not None else None,
        "logs": logs
    }