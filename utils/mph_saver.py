"""
MPH file saving and modification utilities
"""
import re
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Tuple


class MphSaver:
    """
    Utilities for modifying and saving .mph files.
    """

    @staticmethod
    def save_modified_mph(
        mph_path: Path,
        parameters: Dict[str, str]
    ) -> Tuple[bool, str, Path, Path]:
        """
        Save modified parameters back to a new .mph file.

        Args:
            mph_path: Original .mph file path
            parameters: Dictionary of {parameter_name: new_value}

        Returns:
            Tuple of (success, message, new_mph_path, backup_path)
        """
        try:
            # Create temp directory for extraction
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)

                # Extract mph file
                with zipfile.ZipFile(mph_path, 'r') as z:
                    z.extractall(temp_path)

                # Update dmodel.xml
                dmodel_path = temp_path / 'dmodel.xml'
                if not dmodel_path.exists():
                    return (False, "Could not find dmodel.xml in file", None, None)

                content = dmodel_path.read_text(encoding='utf-8')

                # Update each parameter using regex
                for param_name, new_value in parameters.items():
                    pattern = f'(name="{param_name}"[^>]*expr=")([^"]*)(")'
                    replacement = f'\\g<1>{new_value}\\g<3>'
                    content = re.sub(pattern, replacement, content)

                dmodel_path.write_text(content, encoding='utf-8')

                # Create backup of original
                backup_path = mph_path.parent / f"{mph_path.stem}_backup.mph"
                shutil.copy2(mph_path, backup_path)

                # Create new modified file
                new_mph = mph_path.parent / f"{mph_path.stem}_modified.mph"

                # Re-pack as ZIP
                with zipfile.ZipFile(new_mph, 'w', zipfile.ZIP_DEFLATED) as z:
                    for file_path in temp_path.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(temp_path)
                            z.write(file_path, arcname)

                return (True, "Success", new_mph, backup_path)

        except Exception as e:
            return (False, str(e), None, None)

    @staticmethod
    def extract_mph(mph_path: Path, extract_dir: Path) -> Tuple[bool, str, int]:
        """
        Extract .mph file contents to a directory.

        Args:
            mph_path: Path to .mph file
            extract_dir: Directory to extract to

        Returns:
            Tuple of (success, message, file_count)
        """
        try:
            extract_path = extract_dir / f"{mph_path.stem}-extracted"
            extract_path.mkdir(exist_ok=True)

            with zipfile.ZipFile(mph_path, 'r') as z:
                z.extractall(extract_path)

            file_count = len(list(extract_path.rglob('*')))
            return (True, str(extract_path), file_count)

        except Exception as e:
            return (False, str(e), 0)
