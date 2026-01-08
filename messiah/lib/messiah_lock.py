#!/usr/bin/env python3
"""
SPRAXXX Messiah Lock — Core Module
Purpose: Enforce read-only Museum protection with controlled write windows
Doctrine: Truth leaves a trace. No silent rewrites.
"""

import os
import sys
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List


class MessiahLock:
    """
    Controls Museum read-only/read-write state transitions.

    Operational Doctrine:
    - Museum is RO by default (always)
    - Write windows are temporary, logged, and immediately closed
    - Failed re-lock is treated as critical failure
    """

    def __init__(self, museum_path: str = "/messiah/museum", workshop_path: str = "/messiah/workshop"):
        self.museum_path = Path(museum_path)
        self.workshop_path = Path(workshop_path)
        self.lock_log_path = self.workshop_path / "lock_operations.log"

    def is_museum_readonly(self) -> bool:
        """Check if museum has write permissions (based on mode, not actual write test)."""
        try:
            stat_info = os.stat(self.museum_path)
            # Check if owner has write permission (0o200 bit)
            # Museum should be 555 (r-xr-xr-x) when locked
            return (stat_info.st_mode & 0o200) == 0
        except OSError:
            return True  # If can't stat, assume locked

    def open_commit_window(self) -> bool:
        """
        Temporarily enable writes to Museum.
        CRITICAL: Must be followed by close_commit_window().
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        if not self.is_museum_readonly():
            self._log_lock_operation("open_attempt_already_writable", timestamp, success=False)
            return False

        try:
            # Make museum writable
            os.chmod(self.museum_path, 0o755)

            self._log_lock_operation("open_commit_window", timestamp, success=True)
            return True

        except Exception as e:
            self._log_lock_operation("open_commit_window", timestamp, success=False, error=str(e))
            return False

    def close_commit_window(self) -> bool:
        """
        Re-lock Museum to read-only.
        CRITICAL: Failure here is a security event.
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        if self.is_museum_readonly():
            self._log_lock_operation("close_attempt_already_readonly", timestamp, success=True)
            return True

        try:
            # Make museum read-only
            os.chmod(self.museum_path, 0o555)

            # Verify it worked
            if not self.is_museum_readonly():
                self._log_lock_operation("close_commit_window", timestamp, success=False,
                                        error="CRITICAL: Failed to verify RO state after chmod")
                return False

            self._log_lock_operation("close_commit_window", timestamp, success=True)
            return True

        except Exception as e:
            self._log_lock_operation("close_commit_window", timestamp, success=False, error=str(e))
            return False

    def _log_lock_operation(self, operation: str, timestamp: str, success: bool, error: Optional[str] = None):
        """Append-only log of all lock state changes."""
        log_entry = {
            "operation": operation,
            "timestamp": timestamp,
            "success": success,
            "error": error,
            "museum_path": str(self.museum_path)
        }

        with open(self.lock_log_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')


class Artifact:
    """
    Represents a Museum artifact with hash-based verification.
    """

    def __init__(self, content: str, metadata: Optional[Dict[str, Any]] = None):
        self.content = content
        self.metadata = metadata or {}
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def compute_sha256(self) -> str:
        """Generate SHA256 hash of artifact content."""
        return hashlib.sha256(self.content.encode('utf-8')).hexdigest()

    def to_package(self) -> Dict[str, Any]:
        """
        Generate complete artifact package.
        Returns dict with artifact, metadata, hash, and timestamp.
        """
        sha256 = self.compute_sha256()

        return {
            "artifact": self.content,
            "metadata": self.metadata,
            "sha256": sha256,
            "timestamp": self.timestamp
        }

    def write_to_museum(self, museum_path: Path, artifact_id: str) -> bool:
        """
        Write artifact package to Museum.
        Creates directory structure: museum/{artifact_id}/
        """
        artifact_dir = museum_path / artifact_id
        artifact_dir.mkdir(parents=True, exist_ok=True)

        package = self.to_package()

        # Write artifact content
        with open(artifact_dir / "artifact.txt", 'w') as f:
            f.write(package["artifact"])

        # Write metadata
        with open(artifact_dir / "metadata.json", 'w') as f:
            json.dump(package["metadata"], f, indent=2)

        # Write manifest with hash
        manifest = {
            "artifact_id": artifact_id,
            "timestamp": package["timestamp"],
            "sha256": package["sha256"],
            "metadata": package["metadata"]
        }

        with open(artifact_dir / "manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)

        # Create hash receipt file
        with open(artifact_dir / f"{package['sha256']}.sha256", 'w') as f:
            f.write(f"{package['sha256']}  artifact.txt\n")

        return True


def generate_artifact_id(prefix: str = "artifact") -> str:
    """Generate unique artifact ID with timestamp."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{prefix}-{timestamp}"


if __name__ == "__main__":
    # Simple test
    lock = MessiahLock(
        museum_path="/home/user/spraxxx.pantry/messiah/museum",
        workshop_path="/home/user/spraxxx.pantry/messiah/workshop"
    )

    print(f"Museum is read-only: {lock.is_museum_readonly()}")
