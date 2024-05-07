from enum import Enum
import logging
from pydantic import BaseModel, Field
import random
from typing import Optional


# Create a logger
# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.WARN)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

NUM_TRIALS = 1000
MAX_TURNS = 1000

class BoardSpaceType(Enum):
    BASE = 'base'
    SPECIAL = 'special'

class ResourceSetType(Enum):
    CATERPILLAR = 'caterpillar'
    BUTTERFLY = 'butterfly'

class Board(BaseModel):
    spaces: list[BoardSpaceType]
    resource_set_type: ResourceSetType

LARGE_BOARD_SPACES: list[BoardSpaceType] = [
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL,
    BoardSpaceType.BASE,
    BoardSpaceType.BASE,
    BoardSpaceType.SPECIAL
]

class TokenColor(Enum):
    RED = 'red'
    YELLOW = 'yellow'
    GREEN = 'green'
    BLUE = 'blue'
    ORANGE = 'orange'
    PURPLE = 'purple'
    WHITE = 'white'
    BLACK = 'black'


class Token(BaseModel):
    color: TokenColor
    spaces: int
    cost: int
    in_bag: bool = Field(default=True)

    def clone(self):
        return Token(**self.model_dump())

class TokenMaster(Enum):
    RED_1 = Token(color=TokenColor.RED, spaces=1, cost=1)
    RED_2 = Token(color=TokenColor.RED, spaces=2, cost=2)
    RED_4 = Token(color=TokenColor.RED, spaces=4, cost=3)
    YELLOW_1 = Token(color=TokenColor.YELLOW, spaces=1, cost=1)
    YELLOW_2 = Token(color=TokenColor.YELLOW, spaces=2, cost=2)
    YELLOW_4 = Token(color=TokenColor.YELLOW, spaces=4, cost=3)
    GREEN_1 = Token(color=TokenColor.GREEN, spaces=1, cost=1)
    GREEN_2 = Token(color=TokenColor.GREEN, spaces=2, cost=2)
    GREEN_4 = Token(color=TokenColor.GREEN, spaces=4, cost=3)
    BLUE_1 = Token(color=TokenColor.BLUE, spaces=1, cost=1)
    BLUE_2 = Token(color=TokenColor.BLUE, spaces=2, cost=2)
    BLUE_4 = Token(color=TokenColor.BLUE, spaces=4, cost=3)
    ORANGE_5 = Token(color=TokenColor.ORANGE, spaces=5, cost=4)
    PURPLE_5 = Token(color=TokenColor.PURPLE, spaces=5, cost=4)
    WHITE_8 = Token(color=TokenColor.WHITE, spaces=8, cost=5)
    BLACK = Token(color=TokenColor.BLACK, spaces=0, cost=-1)


class TokenInventory(BaseModel):
    tokens: list[Token] = Field(default=[
        TokenMaster.RED_1.value.clone(),
        TokenMaster.RED_1.value.clone(),
        TokenMaster.RED_2.value.clone(),
        TokenMaster.YELLOW_1.value.clone(),

        # Dream Weeds
        TokenMaster.BLACK.value.clone(),
        TokenMaster.BLACK.value.clone(),
        TokenMaster.BLACK.value.clone(),
        TokenMaster.BLACK.value.clone(),
    ])

    def add_token(self, token:Token) -> None:
        self.tokens.append(token.clone())

    def replace_token_at(self, token:Token, token_index_position:int):
        self.tokens[token_index_position] = token.clone()

    def pull_token_from_bag(self) -> tuple[Token, int]:
        # Make array of possible choices
        possible_choices = [index for index, item in enumerate(self.tokens) if item.in_bag]
        assert len(possible_choices) > 0
        
        # Select a random one
        selected_index = random.choice(possible_choices)

        # Set the random one that's in_bag
        self.tokens[selected_index].in_bag = False

        return (self.tokens[selected_index], selected_index)

    def put_all_tokens_back_in_bag(self) -> None:
        for token in self.tokens:
            token.in_bag = True
    
    def three_black_tokens_pulled(self) -> bool:
        num_black_tokens_pulled = sum(1 for token in self.tokens if token.color == TokenColor.BLACK and not token.in_bag)
        return num_black_tokens_pulled >= 3

    def num_pulled_orange_tokens(self) -> int:
        return sum(1 for token in self.tokens if token.color == TokenColor.ORANGE and not token.in_bag)



