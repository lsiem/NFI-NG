import subprocess
import json
import re
from textual.app import ComposeResult
from textual.widgets import Button, Input, Header, Footer, Static
from textual.containers import Horizontal, Vertical
from textual.screen import Screen


def load_config():
    with open('user_data/config-private.json', 'r') as f:
        return json.load(f)


def save_config(config):
    # Load the existing configuration from the JSON file
    with open('user_data/config-private.json', 'r') as f:
        existing_config = json.load(f)

    # Update the existing configuration with the new values
    existing_config.update(config)

    # Validate the updated configuration
    if validate_inputs(existing_config):
        # Write the updated configuration back to the JSON file
        with open('user_data/config-private.json', 'w') as f:
            json.dump(existing_config, f, indent=4)
        return True
    else:
        return False


def validate_inputs(config):
    patterns = {
        'telegram_token': r'^\d{9,10}:[A-Za-z0-9_-]{35}$',
        'telegram_chat_id': r'^-?\d{9,10}$'
    }
    if not re.match(patterns['telegram_token'], config['telegram']['token']):
        return False
    if not re.match(patterns['telegram_chat_id'], config['telegram']['chat_id']):
        return False
    return True


def start_bot():
    subprocess.Popen(['docker-compose', 'up', '-d'], cwd='../')


def stop_bot():
    subprocess.Popen(['docker-compose', 'down'], cwd='../')


class BotManagementScreen(Screen):
    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name=name, id=id, classes=classes)
        self.config = load_config()  # Load configuration during initialization

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer("NFI-NG by lsiem")
        with Vertical(id="bot_management_form"):
            yield Static("Change your settings here")
            yield Input(placeholder="Binance API Key", id="api_key", classes="input",
                        value=self.config.get('binance', {}).get('api_key', ''))
            yield Input(placeholder="Binance API Secret", id="api_secret", classes="input", password=True,
                        value=self.config.get('binance', {}).get('api_secret', ''))
            yield Input(placeholder="Telegram Token", id="telegram_token", classes="input",
                        value=self.config.get('telegram', {}).get('token', ''))
            yield Input(placeholder="Telegram Chat ID", id="telegram_chat_id", classes="input",
                        value=self.config.get('telegram', {}).get('chat_id', ''))
            with Horizontal():
                yield Button("Start Bot", id="start_bot", variant="primary")
                yield Button("Stop Bot", id="stop_bot", variant="error")
                yield Button("Restart Bot", id="restart_bot", variant="warning")
                yield Button("Save Settings", id="save_settings", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start_bot":
            self.start_bot()
        elif event.button.id == "stop_bot":
            self.stop_bot()
        elif event.button.id == "restart_bot":
            self.restart_bot()
        elif event.button.id == "save_settings":
            self.save_settings()

    async def start_bot(self) -> None:
        start_bot()

    async def stop_bot(self) -> None:
        stop_bot()

    async def restart_bot(self) -> None:
        stop_bot()
        start_bot()

    async def save_settings(self) -> None:
        api_key = self.query_one("#api_key", Input).value
        api_secret = self.query_one("#api_secret", Input).value
        telegram_token = self.query_one("#telegram_token", Input).value
        telegram_chat_id = self.query_one("#telegram_chat_id", Input).value

        config = {
            'binance': {'api_key': api_key, 'api_secret': api_secret},
            'telegram': {'token': telegram_token, 'chat_id': telegram_chat_id}
        }

        if save_config(config):
            self.app.log("Settings saved successfully!")
        else:
            self.app.log("Invalid input. Please check your entries and try again.")
