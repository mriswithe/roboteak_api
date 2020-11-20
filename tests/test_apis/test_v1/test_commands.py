from hypothesis import given, strategies as st

from models import Command

st_cmd = st.builds(
    Command,
    name=st.text(min_size=1, alphabet=st.characters(blacklist_categories=("P", "Cs"))),
    template=st.text(min_size=1),
)


@given(command=st_cmd)
def test_get_command(command, client, dep_overrider, mock_cmd_factory):
    from apis.v1.deps.command_deps import fs_snap_exists

    snap = mock_cmd_factory(command)

    async def return_snap(name, game: int):
        assert name == command.name
        assert game == command.game
        return snap

    with dep_overrider(fs_snap_exists, return_snap):
        resp = client.get(
            "/v1/commands", params={"name": command.name, "game": command.game}
        )
    assert Command.parse_raw(resp.content) == command


@given(command=st_cmd)
def test_create_command(command, client, dep_overrider, mock_cmd_factory):
    from unittest.mock import MagicMock

    from google.cloud.firestore_v1 import AsyncDocumentReference

    from apis.v1.deps.command_deps import fs_ref_from_command

    client_mock = MagicMock(spec_set=AsyncDocumentReference)
    snap = mock_cmd_factory(command)

    async def return_ref(name, game: int):
        assert name == command.name
        assert game == command.game
        return snap.reference

    with dep_overrider(fs_ref_from_command, return_ref):
        resp = client.post(
            "/v1/commands",
            params={"name": command.name, "game": command.game},
            data=command.json(),
        )
    assert Command.parse_raw(resp.content) == command
