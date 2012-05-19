@echo off
IF EXISTS ldg.log MOVE ldg.log ldg.log_old
start /B ".\main\__main__.exe"
