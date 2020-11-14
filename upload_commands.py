import json
from typing import Dict, List, Union


from google.cloud import firestore


from models import Command
from twitch_enums import Roles

role_map = {"Regular": Roles.REGULAR, "Moderator": Roles.MOD, "Everyone": Roles.GUEST}


def load_commands() -> List[Command]:
    with open("commands.json") as fp:
        commands = json.load(fp)
    cdict: Dict[str, Union[str, int]]
    cmds = []
    for cdict in commands:
        cmds.append(
            Command(
                name=cdict.get("Command").lstrip("!"),
                cooldown=cdict.get("Cooldown"),
                template=cdict.get("Response"),
                required_role=role_map.get(cdict.get("Permission")),
            )
        )
    return cmds


db = firestore.Client()
cmds = load_commands()
batch: firestore.WriteBatch
batch = db.batch()
col_ref: firestore.CollectionReference
col_ref = db.collection("games/0/commands")
for cmd in cmds:
    doc_ref = col_ref.document(cmd.name)
    batch.create(doc_ref, cmd.to_snap())
batch.commit()
