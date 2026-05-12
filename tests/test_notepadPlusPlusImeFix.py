from __future__ import annotations

import importlib.util
import sys
import types
import unittest
from pathlib import Path


class _BaseScintilla:
	TextInfo = "baseTextInfo"


class _BuiltinNppEdit(_BaseScintilla):
	def _get_TextInfo(self):
		if self.appModule.is64BitProcess and self.appModule.productVersion.startswith("8.95"):
			return "npp83TextInfo"
		return super().TextInfo


def _installNvdaStubs() -> None:
	nvdaObjects = types.ModuleType("NVDAObjects")
	nvdaObjects.__path__ = []
	sys.modules["NVDAObjects"] = nvdaObjects

	inputComposition = types.ModuleType("NVDAObjects.inputComposition")
	inputComposition.InputCompositionTextInfo = "compositionTextInfo"
	sys.modules["NVDAObjects.inputComposition"] = inputComposition

	window = types.ModuleType("NVDAObjects.window")
	window.__path__ = []
	sys.modules["NVDAObjects.window"] = window

	scintilla = types.ModuleType("NVDAObjects.window.scintilla")
	scintilla.Scintilla = _BaseScintilla
	scintilla.ScintillaTextInfo = type("ScintillaTextInfo", (), {})
	sys.modules["NVDAObjects.window.scintilla"] = scintilla

	nvdaBuiltin = types.ModuleType("nvdaBuiltin")
	nvdaBuiltin.__path__ = []
	sys.modules["nvdaBuiltin"] = nvdaBuiltin

	builtinAppModules = types.ModuleType("nvdaBuiltin.appModules")
	builtinAppModules.__path__ = []
	sys.modules["nvdaBuiltin.appModules"] = builtinAppModules

	builtinNpp = types.ModuleType("nvdaBuiltin.appModules.notepadPlusPlus")
	builtinNpp.NppEdit = _BuiltinNppEdit
	builtinNpp.AppModule = type("AppModule", (), {})
	sys.modules["nvdaBuiltin.appModules.notepadPlusPlus"] = builtinNpp


def _loadAddonModule():
	_installNvdaStubs()
	modulePath = Path(__file__).parents[1] / "addon" / "appModules" / "notepadPlusPlus.py"
	spec = importlib.util.spec_from_file_location("addon_notepadPlusPlus", modulePath)
	assert spec and spec.loader
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


class NotepadPlusPlusImeFixTest(unittest.TestCase):
	def test_composition_text_info_is_prioritized_over_npp83_text_info(self):
		module = _loadAddonModule()
		obj = module.NppEdit()
		obj.appModule = types.SimpleNamespace(is64BitProcess=True, productVersion="8.95.0.0")
		obj.compositionString = "\u70cf\u9f9c"
		obj.compositionSelectionOffsets = (1, 1)
		obj.isReading = False

		self.assertEqual(obj._get_TextInfo(), "compositionTextInfo")

	def test_npp83_text_info_is_used_for_64_bit_notepad_plus_plus_without_composition(self):
		module = _loadAddonModule()
		obj = module.NppEdit()
		obj.appModule = types.SimpleNamespace(is64BitProcess=True, productVersion="8.95.0.0")
		obj.compositionString = ""
		obj.isReading = False

		self.assertEqual(obj._get_TextInfo(), "npp83TextInfo")

	def test_base_scintilla_text_info_is_kept_for_older_notepad_plus_plus(self):
		module = _loadAddonModule()
		obj = module.NppEdit()
		obj.appModule = types.SimpleNamespace(is64BitProcess=True, productVersion="8.21.0.0")
		obj.compositionString = ""
		obj.isReading = False

		self.assertEqual(obj._get_TextInfo(), "baseTextInfo")


if __name__ == "__main__":
	unittest.main()
