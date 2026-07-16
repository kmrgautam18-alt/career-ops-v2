"""
Plugin System Architecture — Extend Career-Ops with third-party plugins.
Supports job scrapers, AI providers, resume parsers, and notification channels.
"""

from __future__ import annotations

import importlib
import json
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

PLUGIN_DIR = Path(os.getenv("PLUGIN_DIR", "/data/plugins"))
REGISTRY_FILE = PLUGIN_DIR / "registry.json"


# ==============================================================================
# Plugin Types
# ==============================================================================


class PluginType:
    JOB_SCRAPER = "job_scraper"
    AI_PROVIDER = "ai_provider"
    RESUME_PARSER = "resume_parser"
    NOTIFICATION_CHANNEL = "notification_channel"
    ANALYTICS = "analytics"


# ==============================================================================
# Plugin Interface
# ==============================================================================


class PluginInterface(ABC):
    """Abstract base class for all plugins."""

    @property
    @abstractmethod
    def plugin_id(self) -> str: ...

    @property
    @abstractmethod
    def plugin_type(self) -> str: ...

    @property
    @abstractmethod
    def version(self) -> str: ...

    @abstractmethod
    def health_check(self) -> bool: ...

    @abstractmethod
    def initialize(self) -> bool: ...

    @abstractmethod
    def shutdown(self) -> bool: ...


# ==============================================================================
# Plugin Registry
# ==============================================================================


@dataclass
class PluginMeta:
    """Metadata about an installed plugin."""
    plugin_id: str
    plugin_type: str
    version: str
    source: str
    enabled: bool = True
    health_status: bool = False
    config: dict[str, Any] = field(default_factory=dict)


class PluginRegistry:
    """Manages plugin discovery, loading, and lifecycle."""

    def __init__(self) -> None:
        self._plugins: dict[str, PluginInterface] = {}
        self._metadata: dict[str, PluginMeta] = {}

    def discover(self) -> list[PluginMeta]:
        """Discover plugins from the plugin directory."""
        PLUGIN_DIR.mkdir(parents=True, exist_ok=True)

        discovered: list[PluginMeta] = []

        # Check Python packages with careerops_ prefix
        for entry in PLUGIN_DIR.iterdir():
            if entry.is_dir() and entry.name.startswith(("careerops_", "co_")):
                meta_file = entry / "plugin.json"
                if meta_file.exists():
                    try:
                        with open(meta_file) as f:
                            data = json.load(f)
                        meta = PluginMeta(
                            plugin_id=data["id"],
                            plugin_type=data["type"],
                            version=data.get("version", "0.1.0"),
                            source=str(entry),
                            enabled=data.get("enabled", True),
                            config=data.get("config", {}),
                        )
                        discovered.append(meta)
                    except (json.JSONDecodeError, KeyError) as e:
                        logger.warning(f"Invalid plugin manifest in {entry}: {e}")

        return discovered

    def load(self, plugin_id: str) -> bool:
        """Load and initialize a plugin by ID."""
        if plugin_id in self._plugins:
            return True

        meta = self._metadata.get(plugin_id)
        if meta is None:
            logger.warning(f"Plugin {plugin_id} not found in registry")
            return False

        try:
            # Try dynamic import
            module_path = meta.source.replace("/", ".")
            module = importlib.import_module(module_path)
            if hasattr(module, "create_plugin"):
                plugin = module.create_plugin()
            else:
                logger.warning(f"Plugin {plugin_id} has no create_plugin()")
                return False

            if not plugin.initialize():
                logger.warning(f"Plugin {plugin_id} failed to initialize")
                return False

            self._plugins[plugin_id] = plugin
            meta.health_status = plugin.health_check()
            return True

        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_id}: {e}")
            return False

    def unload(self, plugin_id: str) -> bool:
        """Shutdown and unload a plugin."""
        plugin = self._plugins.pop(plugin_id, None)
        if plugin is None:
            return False
        try:
            plugin.shutdown()
            return True
        except Exception as e:
            logger.error(f"Error shutting down plugin {plugin_id}: {e}")
            return False

    def get_plugin(self, plugin_id: str) -> PluginInterface | None:
        """Get a loaded plugin instance."""
        return self._plugins.get(plugin_id)

    def get_plugins_by_type(self, plugin_type: str) -> list[PluginInterface]:
        """Get all loaded plugins of a specific type."""
        return [p for p in self._plugins.values() if p.plugin_type == plugin_type]

    def save_registry(self) -> None:
        """Persist the plugin registry to disk."""
        REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = {
            pid: {
                "plugin_id": m.plugin_id,
                "plugin_type": m.plugin_type,
                "version": m.version,
                "source": m.source,
                "enabled": m.enabled,
                "config": m.config,
            }
            for pid, m in self._metadata.items()
        }
        with open(REGISTRY_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load_registry(self) -> None:
        """Load persisted plugin registry."""
        if REGISTRY_FILE.exists():
            try:
                with open(REGISTRY_FILE) as f:
                    data = json.load(f)
                for pid, mdata in data.items():
                    self._metadata[pid] = PluginMeta(**mdata)
            except (json.JSONDecodeError, Exception) as e:
                logger.warning(f"Failed to load plugin registry: {e}")


# Global singleton
registry = PluginRegistry()
