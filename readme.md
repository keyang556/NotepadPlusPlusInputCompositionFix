# 停止維護和遷移說明 / archive and migreation.

此專案的所有內容已經整合至 NotepadPlusPlus 附加元件，請改安裝 https://github.com/derekriemer/nvda-notepadPlusPlus/ 的版本。

Please use https://github.com/derekriemer/nvda-notepadPlusPlus/ version.

# Notepad++ IME composition fix

This NVDA add-on restores caret reporting for uncommitted IME composition text in
64-bit Notepad++ 8.3 and later.

It addresses nvaccess/nvda#14152, where moving the caret inside Chinese IME
composition text in Notepad++ could produce blank speech and no braille update
with NVDA 2022.1 and later.

The add-on keeps NVDA's Notepad++ 64-bit Scintilla TextInfo fix for normal editor
text, and only prioritizes NVDA's input-composition TextInfo while an active IME
composition or reading string exists.

## Compatibility note

This add-on overrides NVDA's Notepad++ app module. It may conflict with other
NVDA add-ons that also customize Notepad++. Before installing this add-on,
uninstall or disable other Notepad++ related NVDA add-ons.
