"""
MPH file parsing utilities
"""
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class MphParser:
    """
    Parser for Comsol .mph files (which are ZIP archives containing XML/JSON/binary data).
    """

    @staticmethod
    def parse_parameters(xml_content: str) -> List[Tuple[str, str, str]]:
        """
        Parse parameters from dmodel.xml content.

        Args:
            xml_content: String content of dmodel.xml

        Returns:
            List of tuples (name, value, description) for each parameter
        """
        try:
            # Use regex to find parameter expressions
            # Pattern matches: <expressions name="param_name" expr="value" descr="description"...
            pattern = r'<expressions[^>]*name="([^"]*)"[^>]*expr="([^"]*)"[^>]*descr="([^"]*)"'
            matches = re.findall(pattern, xml_content)

            parameters = []
            for name, value, desc in matches:
                # Skip internal/computed parameters and very long expressions
                if name not in ['currentiter'] and not value.startswith('Triangle') and len(value) < 100:
                    parameters.append((name, value, desc))

            return parameters
        except Exception:
            return []

    @staticmethod
    def load_file_list(mph_path: Path) -> List[Dict[str, str]]:
        """
        Load list of files inside .mph archive.

        Args:
            mph_path: Path to .mph file

        Returns:
            List of dictionaries with file information
        """
        files = []
        try:
            with zipfile.ZipFile(mph_path, 'r') as z:
                for file_info in z.infolist():
                    size_kb = file_info.file_size / 1024
                    if size_kb < 1:
                        size_str = f"{file_info.file_size} B"
                    else:
                        size_str = f"{size_kb:.1f} KB"

                    # Determine type and color tag
                    file_type, tag = MphParser._classify_file(file_info.filename)

                    files.append({
                        'filename': file_info.filename,
                        'size': size_str,
                        'type': file_type,
                        'tag': tag
                    })
        except Exception:
            pass

        return files

    @staticmethod
    def _classify_file(filename: str) -> Tuple[str, str]:
        """
        Classify file by extension.

        Args:
            filename: Name of file

        Returns:
            Tuple of (file_type_label, color_tag)
        """
        if filename.endswith('.xml'):
            return ("Configuration", 'xml')
        elif filename.endswith('.json'):
            return ("Metadata", 'json')
        elif filename.endswith('.mphbin'):
            return ("Simulation Data", 'binary')
        elif filename.endswith('.png'):
            return ("Preview Image", 'image')
        elif filename.endswith('.txt'):
            return ("Text Data", 'text')
        elif filename.endswith('.zip'):
            return ("Checkpoint", 'archive')
        else:
            return ("Data", 'text')

    @staticmethod
    def load_model_info(mph_path: Path) -> Optional[Dict[str, str]]:
        """
        Load model information from mph file.

        Args:
            mph_path: Path to .mph file

        Returns:
            Dictionary with model info or None if loading fails
        """
        try:
            with zipfile.ZipFile(mph_path, 'r') as z:
                # Read version
                fileversion = z.read('fileversion').decode('utf-8', errors='ignore').strip()

                # Read model info XML
                modelinfo = z.read('modelinfo.xml').decode('utf-8')
                root = ET.fromstring(modelinfo)
                title = root.get('title', 'N/A')
                description = root.get('description', 'N/A')

                # Calculate sizes
                total_size = sum(f.file_size for f in z.infolist())
                text_size = sum(f.file_size for f in z.infolist()
                               if f.filename.endswith(('.xml', '.json', '.txt')))
                binary_size = sum(f.file_size for f in z.infolist()
                                 if f.filename.endswith('.mphbin'))

                return {
                    'version': fileversion,
                    'title': title,
                    'description': description,
                    'file_count': len(z.namelist()),
                    'total_size_mb': total_size / 1024 / 1024,
                    'text_size_mb': text_size / 1024 / 1024,
                    'binary_size_mb': binary_size / 1024 / 1024,
                    'text_percent': text_size / total_size * 100 if total_size > 0 else 0,
                    'binary_percent': binary_size / total_size * 100 if total_size > 0 else 0
                }
        except Exception:
            return None

    @staticmethod
    def load_parameters_from_mph(mph_path: Path) -> List[Tuple[str, str, str]]:
        """
        Load parameters directly from .mph file.

        Args:
            mph_path: Path to .mph file

        Returns:
            List of tuples (name, value, description)
        """
        try:
            with zipfile.ZipFile(mph_path, 'r') as z:
                dmodel_content = z.read('dmodel.xml').decode('utf-8')
                return MphParser.parse_parameters(dmodel_content)
        except Exception:
            return []
