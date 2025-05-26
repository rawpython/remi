@echo off
setlocal enabledelayedexpansion

:: 第一次运行初始化 Git 仓库
git config --global user.name "a764519892"
git config --global user.email "a764519892@qq.com"

:: GitHub 仓库地址
set REPO_URL=https://github.com/a764519892/remi.git

:: 当前目录作为项目目录
set PROJECT_DIR=%cd%
cd /d %PROJECT_DIR%

:: 初始化仓库并绑定远程
echo ?? 正在初始化 Git 仓库...
git init
git remote add origin %REPO_URL%

:: 拉取远程仓库（防止 push 被拒绝）
echo ?? 正在拉取远程分支...
git pull origin main --allow-unrelated-histories

echo ? 初始化完成，请使用 upload_git.bat 上传代码
pause
