import logging
from pathlib import Path
from typing import Iterable

from raggamuffin.models import Document

logger = logging.getLogger(__name__)


class DocumentHandler:
    path: Path
    glob: str

    def __init__(self, path: Path, glob: str = "**/*.txt"):
        self.path = path
        self.glob = glob

    def get_documents(self) -> Iterable[Document]:
        """Return iterator of documents found."""

        for path in self.path.glob(self.glob):
            try:
                text = path.read_text()
            except UnicodeDecodeError as e:
                logger.warn("Skipping %s due to %e", path, e)
                continue

            yield Document(title=str(path), text=text)
