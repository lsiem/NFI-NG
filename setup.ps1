# Ensure the script stops on any errors
$ErrorActionPreference = "Stop"

function Test-RequiredTools {
    if (-not (Get-Command "git" -ErrorAction SilentlyContinue)) {
        Write-Error "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): Git is not installed."
        exit 1
    }
    if (-not (Get-Command "python3" -ErrorAction SilentlyContinue)) {
        Write-Error "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): Python is not installed."
        exit 1
    }
}

function Sync-Repository {
    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): Cloning the repository..."
    try {
        git clone https://github.com/lsiem/crypto-bot.git
        Set-Location -Path "./crypto-bot"
        if (-not (Test-Path ".git")) {
            Write-Error "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): The repository was not cloned properly."
            exit 1
        }
        git checkout main
    } catch {
        Write-Error "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): An error occurred while cloning the repository: $_"
        exit 1
    }
}

function Initialize-VirtualEnvironment {
    try {
        python3 -m venv .venv
        . .\.venv\Scripts\Activate.ps1
        pip install -r requirements.txt
    } catch {
        Write-Error "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): An error occurred while setting up the virtual environment: $_"
        exit 1
    }
}

function Start-SetupWizard {
    try {
        python3 .\scripts\tui_setup_wizard.py
        Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): Setup completed successfully!"
    } catch {
        Write-Error "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): An error occurred while running the setup wizard: $_"
        exit 1
    }
}

# Execute functions
Test-RequiredTools
Sync-Repository
Initialize-VirtualEnvironment
Start-SetupWizard

