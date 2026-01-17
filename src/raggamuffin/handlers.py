"""Document handlers for loading documents from various sources."""

import logging
from pathlib import Path
from typing import Iterable

from raggamuffin.models import DocumentTable, TextDocumentTable

logger = logging.getLogger(__name__)


class DocumentHandler:
    """Handler for loading text documents from a directory.

    TODO: This needs to be updated to work with the new schema:
    - Documents require a Source (which requires a SourceType)
    - TextDocuments are joined tables (DocumentTable + TextDocumentTable)
    - Consider using a factory or service layer for document creation
    """

    path: Path
    glob: str

    def __init__(self, path: Path, glob: str = "**/*.txt"):
        self.path = path
        self.glob = glob

    def get_documents(self) -> Iterable[tuple[DocumentTable, TextDocumentTable]]:
        """Return iterator of document pairs (base + text) found.

        Note: These documents don't have sources set - the caller must
        create appropriate SourceType and Source records first.
        """
        for file_path in self.path.glob(self.glob):
            try:
                text = file_path.read_text()
            except UnicodeDecodeError as e:
                logger.warning("Skipping %s due to %e", file_path, e)
                continue

            # TODO: Full implementation needs source handling
            # Create base document (source_id must be set by caller)
            # doc = DocumentTable(type="text_document", ...)
            # text_doc = TextDocumentTable(id=doc.id, text=text)
            # yield (doc, text_doc)

            # For now, just log
            logger.info(
                "Would create document from: %s (%d chars)", file_path, len(text)
            )

        # Empty generator - no documents yielded until source handling is implemented
        return
        yield  # type: ignore[misc]  # Makes this a generator function
