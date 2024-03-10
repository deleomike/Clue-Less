import click
import rich


@click.group()
def clue():
    print("Clue-Less")


@clue.command(help="Play the game in your browser.")
@click.option("--port", "-p", default=8080, help="Port for webserver")
@click.option("--host", default="127.0.0.1", help="IP Address for serving")
# @click.option("--debug", "-d")
def serve(port, host):
    from clueless.app.webapp import app
    import uvicorn

    uvicorn.run(app=app, host=host, port=port)



@clue.command(help="Play the game locally in a terminal")
@click.option("--players", default=2, type=int, help="Number of Players")
def play(players: int):
    if players <= 1:
        print("Can't start a game with fewer than 2 players.")
        exit(1)
    pass


if __name__ == '__main__':
    clue()