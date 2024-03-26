
from typing import Self

from settings import DOWNLOADS
from medicalboards.states import State

class DownloadManager:
    """
    Context manager for making sure asset folders exist and provides a general
    interface for downloading external assets for this application.
    """

    MAX_DATABASE_SIZE = 100_000_000 # 100 megabytes

    def __init__(self, state: State):
        self.state = state
        self.download_directory = DOWNLOADS / self.state.name.casefold()

    def __enter__(self) -> Self:
        if not DOWNLOADS.exists():
            DOWNLOADS.mkdir()
        if not self.download_directory.exists():
            self.download_directory.mkdir()
        return self