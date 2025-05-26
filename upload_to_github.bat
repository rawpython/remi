@echo off
setlocal enabledelayedexpansion


:: GitHub 仓库地址（仅显示用）

:: GitHub 仓库地址

set REPO_URL=https://github.com/a764519892/remi.git

:: 当前目录
set PROJECT_DIR=%cd%
cd /d %PROJECT_DIR%


:: 添加所有文件
git add .

:: 获取当前日期时间
for /f "tokens=1-4 delims=/ " %%a in ("%date%") do (
    set mydate=%%a-%%b-%%c
)
for /f "tokens=1-2 delims=: " %%a in ("%time%") do (
    set mytime=%%a-%%b
)

:: 提交并推送
git commit -m "Auto commit on !mydate! !mytime!"
git branch -M main
git push -u origin main
git submodule update --checkout --recursive

echo ? 已上传： %REPO_URL%

:: 获取时间戳
for /f %%i in ('powershell -command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set "timestamp=%%i"

echo ---------------------------------------
echo ?? 正在处理子模块递归提交和上传...
echo ---------------------------------------

:: 遍历所有子模块目录并提交上传
for /f "delims=" %%s in ('git config --file .gitmodules --get-regexp path ^| awk "{ print $2 }"') do (
    echo ?? 进入子模块：%%s
    cd %%s
    git add .
    git commit -m "Submodule auto commit on !timestamp!" >nul 2>&1
    if errorlevel 1 (
        echo ?? 子模块 %%s 没有变更，跳过提交。
    ) else (
        git push
        echo ? 子模块 %%s 已上传。
    )
    cd %PROJECT_DIR%
)

echo ---------------------------------------
echo ?? 正在提交主项目...
echo ---------------------------------------

:: 主项目添加所有变动（包括子模块引用更新）
git add .

:: 提交
git commit -m "Auto commit on !timestamp!" >nul 2>&1
if errorlevel 1 (
    echo ?? 主项目没有变更，跳过 push。
    goto end
)

:: 推送主项目
git branch -M main
git push -u origin main

:end
echo ---------------------------------------
echo ? 所有变更已上传： %REPO_URL%

pause
