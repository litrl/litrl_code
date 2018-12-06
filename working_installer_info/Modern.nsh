;this file is to be used with zip2exe in NSIS
;the installer could use a little TLC and an uninstaller...

!include "MUI2.nsh"

!define MUI_PRODUCT "Litrl Browser"
!define MUI_FILE "LitrlBrowser"
!define MUI_BRANDINGTEXT "Litrl Browser: The News Verification Suite"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

!define MUI_CUSTOMFUNCTION_GUIINIT PreInstall
!define MUI_PAGE_CUSTOMFUNCTION_PRE PostInstall

!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Function PreInstall
	MessageBox MB_YESNO "Litrl Browser is licensed under the terms of the GNU GPLv3 (a copy of it can be found in the folder where Litrl is installed after). Would you like to read a copy of it now?" IDYES "true" IDNO "false"
	true:
		ExecShell open "https://www.gnu.org/licenses/gpl-3.0.en.html"
	false:
FunctionEnd

Function PostInstall
	
	;create desktop shortcut
	CreateShortCut "$DESKTOP\${MUI_PRODUCT}.lnk" "$INSTDIR\${MUI_FILE}.exe" "" "$INSTDIR\logo_full.ico"
	 
	;fixme: python crashes or closes instantly in program files. For now, we will just install to the desktop as a workaround
	;since there is no uninstaller a user can just delete the folder
	;create start-menu items
	;CreateDirectory "$SMPROGRAMS\${MUI_PRODUCT}"
	;CreateShortCut "$SMPROGRAMS\${MUI_PRODUCT}\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\Uninstall.exe" 0
	;CreateShortCut "$SMPROGRAMS\${MUI_PRODUCT}\${MUI_PRODUCT}.lnk" "$INSTDIR\${MUI_FILE}.exe" "" "$INSTDIR\logo_full.ico"
	
	MessageBox MB_OK "Litrl Browser depends on Python 2.7, and several Python packages. These will now be installed."
    ExecWait '"$INSTDIR\install.cmd"' "$INSTDIR"
	MessageBox MB_OK "To uninstall Litrl Browser, simply delete the folder and shortcut to it on your desktop."
	
FunctionEnd