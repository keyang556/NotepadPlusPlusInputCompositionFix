# A part of the Notepad++ IME composition fix add-on for NVDA.
# This file may be used under the terms of the GNU General Public License, version 2 or later.

"""AppModule for Notepad++.

The add-on extends NVDA's built-in Notepad++ module instead of replacing its
64-bit Scintilla support. The only behavioral change is that active IME
composition objects keep NVDA's InputCompositionTextInfo.
"""

from NVDAObjects.inputComposition import InputCompositionTextInfo
from nvdaBuiltin.appModules import notepadPlusPlus as builtInNotepadPlusPlus


def _hasActiveInputComposition(obj) -> bool:
	"""Return True when NVDA has current IME composition text on this object."""

	if getattr(obj, "isReading", False):
		return bool(getattr(obj, "readingString", ""))
	return bool(getattr(obj, "compositionString", ""))


class NppEdit(builtInNotepadPlusPlus.NppEdit):
	def _get_TextInfo(self):
		if _hasActiveInputComposition(self):
			return InputCompositionTextInfo
		return super()._get_TextInfo()


class AppModule(builtInNotepadPlusPlus.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "Scintilla" and obj.windowControlID == 0:
			clsList.insert(0, NppEdit)