class PlayerStrategy(BaseModel):
    def make_buys(self, rubies):
        raise NotImplementedError

    def select_two_or_four_token(self, token_num_spaces: int):
        """
        token_num_spaces is either 2 or 4
        """
        raise NotImplementedError


# class RandomPlayerStrategy(PlayerStrategy):
#     def make_buys(self, rubies):
#         return []

#     def select_two_or_four_token(self, token_num_spaces: int):
#         """
#         We have to take something so make it green
#         """
#         if token_num_spaces == 2:
#             return TokenMaster.GREEN_2
#         elif token_num_spaces == 4:
#             return TokenMaster.GREEN_4
#         else:
#             logger.error(f'Unexpected token spaces: {token_num_spaces}')
#             assert False


class BuyNothingPlayerStrategy(PlayerStrategy):
    def make_buys(self, rubies):
        return []

    def select_two_or_four_token(self, token_num_spaces: int):
        """
        We have to take something so make it green
        """
        if token_num_spaces == 2:
            return TokenMaster.GREEN_2
        elif token_num_spaces == 4:
            return TokenMaster.GREEN_4
        else:
            logger.error(f'Unexpected token spaces: {token_num_spaces}')
            assert False


class AlwaysWhitePlayerStrategy(PlayerStrategy):
    def make_buys(self, rubies):
        return [TokenMaster.WHITE_8.value]

    def select_two_or_four_token(self, token_num_spaces: int):
        """
        We have to take something so make it green
        """
        if token_num_spaces == 2:
            return TokenMaster.GREEN_2
        elif token_num_spaces == 4:
            return TokenMaster.GREEN_4
        else:
            logger.error(f'Unexpected token spaces: {token_num_spaces}')
            assert False


class BuyTokenOrderPlayerStrategy(PlayerStrategy):
    tokens_to_buy: list[TokenMaster]

    def make_buys(self, rubies):
        purchased_tokens = []
        purchased_color = []

        for possible_token_purchase in self.tokens_to_buy:
            if possible_token_purchase.value.color not in purchased_color and rubies >= possible_token_purchase.value.cost:
                purchased_tokens.append(possible_token_purchase.value)
                purchased_color.append(possible_token_purchase.value.color)
                rubies -= possible_token_purchase.value.cost

        return purchased_tokens


    def select_two_or_four_token(self, token_num_spaces: int):
        """
        token_num_spaces is either 2 or 4
        """

        # TODO: make this not hard coded

        if token_num_spaces == 2:
            return TokenMaster.GREEN_2
        elif token_num_spaces == 4:
            return TokenMaster.GREEN_4
        else:
            logger.error(f'Unexpected token spaces: {token_num_spaces}')
            assert False


# class AlwaysSameTokenPlayerStrategy(PlayerStrategy):
#     def make_buys(self, rubies):
#         purchased_tokens = []
#         if rubies >= 3:
#             purchased_tokens.append(TokenMaster.RED_4)
#             rubies -= TokenMaster.RED_4.value.cost
#         elif rubies >= 2:
#             purchased_tokens.append(TokenMaster.RED_2)
#             rubies -= TokenMaster.RED_2.value.cost
#         elif rubies >= 1:
#             purchased_tokens.append(TokenMaster.RED_1)
#             rubies -= TokenMaster.RED_1.value.cost

#         # TODO: Buy something else if possible

#         return purchased_tokens


class AlwaysBluePlayerStrategy(PlayerStrategy):
    def make_buys(self, rubies):
        # TODO
        purchased_tokens = []

