#!/usr/bin/env bash
set -e
set -u

check_required_tools() {
    if ! command -v git &> /dev/null; then
        echo "git could not be found, please install git."
        exit 1
    fi

    if ! command -v python3 &> /dev/null; then
        echo "python3 could not be found, please install python3."
        exit 1
    fi
}

clone_repository() {
    local REPO_URL="https://github.com/lsiem/crypto-bot.git"
    echo "Cloning the repository..."
    git clone $REPO_URL
    cd crypto-bot
    git checkout main
}

create_and_activate_virtualenv() {
    echo "Creating a virtual environment..."
    python3 -m venv .venv

    echo "Activating the virtual environment..."
    if [[ "$(uname -s)" == "Linux" ]] || [[ "$(uname -s)" == "Darwin" ]]; then
        source .venv/bin/activate
    else
        source .venv/Scripts/activate
    fi
}

install_requirements() {
    echo "Installing requirements..."
    pip install -r requirements.txt
}

run_setup_wizard() {
    echo "Running the setup wizard..."
    python3 scripts/tui_setup_wizard.py
}

# Main execution flow
check_required_tools
clone_repository
create_and_activate_virtualenv
install_requirements
run_setup_wizard

