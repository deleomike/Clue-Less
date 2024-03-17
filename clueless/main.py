import click


@click.group()
def clue():
    """
    Clue-Less Root CLI Group
    :return:
    """

    from clueless.cli_utils import CLUE_LESS_ASCII, CONSOLE

    CONSOLE.print(CLUE_LESS_ASCII)


@clue.command(help="Play the game in your browser.")
@click.option("--port", "-p", default=8080, help="Port for webserver")
@click.option("--host", default="127.0.0.1", help="IP Address for serving")
def serve(port, host):
    """
    Play the game in your browser.

    :param port: Port number for the app
    :param host: Host for the app
    :return:
    """
    from clueless.app.webapp import app
    import uvicorn

    uvicorn.run(app=app, host=host, port=port)


@clue.command(help="Play the game locally in a terminal")
@click.option("--players", default=2, type=int, help="Number of Players")
def play(players: int):
    """

    :param players:
    :return:
    """

    from clueless.app.core.game.GameLoop import GameLoop

    GameLoop()

    if players <= 1:
        print("Can't start a game with fewer than 2 players.")
        exit(1)

    # TODO


if __name__ == '__main__':
    clue()