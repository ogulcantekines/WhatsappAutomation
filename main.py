# WhatsApp Automation - CLI Tool
# Sends a WhatsApp message instantly via WhatsApp Web using pywhatkit.
# Supports both argument-based and interactive usage.
#
# Usage:
#   python main.py -n +905551234567 -m "Hello!"
#   python main.py  (interactive mode)

import argparse
import datetime
import re
from typing import Optional

import pywhatkit
from rich.console import Console
from rich.panel import Panel

console = Console()


def show_banner():
    # Displays the welcome banner at startup.
    banner_text = (
        "[bold green]WHATSAPP AUTOMATION[/bold green]\n"
        "[cyan]Professional CLI Tool v1.0[/cyan]\n"
        "[white]Developed by Oğulcan Tekineş[/white]"
    )
    console.print(Panel(banner_text, expand=False, border_style="blue"))


def log(message, level="info"):
    # Prints a timestamped log message.
    # Levels: "info" (cyan), "success" (green), "error" (red)
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    if level == "success":
        console.print(f"[dim]{time_str}[/dim] [bold green]✔[/bold green] {message}")
    elif level == "error":
        console.print(f"[dim]{time_str}[/dim] [bold red]✘[/bold red] {message}")
    else:
        console.print(f"[dim]{time_str}[/dim] [bold cyan]![/bold cyan] {message}")


def normalize_phone(raw: str) -> Optional[str]:
    # Strips non-digit characters and validates the phone number length (10–15 digits).
    # Returns a E.164-style string (e.g. "+905551234567") or None if invalid.
    s = raw.strip()
    if not s:
        return None
    digits = re.sub(r"\D", "", s)
    if len(digits) < 10 or len(digits) > 15:
        return None
    return f"+{digits}"


def main():
    show_banner()

    parser = argparse.ArgumentParser(description="Professional WhatsApp CLI Bot")
    parser.add_argument("-n", "--number", help="Target phone (country code, e.g. +905551234567)")
    parser.add_argument("-m", "--message", help="Message to send")
    parser.add_argument(
        "-w",
        "--wait-time",
        type=int,
        default=25,
        metavar="SEC",
        help="Seconds to wait for WhatsApp Web before sending (default: 25)",
    )
    args = parser.parse_args()

    # If any required argument is missing, show usage hint and fall back to interactive mode.
    if not args.number or not args.message:
        console.print(
            "[dim italic]Hint: python main.py -n <number> -m <message> [-w seconds][/dim italic]"
        )
        console.print("")

    number_raw = args.number or console.input(
        "[bold yellow]?[/bold yellow] Target number (+country...): "
    )
    message = args.message or console.input("[bold yellow]?[/bold yellow] Your message: ")

    number = normalize_phone(number_raw)
    if not number:
        if number_raw.strip():
            log(
                "Invalid phone: use 10–15 digits with country code (e.g. +905551234567).",
                level="error",
            )
        else:
            log("Operation cancelled due to missing information.", level="error")
        return

    message = message.strip()
    if not message:
        log("Operation cancelled: message is empty.", level="error")
        return

    log(f"Operation started: [cyan]{number}[/cyan]")
    log("Browser is being triggered, please wait...")

    # Enforce a minimum wait time to give WhatsApp Web enough time to load.
    if args.wait_time < 5:
        log("Wait time too low, setting to minimum 5 seconds.", level="info")
        args.wait_time = 5

    try:
        pywhatkit.sendwhatmsg_instantly(
            number, message, wait_time=args.wait_time, tab_close=True
        )
        log("Message sent successfully!", level="success")
    except Exception as e:
        log(f"An error occurred: {e}", level="error")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n")
        log("Operation cancelled by user.", level="error")
