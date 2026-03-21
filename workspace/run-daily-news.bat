@echo off
chcp 65001 >nul
echo Starting Daily News Bot...
set PATH=%PATH%;C:\Users\Administrator\AppData\Local\Programs\Python\Python312
cd /d C:\Users\Administrator\.openclaw\workspace
python daily-news-bot.py >> news-bot.log 2>&1
echo Done.
