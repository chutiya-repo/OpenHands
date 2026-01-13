from dataclasses import dataclass

from wsaicode.core.schema import ObservationType
from wsaicode.events.observation.observation import Observation


@dataclass
class SuccessObservation(Observation):
    """This data class represents the result of a successful action."""

    observation: str = ObservationType.SUCCESS

    @property
    def message(self) -> str:
        return self.content
