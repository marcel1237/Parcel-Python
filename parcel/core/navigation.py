from enum import Enum, auto
from typing import Callable, Optional

class NavigationTarget(Enum):
    HOME = auto()
    NEW_PROJECT = auto()
    OPEN_PROJECT = auto()
    TEMPLATES = auto()
    GIT = auto()
    GITHUB = auto()
    SETTINGS = auto()
    ABOUT = auto()
    WORKSPACE = auto()


class NavigationController:
    _instance: Optional["NavigationController"] = None

    @classmethod
    def get_instance(cls) -> "NavigationController":
        if cls._instance is None:
            cls._instance = NavigationController()
        return cls._instance

    def __init__(self):
        self.current: NavigationTarget = NavigationTarget.HOME
        self.previous: NavigationTarget = NavigationTarget.HOME
        self.current_path: str = ""
        self.on_navigate = None

    def navigate_to(self, target: NavigationTarget, path: str = ""):
        if self.current != target or (path and path != self.current_path):
            self.previous = self.current
            self.current = target
            self.current_path = path
            if self.on_navigate:
                self.on_navigate(target, path)

    def go_back(self):
        self.navigate_to(self.previous)

    def set_on_navigate(self, callback):
        self.on_navigate = callback
