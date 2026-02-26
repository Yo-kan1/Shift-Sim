@echo off
:: バッチファイルの場所を起点にする
cd /d "%~dp0"
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==========================================
echo    Python ＆ JS 一括クリーンアップツール
echo    対象範囲: %~dp0
echo ==========================================

:: 1. pipreqsの確認（Python用）
pip show pipreqs >nul 2>&1
if %errorlevel% neq 0 (
    echo [準備] pipreqsをインストールしています...
    pip install pipreqs >nul 2>&1
)

:: 2. すべてのサブフォルダをスキャン
for /r /d %%d in (*) do (
    set "target_dir=%%d"
    
    :: --- Pythonプロジェクトの処理 ---
    if exist "%%d\*.py" (
        echo ------------------------------------------
        echo [Python] フォルダ確認: %%d
        
        :: レシピ作成
        pushd "%%d"
        pipreqs . --encoding=utf8 --force >nul 2>&1
        echo   - requirements.txt を更新しました
        popd
        
        :: venv削除
        if exist "%%d\venv" (
            rmdir /s /q "%%d\venv" 2>nul
            echo   - venv を削除しました
        )
        if exist "%%d\.venv" (
            rmdir /s /q "%%d\.venv" 2>nul
            echo   - .venv を削除しました
        )
    )

    :: --- JavaScript (Node.js) プロジェクトの処理 ---
    if exist "%%d\package.json" (
        if exist "%%d\node_modules" (
            echo ------------------------------------------
            echo [JS] フォルダ確認: %%d
            rmdir /s /q "%%d\node_modules" 2>nul
            echo   - node_modules を削除しました
        )
    )

    :: --- 共通キャッシュの削除 ---
    if exist "%%d\__pycache__" (
        rmdir /s /q "%%d\__pycache__" 2>nul
        echo   - __pycache__ を削除しました
    )
)

echo ==========================================
echo    整理完了！NASへのコピー準備が整いました。
echo ==========================================
pause