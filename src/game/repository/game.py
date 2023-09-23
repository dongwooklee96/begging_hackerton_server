from database.models import Game


class GameRepository:
    def __init__(self, session):
        self.session = session

    async def create_game(self, product_key: int, user_key: int):
        """
        게임을 생성한다.
        """
        game = Game(product_key=product_key, user_key=user_key)
        self.session.add(game)