class Player(BaseModel):
    name: str
    player_strategy: PlayerStrategy
    board: Board
    num_rubies: int = Field(default=0)
    num_clovers: int = Field(default=0)

    # Starting at -1 since the first space is index 0
    position: int = Field(default=-1)
    token_inventory: TokenInventory = Field(default=TokenInventory())

    def is_on_special_space(self):
        return self.board.spaces[self.position] == BoardSpaceType.SPECIAL

    def do_turn(self):
        # Pull token
        (token_pulled, token_index_position) = self.token_inventory.pull_token_from_bag()

        # Advance token spaces
        self.position += token_pulled.spaces
        logger.info(f'Advanced {token_pulled.spaces} to position {self.position}')

        # If won, end early
        if (self.position >= len(self.board.spaces)):
            logger.info(f'Won so ending early...')
            return

        # Define extra actions
        actions = {
            TokenColor.RED: self.perform_red_action,
            TokenColor.YELLOW: self.perform_yellow_action,
            TokenColor.GREEN: self.perform_green_action,
            TokenColor.BLUE: self.perform_blue_action,
            TokenColor.ORANGE: self.perform_orange_action,
            TokenColor.PURPLE: self.perform_purple_action,
            TokenColor.WHITE: self.perform_white_action,
            TokenColor.BLACK: self.perform_black_action,
        }

        # Resolve Token Action
        action_func = actions.get(token_pulled.color)
        if action_func:
            action_func(token_pulled, token_index_position)
        else:
            logger.error(f'Invalid token color pulled({token_pulled.color})')

        # Check if three dream weeds are pulled, if so replace and buy
        if self.token_inventory.three_black_tokens_pulled():
            logger.info('Three dream weeds pulled, buying and replacing all tokens')

            # Advance by clover amount
            self.position += self.num_clovers

            # If won, end early
            if (self.position >= len(self.board.spaces)):
                logger.info(f'Won so ending early due to clovers...')
                return

            # Buy tokens
            self.buy_tokens()

            # Put all tokens back in
            self.token_inventory.put_all_tokens_back_in_bag()


    def buy_tokens(self):
        logger.info(f'Buying tokens with {self.num_rubies} rubies')
        purchased_tokens = self.player_strategy.make_buys(self.num_rubies)
        logger.info(f'Purchased: {purchased_tokens}')

        # Add all the new tokens into the token inventory
        for token in purchased_tokens:
            # Clone since need in_bag to have difference instances
            self.token_inventory.add_token(token)
        
        # After buying, all rubies are either spent or lost
        self.num_rubies = 0

    def perform_red_action(self, token: Token, token_index_position: int):
        logger.info(f"Doing red action")
        match self.board.resource_set_type:
            case ResourceSetType.CATERPILLAR:
                # Gain two rubies on a special space, otherwise gain one
                if self.is_on_special_space():
                    logger.info('Gaining 2 rubies')
                    self.num_rubies += 2
                else:
                    logger.info('Gaining 1 ruby')
                    self.num_rubies += 1
            case ResourceSetType.BUTTERFLY:
                if token.spaces == 1:
                    logger.info('Gaining 1 ruby')
                    self.num_rubies += 1
                elif token.spaces == 2:
                    logger.info('Gaining 2 ruby')
                    self.num_rubies += 2
                elif token.spaces == 4:
                    logger.info('Gaining 3 ruby')
                    self.num_rubies += 3
                else:
                    logger.error(f'Unknown red spaces {token.spaces}')
            case _:
                logger.error(f'Unknown resource set type {self.board.resource_set_type}')


    def perform_yellow_action(self, token: Token, token_index_position: int):
        logger.info(f"Doing yellow action")
        match self.board.resource_set_type:
            case ResourceSetType.CATERPILLAR:
                ...
            case ResourceSetType.BUTTERFLY:
                ...
            case _:
                logger.error(f'Unknown resource set type {self.board.resource_set_type}')


    def perform_green_action(self, token: Token, token_index_position: int):
        logger.info(f"Doing green action")
        match self.board.resource_set_type:
            case ResourceSetType.CATERPILLAR:
                # Put back in your bag any non-dream weed token that's been pulled, including the one just pulled
                ...
            case ResourceSetType.BUTTERFLY:
                # Pull another token from your bag
                ...
            case _:
                logger.error(f'Unknown resource set type {self.board.resource_set_type}')


    def perform_blue_action(self, token: Token, token_index_position: int):
        logger.info(f"Doing blue action")
        match self.board.resource_set_type:
            case ResourceSetType.CATERPILLAR:
                # Move to the next special field on the board
                next_special_position = -1
                possible_special_position = self.position + 1

                # Loop while we could have a next special position
                while possible_special_position < len(self.board.spaces):
                    if self.board.spaces[possible_special_position] == BoardSpaceType.SPECIAL:
                        next_special_position = possible_special_position
                        break

                # Check to see if we found a next spiral and set it
                if next_special_position > 0:
                    self.position = next_special_position

            case ResourceSetType.BUTTERFLY:
                # Replace the token with the next version up to white
                if token.color == TokenColor.BLUE:
                    if token.spaces == 1:
                        self.token_inventory.replace_token_at(TokenMaster.BLUE_2.value, token_index_position)
                    elif token.spaces == 2:
                        self.token_inventory.replace_token_at(TokenMaster.BLUE_4.value, token_index_position)
                    elif token.spaces == 4:
                        self.token_inventory.replace_token_at(TokenMaster.WHITE_8.value, token_index_position)
                    else:
                        logger.error(f'We have a blue token with a non-standard number of spaces={token.spaces}')
                        assert False

            case _:
                logger.error(f'Unknown resource set type {self.board.resource_set_type}')


    def perform_orange_action(self, token: Token, token_index_position: int):
        logger.info(f"Doing orange action")
        match self.board.resource_set_type:
            case ResourceSetType.CATERPILLAR:
                # Collect a clover, if on a special space, collect 2 clovers
                self.num_clovers += 2 if self.is_on_special_space() else 1

            case ResourceSetType.BUTTERFLY:
                # Collect a clover for every pulled orange token (including the one that was just pulled)
                self.num_clovers += self.token_inventory.num_pulled_orange_tokens()

            case _:
                logger.error(f'Unknown resource set type {self.board.resource_set_type}')


    def perform_purple_action(self, token: Token, token_index_position: int):
        logger.info(f"Doing purple action")
        match self.board.resource_set_type:
            case ResourceSetType.CATERPILLAR:
                # Move forward the number of rubies the player currently has
                self.position += self.num_rubies

            case ResourceSetType.BUTTERFLY:
                # Take any 2 space token from the bag, take any 4 space token from the bag
                
                player_strategy.select_two_or_four_token(4 if self.is_on_special_space() else 2)
                
                # 
                ...

            case _:
                logger.error(f'Unknown resource set type {self.board.resource_set_type}')


    def perform_white_action(self, token: Token, token_index_position: int):
        # No real white action, just movement
        ...


    def perform_black_action(self, token: Token, token_index_position: int):
        # No real black action, just buy phase at 3 pulls which happens separately
        ...



