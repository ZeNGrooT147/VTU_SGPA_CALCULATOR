@echo off
echo ========================================
echo VTU SGPA Calculator - Vercel Deployment
echo ========================================
echo.

echo Checking if Vercel CLI is installed...
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Vercel CLI not found. Installing...
    npm install -g vercel
    if %errorlevel% neq 0 (
        echo Failed to install Vercel CLI. Please install Node.js first.
        pause
        exit /b 1
    )
)

echo.
echo Starting deployment...
echo.

vercel --prod

echo.
echo Deployment completed!
echo Check your Vercel dashboard for the live URL.
pause
