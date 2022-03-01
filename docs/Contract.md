## Contract

Games will communicate with messages in the following formats.

Messages to the app will take the form:
```
{
    "game_id": <game_id>, # this should be enough for the backend to determine the type of game
    "message_type": <type> # depending on the game, this should specify what the intent is
    <other specific fields>
    # possibly later to add, a web token that confirms the users id/role
}
```

Messages from the app will take the form:
```
{
    "game_id": <game_id>,
    "state": <specific info for the updated game state>
}
```