class GameManager(BaseModel):
    players: list[Player]
    board: Board
    turns: int = Field(default=0)
    winner: Optional[Player] = Field(default=None)

    def game_ended(self):
        for player in self.players:
            if player.position >= len(self.board.spaces):
                return player

        return None

    def play_game(self):
        # Loop over players until someone wins
        while self.turns < MAX_TURNS:
            self.turns += 1
            for player in self.players:
                # Do Turn
                go_again = True
                while go_again:
                    go_again = player.do_turn()

                # Check win condition
                if player.position >= len(self.board.spaces):
                    # Set the winner
                    self.winner = player
                    return player
        
        logger.error('ERROR: Game hit MAX_TURNS')


def get_turns_for_one_game(player_strategy, board):
    player1 = Player(name='Player 1', player_strategy=player_strategy, board=board)

    game_manager = GameManager(
        players=[player1],
        board=board
    )

    game_manager.play_game()

    logger.info(f'Completed in {game_manager.turns} turns')

    return game_manager.turns

if __name__ == '__main__':

    # player_strategy = BuyTokenOrderPlayerStrategy(tokens_to_buy=[
    #     TokenMaster.RED_4, TokenMaster.RED_2, TokenMaster.RED_1
    # ])

    # Always blue, green backup
    # player_strategy = BuyTokenOrderPlayerStrategy(tokens_to_buy=[
    #     TokenMaster.BLUE_4, TokenMaster.BLUE_2, TokenMaster.BLUE_1,
    #     TokenMaster.GREEN_4, TokenMaster.GREEN_2, TokenMaster.GREEN_1,
    # ])

    # Always white with green normally, blue backup
    # player_strategy = BuyTokenOrderPlayerStrategy(tokens_to_buy=[
    #     TokenMaster.WHITE_8,
    #     TokenMaster.GREEN_4, TokenMaster.GREEN_2, TokenMaster.GREEN_1,
    #     TokenMaster.BLUE_4, TokenMaster.BLUE_2, TokenMaster.BLUE_1,
    # ])

    # Always white with blues normally, green backup
    # player_strategy = BuyTokenOrderPlayerStrategy(tokens_to_buy=[
    #     TokenMaster.WHITE_8,
    #     TokenMaster.BLUE_4, TokenMaster.BLUE_2, TokenMaster.BLUE_1,
    #     TokenMaster.GREEN_4, TokenMaster.GREEN_2, TokenMaster.GREEN_1,
    # ])

    # Buy red with green backups
    # player_strategy = BuyTokenOrderPlayerStrategy(tokens_to_buy=[
    #     TokenMaster.RED_4, TokenMaster.RED_2, TokenMaster.RED_1,
    #     TokenMaster.WHITE_8,
    #     TokenMaster.BLUE_4, TokenMaster.BLUE_2, TokenMaster.BLUE_1,
    #     TokenMaster.GREEN_4, TokenMaster.GREEN_2, TokenMaster.GREEN_1,
    # ])

    # Test a color orange
    # player_strategy = BuyTokenOrderPlayerStrategy(tokens_to_buy=[
    #     TokenMaster.ORANGE_5,
    #     TokenMaster.RED_4, TokenMaster.RED_2, TokenMaster.RED_1,
    # ])

    # Test a color purple
    player_strategy = BuyTokenOrderPlayerStrategy(tokens_to_buy=[
        TokenMaster.PURPLE_5,
        TokenMaster.RED_4, TokenMaster.RED_2, TokenMaster.RED_1,
    ])

    # Don't buy anything ever
    # player_strategy = BuyNothingPlayerStrategy()

    # Cheat and get a turnip every time you buy
    # player_strategy = AlwaysWhitePlayerStrategy()

    board = Board(
        spaces=LARGE_BOARD_SPACES,
        resource_set_type=ResourceSetType.CATERPILLAR
    )

    total_turns = 0
    for i in range(0, NUM_TRIALS):
        total_turns += get_turns_for_one_game(player_strategy, board)

    print(f'Average turns: {total_turns / NUM_TRIALS}')

    # tokens = [
    #     TokenMaster.GREEN_1.value.clone(),
    #     TokenMaster.GREEN_1.value.clone(),
    #     TokenMaster.GREEN_1.value.clone(),
    #     TokenMaster.GREEN_1.value.clone()
    # ]

    # print(f'tokens[0].value.in_bag={tokens[0].in_bag}')
    # print(f'tokens[1].value.in_bag={tokens[1].in_bag}')
    # tokens[0].in_bag = False
    # print(f'tokens[0].value.in_bag={tokens[0].in_bag}')
    # print(f'tokens[1].value.in_bag={tokens[1].in_bag}')