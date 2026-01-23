import logging
import os
import shutil
import threading
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LocalFileUploader:
    """File uploader that stores files in the local filesystem instead of S3."""

    def __init__(self, filename):
        """Initialize the LocalFileUploader.

        Args:
            filename (str): The name of the file to store (relative path within media/recordings)
        """
        self.filename = filename
        self.media_root = getattr(settings, "MEDIA_ROOT", os.path.join(settings.BASE_DIR, "media"))
        self.recordings_dir = os.path.join(self.media_root, "recordings")
        os.makedirs(self.recordings_dir, exist_ok=True)
        self._upload_thread = None

    def upload_file(self, file_path: str, callback=None):
        """Start an asynchronous 'upload' (copy) of a file to local storage.

        Args:
            file_path (str): Path to the local file to copy
            callback (callable, optional): Function to call when upload completes
        """
        self._upload_thread = threading.Thread(target=self._upload_worker, args=(file_path, callback), daemon=True)
        self._upload_thread.start()

    def _upload_worker(self, file_path: str, callback=None):
        """Background thread that handles the actual file copy.

        Args:
            file_path (str): Path to the local file to copy
            callback (callable, optional): Function to call when upload completes
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            # Destination path
            dest_path = os.path.join(self.recordings_dir, self.filename)

            # Copy the file
            shutil.copy2(str(file_path), dest_path)

            logger.info(f"Successfully copied {file_path} to {dest_path}")

            if callback:
                callback(True)

        except Exception as e:
            logger.error(f"Upload error: {e}")
            if callback:
                callback(False)

    def wait_for_upload(self):
        """Wait for the current upload to complete."""
        if self._upload_thread and self._upload_thread.is_alive():
            self._upload_thread.join()

    def delete_file(self, file_path: str):
        """Delete a file from the local filesystem."""
        file_path = Path(file_path)
        if file_path.exists():
            file_path.unlink()
