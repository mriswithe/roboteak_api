from hypothesis import strategies as st, given

from models import Command

st_cmd = st.builds(
    Command,
    name=st.text(min_size=1, alphabet=st.characters(blacklist_categories=("P", "Cs"))),
    template=st.text(min_size=1),
)


@given(command=st_cmd)
def test_get_command(client, dep_overrider, command, mock_cmd_factory):
    from apis.v1.deps.command_deps import fs_snap_exists

    snap = mock_cmd_factory(command)

    async def return_snap():
        return snap

    with dep_overrider(fs_snap_exists, return_snap):
        resp = client.get(
            "/v1/commands", params={"name": command.name, "game": command.game}
        )
    assert Command.parse_raw(resp.content) == command
