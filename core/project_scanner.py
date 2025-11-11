"""
Project scanning and analysis functionality
"""
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class ProjectScanner:
    """
    Scans directories for Comsol .mph files and extracts metadata.
    """

    def __init__(self, projects_path: Path):
        """
        Initialize scanner with projects directory.

        Args:
            projects_path: Path to directory containing .mph files
        """
        self.projects_path = projects_path

    def scan_projects(self) -> Dict[str, Dict[str, Any]]:
        """
        Scan the projects folder for Comsol .mph files.

        Returns:
            Dictionary mapping project names to project metadata
        """
        projects = {}

        if not self.projects_path.exists():
            return projects

        # Find all .mph files recursively
        mph_files = list(self.projects_path.rglob("*.mph"))

        for mph_file in sorted(mph_files):
            project_info = self.analyze_project(mph_file)
            if project_info:
                rel_path = mph_file.relative_to(self.projects_path)
                project_name = str(rel_path)
                projects[project_name] = project_info

        return projects

    def analyze_project(self, mph_file: Path) -> Optional[Dict[str, Any]]:
        """
        Analyze a Comsol .mph file to extract metadata.

        Args:
            mph_file: Path to .mph file

        Returns:
            Dictionary with project metadata or None if analysis fails
        """
        try:
            stat_info = mph_file.stat()

            # Calculate human-readable size
            size_bytes = stat_info.st_size
            size_str = self._format_file_size(size_bytes)

            # Format modification time
            mod_time = datetime.fromtimestamp(stat_info.st_mtime)
            modified_str = mod_time.strftime("%b %d, %Y")

            return {
                'file_path': mph_file,
                'display_name': mph_file.stem,
                'size_bytes': size_bytes,
                'size_str': size_str,
                'modified': mod_time,
                'modified_str': modified_str,
                'folder': mph_file.parent
            }
        except Exception:
            return None

    @staticmethod
    def _format_file_size(size_bytes: int) -> str:
        """
        Format file size in human-readable format.

        Args:
            size_bytes: File size in bytes

        Returns:
            Formatted string (e.g., "1.5 MB", "250 KB")
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
