^!r::REload ; Ctrl + Alt + R

NumpadIns::
MsgBox,
(
hotkeys
NumpadDot (NumpadDel) - launch php my admin
Numpad 0 (NumpadIns) - help
Numpad 5 (NumpadClear) - launch vocabulary.com
Numpad 7 (NumpadHome) - create 1-5 number list
Numpad 8 (NumpadUp) - input dialog that create a number list
Numpad 9 (NumpadPgUp) - open or bring to focus xampp application

hotstrings
"imgfig " -> "Image figure: "
)
return

NumpadDel::
Run, http://localhost/phpmyadmin/db_structure.php?server=1&db=phpmotors
return

NumpadClear::
Run, https://www.vocabulary.com/dictionary/
return


; create a number-list up to 5
NumpadHome::
Send, {Shift Up}
Send,
(
1 -{space}
2 -{space}
3 -{space}
4 -{space}
5 -{space}
)
return

NumpadUp::
InputBox, total, Enter total lines
if not ErrorLevel
  message = 
  Loop, %total% {
    if (total == A_Index)
      message .= A_Index . " - "
    else
      message .= A_Index . " - `n"
  }
  Send, {Enter Up}
  Send, %message%
return

NumpadPgUp::
if not WinExist("ahk_exe C:\xampp\xampp-control.exe")
 Run, C:\xampp\xampp-control.exe
else
 WinActivate, ahk_exe C:\xampp\xampp-control.exe
return

::imgfig::Image figure:
:*:<?::<?php ?>


~RButton & LButton::
    ; Send Y
    Send, {LWin}
Return

; RButton & LButton::
; Send, {win}
; return
