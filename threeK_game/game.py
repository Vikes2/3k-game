import abc
import random
from .models import Match as mMatch, Profile

class QueueI(abc.ABC):
    @abc.abstractmethod
    def len(self):
        pass
    @abc.abstractmethod
    def pop(self):
        pass
    @abc.abstractmethod
    def push(self, value):
        pass
    @abc.abstractmethod
    def is_empty(self):
        pass

class Queue(QueueI):
    def __init__(self, container):
        self.players = container

    def len(self):
        return len(self.players)

    def pop(self):
        return self.players.pop(0) if self.len() > 0 else None

    def push(self, value):
        self.players.append(value)

    def is_empty(self):
        return (self.len() == 0)

    def print_content(self):
        # return tuple(self.players)
        return self.players

class GameManager(object):
    __instance = None
    def __new__(cls):
        if GameManager.__instance is None:
            GameManager.__instance = object.__new__(cls)
            cls.queue = Queue([])
            cls.active_matches = []    
        return GameManager.__instance


    def connect_player(self, consumer):
        #user = consumer.scope['user'].username
        self.queue.push(consumer)
        print(self.queue.len(), end="============================ len queue\n")
        if self.queue.len() > 1:
            self.create_new_game()
    
    def create_new_game(self):
        player_a = self.queue.pop()
        player_b = self.queue.pop()
        new_match= Match(player_a, player_b)
        print("match created")
        new_match.attach(player_a)
        new_match.attach(player_b)
        new_match.match_start = new_match.match_id
        print(new_match.match_id)
        self.active_matches.append(new_match)

class Match:
    def __init__(self, username_a, username_b):
        self.player_a = username_a
        self.player_b = username_b
        self._observers = set()
        self.create_match_model(username_a.scope['user'].username, username_b.scope['user'].username)
        self.game_list = []
        self.is_end_match = False

    def run_games(self):
        #the first win
        #create game
        #game_model = self.match_model.game_set.create()
        game_obj = Game(self)
        self.game_list.append(game_obj)

    def finish_game(self, result):
        if result:
            self.is_end_match = True
            #end match
        else:
            self.run_games()


    def create_match_model(self, username_a, username_b):
        print(username_a, username_b, end="---")
        user_a = Profile.objects.get(user__username=username_a)
        user_b = Profile.objects.get(user__username=username_b)
        self.match_model = mMatch.objects.create(playerA=user_a, playerB=user_b)
        self.match_id = self.match_model.id

    def attach(self, observer):
        observer._match = self
        self._observers.add(observer)

    def detach(self, observer):
        observer._match = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._match_start)
        

    @property
    def match_start(self):
        return self._match_start

    @match_start.setter
    def match_start(self, arg):
        self._match_start = arg
        self._notify()
        self.run_games()

class Game:
    def __init__(self, match):
        self.board = dict()
        self.is_finished = False
        self.match = match
        self.create_game_model(match.match_model)
        self.a_side = (random.random() > 0.5)
        self.group_message("Gra została utworzona", "log")
        self.run_game()

    def create_game_model(self, match_model):
        self.game_model = match_model.game_set.create()

    def run_game(self):
        player = "A" if self.a_side else "B"
        self.group_message("Game is on! Player " + player + " is your move", "log")

    def end_game(self, result):
        self.is_finished = False
        self.match.finish_game(result)

    def group_message(self, text, content_type):
        print("\nmaking_group_message\n")
        self.match.player_a.group_message(text, content_type)

class FlyweightFactory(object):
    def __init__(self, cls):
        self._cls = cls
        self._instances = dict()

    def get_instance(self, *args, **kargs):
        return self._instances.setdefault(
                (args, tuple(kargs.items())),
                self._cls(*args, **kargs)
            )


#----------------------------------------------------------
class Mark(object):
    def __init__(self, type):
        self.type = type

# SharpFactory = FlyweightFactory(Sharp)
# CircleFactory = FlyweightFactory(Circle)

# SharpFactory.get_instance()
