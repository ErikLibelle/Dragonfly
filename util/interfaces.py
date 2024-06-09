from typing import List, Optional, Protocol, Tuple
from rlbot.agents.base_agent import SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket


class iCar(Protocol):
    location: "iVector3"
    orientation: "iMatrix3"
    velocity: "iVector3"
    angular_velocity: List[float]
    demolished: bool
    airborne: bool
    supersonic: bool
    jumped: bool
    doublejumped: bool
    boost: int
    index: int

    def __init__(self, index: int, packet: GameTickPacket) -> None:
        super().__init__()

    def local(self, value: "iVector3") -> "iVector3":
        pass

    def update(self, packet: "GameTickPacket") -> None:
        pass

    @property
    def forward(self) -> "iVector3":
        pass

    @property
    def left(self) -> "iVector3":
        pass

    @property
    def up(self) -> "iVector3":
        pass


class iBall(Protocol):
    location: "iVector3"
    velocity: "iVector3"
    latest_touched_time: float
    latest_touched_team: int

    def update(self, packet: "GameTickPacket") -> None:
        pass


class iBoost(Protocol):
    index: int
    location: "iVector3"
    active: bool
    large: bool

    def update(self, packet: "GameTickPacket") -> None:
        pass


class iGoal(Protocol):
    location: "iVector3"
    left_post: "iVector3"
    right_post: "iVector3"


class iGame(Protocol):
    time: float
    time_remaining: float
    overtime: bool
    round_active: bool
    kickoff: bool
    match_ended: bool

    def update(self, packet: "GameTickPacket") -> None:
        pass


class iSmartRoutine(Protocol):
    last_check: int = -10000
    name: str = "Untitled Routine"
    first_run: bool = False

    def run(self, agent: "iCommandAgent") -> None:
        pass

    def next_check(self) -> int:
        pass


class iCommandAgent(Protocol):
    friends: List[iCar]
    foes: List[iCar]
    me: iCar
    ball: iBall
    game: iGame
    boosts: List[iBoost]
    friend_goal: iGoal
    foe_goal: iGoal
    intent: Optional[iSmartRoutine]
    time: float
    ready: bool
    controller: "SimpleControllerState"
    kickoff_flag: bool

    def get_ready(self, packet: "GameTickPacket") -> None:
        pass

    def refresh_player_lists(self, packet: "GameTickPacket") -> None:
        pass

    def set_intent(self, routine: iSmartRoutine) -> None:
        pass

    def get_intent(self) -> Optional[iSmartRoutine]:
        pass

    def clear_intent(self) -> None:
        pass

    def push(self, routine: iSmartRoutine) -> None:
        pass

    def pop(self) -> Optional[iSmartRoutine]:
        pass

    def line(
        self,
        start: "iVector3",
        end: "iVector3",
        color: Optional[Tuple[int, int, int]] = None,
    ) -> None:
        pass

    def debug_intent(self) -> None:
        pass

    def clear(self) -> None:
        pass

    def preprocess(self, packet: "GameTickPacket") -> None:
        pass

    def get_output(self, packet: "GameTickPacket") -> "SimpleControllerState":
        pass

    def run(self) -> None:
        pass


class iVector3(Protocol):
    def __getitem__(self, key: int) -> float:
        pass

    def __setitem__(self, key: int, value: float) -> None:
        pass

    def __add__(self, value: "iVector3") -> "iVector3":
        pass

    def __sub__(self, value: "iVector3") -> "iVector3":
        pass

    def __mul__(self, value: float) -> "iVector3":
        pass

    def __truediv__(self, value: float) -> "iVector3":
        pass

    def dot(self, value: "iVector3") -> float:
        pass

    def cross(self, value: "iVector3") -> "iVector3":
        pass

    def magnitude(self) -> float:
        pass

    def normalize(self) -> "iVector3":
        pass

    def copy(self) -> "iVector3":
        pass


class iMatrix3(Protocol):
    forward: iVector3
    left: iVector3
    up: iVector3

    def __getitem__(self, key: int) -> iVector3:
        pass

    def dot(self, vector: iVector3) -> iVector3:
        pass
