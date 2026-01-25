#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource helper for finding files in both development and PyInstaller environments
"""
import os
import sys
from pathlib import Path

def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.

    Args:
        relative_path: Path relative to the project root (e.g., 'src/simi.py')

    Returns:
        Absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', None)
        if base_path is None:
            raise AttributeError("_MEIPASS not found")
    
    except (AttributeError, Exception):
        # Development mode - use the directory containing this script
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)

def get_script_path(script_name):
    """
    Get path to a script file, handling PyInstaller and development environments.

    Args:
        script_name: Name of the script (e.g., 'simi.py')

    Returns:
        Absolute path to the script
    """
    return get_resource_path(f'src/{script_name}')

def resource_exists(relative_path):
    """
    Check if a resource exists.

    Args:
        relative_path: Path relative to the project root

    Returns:
        True if the resource exists, False otherwise
    """
    return os.path.exists(get_resource_path(relative_path))

def get_asset_path(asset_name):
    """
    Get path to an asset file, handling PyInstaller and development environments.

    Args:
        asset_name: Name of the asset (e.g., 'icono_win.ico')

    Returns:
        Absolute path to the asset
    """
    return get_resource_path(f'assets/{asset_name}')

def get_base_path():
    """
    Get the base path of the application (useful for debugging).

    Returns:
        Base path string
    """
    try:
        base_path = getattr(sys, '_MEIPASS', None)
        if base_path is None:
            raise AttributeError("_MEIPASS not found")
        return base_path
    
    except (AttributeError, Exception):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
