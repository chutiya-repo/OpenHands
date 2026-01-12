from dataclasses import dataclass

from wsai_code.core.schema import ObservationType
from wsai_code.events.observation.observation import Observation


@dataclass
class UserRejectObservation(Observation):
    """This data class represents the result of a rejected action."""

    observation: str = ObservationType.USER_REJECTED

    @property
    def message(self) -> str:
        return self.content
