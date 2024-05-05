import json
import re
import subprocess
import threading
import time
import schedule
from install_docker import install_docker
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, Static
from textual.containers import Vertical, Horizontal
from textual.screen import Screen

from bot_management_gui import BotManagementScreen


def run_update() -> None:
    subprocess.run(['python', 'scripts/auto_update.py'], check=True)


def schedule_updates() -> None:
    schedule.every().hour.at(":00").do(run_update)
    while True:
        schedule.run_pending()
        time.sleep(60)


class TUIApp(App):
    TITLE = "NFI-NG by lsiem"

    async def on_mount(self) -> None:
        threading.Thread(target=schedule_updates, daemon=True).start()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, name="NFI-NG by lsiem")
        yield Footer()
        with Vertical(id="form"):
            yield Static("Welcome to the NFI-NG Setup Wizard!")
            yield Button("Installation", id="installation", variant="primary")
            yield Button("Management", id="management", variant="primary")
            yield Button("Cancel", id="cancel", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "installation":
            self.push_screen(InstallationScreen())
        elif event.button.id == "management":
            self.push_screen(BotManagementScreen())
        elif event.button.id == "cancel":
            self.exit()


class InstallationScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer("NFI-NG by lsiem")
        with Vertical(id="form") as form:
            yield Static("Please enter your Binance API keys as well as your Telegram bot token and chat ID.")
            yield Input(placeholder="Binance API Key", id="api_key", classes="input")
            yield Input(placeholder="Binance API Secret", id="api_secret", classes="input", password=True)
            yield Input(placeholder="Telegram Token", id="telegram_token", classes="input")
            yield Input(placeholder="Telegram Chat ID", id="telegram_chat_id", classes="input")
            with Horizontal(id="buttons"):
                yield Button("Proceed", id="proceed", variant="primary")
                yield Button("Cancel", id="cancel", variant="error")
        yield form

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "proceed":
            self.on_proceed_clicked()
        elif event.button.id == "cancel":
            self.on_cancel_clicked()

    async def on_proceed_clicked(self) -> None:
        api_key = self.query_one("#api_key", Input).value
        api_secret = self.query_one("#api_secret", Input).value
        telegram_token = self.query_one("#telegram_token", Input).value
        telegram_chat_id = self.query_one("#telegram_chat_id", Input).value

        if not re.match(r"^[A-Za-z0-9]{64}$", api_key):
            self.app.bell()
            self.query_one("#api_key", Input).focus()
            return
        if not re.match(r"^[A-Za-z0-9]{64}$", api_secret):
            self.app.bell()
            self.query_one("#api_secret", Input).focus()
            return
        if not re.match(r"^[0-9]{9}:[A-Za-z0-9_-]{35}$", telegram_token):
            self.app.bell()
            self.query_one("#telegram_token", Input).focus()
            return
        if not re.match(r"^-?\d+$", telegram_chat_id):
            self.app.bell()
            self.query_one("#telegram_chat_id", Input).focus()
            return

        await self.write_config(api_key, api_secret, telegram_token, telegram_chat_id)
        install_docker()
        await self.app.push_screen(BotManagementScreen())  # Launch the BotManagementApp

    async def on_cancel_clicked(self) -> None:
        self.app.exit()

    @staticmethod
    async def write_config(api_key: str, api_secret: str, telegram_token: str, telegram_chat_id: str) -> None:
        # Load the existing configuration from the JSON file
        with open('user_data/config-private.json', 'r') as f:
            config = json.load(f)

        # Update the configuration with new values
        config['exchange']['key'] = api_key
        config['exchange']['secret'] = api_secret
        config['telegram']['token'] = telegram_token
        config['telegram']['chat_id'] = telegram_chat_id

        # Write the updated configuration back to the JSON file
        with open('user_data/config-private.json', 'w') as f:
            json.dump(config, f, indent=4)


if __name__ == "__main__":
    app = TUIApp()
    app.run()
