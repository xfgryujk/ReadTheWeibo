@echo off
call pyuic5 -o ui_mainwindow.py ui\mainwindow.ui
call pyuic5 -o ui_login_dlg.py ui\login_dlg.ui
call pyuic5 -o ui_popup_post.py ui\popup_post.ui
call pyrcc5 -o res_rc.py ui\res.qrc
