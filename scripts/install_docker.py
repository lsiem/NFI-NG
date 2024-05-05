import platform
import subprocess
import webbrowser


def install_docker():
    os_type = platform.system()
    print(f"Starting Docker installation for {os_type}...")

    if os_type == "Linux":
        install_docker_linux()
    elif os_type == "Darwin":
        install_docker_macos()
    elif os_type == "Windows":
        install_docker_windows()
    else:
        print("Unsupported OS. Please install Docker manually.")


def check_docker_installed():
    """Check if Docker is installed by trying to get its version."""
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True, check=True)
        if "Docker version" in result.stdout:
            return True
    except subprocess.CalledProcessError:
        return False
    return False


def install_docker_linux():
    try:
        print("Checking for existing Docker installation on Linux...")
        if not check_docker_installed():
            print("Docker not found, installing...")
            subprocess.run(["curl", "-fsSL", "https://get.docker.com", "-o", "get-docker.sh"], check=True)
            subprocess.run(["sh", "get-docker.sh"], check=True)
            print("Docker installed successfully on Linux.")
        else:
            print("Docker is already installed on Linux.")
    except Exception as e:
        print(f"Failed to install Docker on Linux: {e}")


def install_docker_macos():
    try:
        print("Checking for existing Docker installation on macOS...")
        if not check_docker_installed():
            print("Docker not found, installing...")
            subprocess.run(["/bin/bash", "-c", "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"], check=True)
            subprocess.run(["brew", "install", "--cask", "docker"], check=True)
            print("Docker installed successfully on macOS.")
        else:
            print("Docker is already installed on macOS.")
    except Exception as e:
        print(f"Failed to install Docker on macOS: {e}")


def install_docker_windows():
    try:
        print("Checking for existing Docker installation on Windows...")
        if not check_docker_installed():
            print("Docker not found, please download and install Docker Desktop manually.")
            webbrowser.open("https://www.docker.com/products/docker-desktop")
        else:
            print("Docker is already installed on Windows.")
    except Exception as e:
        print(f"Failed to check Docker installation on Windows: {e}")


if __name__ == "__main__":
    install_docker()
