from dataclasses import dataclass

from wsaicode.core.schema import ObservationType
from wsaicode.events.observation.observation import Observation


@dataclass
class FileDownloadObservation(Observation):
    file_path: str
    observation: str = ObservationType.DOWNLOAD

    @property
    def message(self) -> str:
        return f'Downloaded the file at location: {self.file_path}'

    def __str__(self) -> str:
        ret = (
            '**FileDownloadObservation**\n'
            f'Location of downloaded file: {self.file_path}\n'
        )
        return ret
