from dataclasses import dataclass

from wsaicode.core.schema import ActionType
from wsaicode.events.action.action import Action


@dataclass
class NullAction(Action):
    """An action that does nothing."""

    action: str = ActionType.NULL

    @property
    def message(self) -> str:
        return 'No action'
