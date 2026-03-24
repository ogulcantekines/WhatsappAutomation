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


def normalize_group_id(raw: str) -> Optional[str]:
    """
    Accepts either a raw group id or a WhatsApp invite link and returns a clean group id.
    Example link: https://chat.whatsapp.com/AB123CDEFGHijklmn
    """
    s = raw.strip()
    if not s:
        return None

    # If user pasted the invite URL, extract the group id part.
    if "chat.whatsapp.com" in s:
        # Keep only the part after the last '/'.
        s = s.split("/")[-1]
    # Remove query parameters if present (e.g. "?foo=bar").
    s = s.split("?")[0].split("&")[0]

    # WhatsApp group invite codes are mostly alphanumeric.
    # Some codes may include '-' or '_' so we keep them.
    s = re.sub(r"[^A-Za-z0-9_-]", "", s)

    # Basic sanity check: group ids are short, but not empty.
    if len(s) < 8:
        return None
    return s


def main():
    show_banner()

    parser = argparse.ArgumentParser(description="Professional WhatsApp CLI Bot")
    parser.add_argument("-n", "--number", help="Target phone (country code, e.g. +905551234567)")
    parser.add_argument("-m", "--message", help="Message to send")
    parser.add_argument(
        "-g",
        "--group",
        help="WhatsApp group id (or invite link like https://chat.whatsapp.com/...)",
    )
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
    if not (args.number or args.group) or not args.message:
        console.print(
            "[dim italic]Hint(personal): python main.py -n <number> -m <message> [-w seconds][/dim italic] \n"
            "[dim italic]Hint(group): python main.py -g <group_id_or_link> -m <message> [-w seconds][/dim italic]"
        )
        console.print("")

    number_raw = args.number
    group_raw = args.group
    number = None
    group_id = None

    if not group_raw and not number_raw:
        mode = console.input(
            "[bold yellow]?[/bold yellow] Mode ([cyan]1[/cyan] Personal, [cyan]2[/cyan] Group): "
        ).strip()

        if mode == "1":
            number_raw = console.input(
                "[bold yellow]?[/bold yellow] Target number:(with country code, e.g. +905551234567): "
            ).strip()
            number = normalize_phone(number_raw)
            if not number:
                log(
                    "Invalid phone: use 10–15 digits with country code (e.g. +905551234567).",
                    level="error",
                )
                return
        elif mode == "2":
            group_raw = console.input("[bold yellow]?[/bold yellow] Group ID (or invite link): ").strip()
            group_id = normalize_group_id(group_raw) if group_raw else None
            if not group_id:
                log("Invalid group id/link. Please enter a valid group id or invite link.", level="error")
                return
        else:
            log("Invalid mode selected. Please choose 1 (Personal) or 2 (Group).", level="error")
            return
    else:
        if group_raw:
            group_id = normalize_group_id(group_raw)
            if not group_id:
                log("Invalid group id/link provided in -g.", level="error")
                return

        if not group_id:
            number = normalize_phone(number_raw) if number_raw else None
            if not number:
                if number_raw and number_raw.strip():
                    log(
                        "Invalid phone: use 10–15 digits with country code (e.g. +905551234567).",
                        level="error",
                    )
                else:
                    log("Operation cancelled due to missing information.", level="error")
                return

    message = args.message or console.input("[bold yellow]?[/bold yellow] Your message: ")

    message = message.strip()
    if not message:
        log("Operation cancelled: message is empty.", level="error")
        return

    target = group_id if group_id else number
    log(f"Operation started: [cyan]{target}[/cyan]")

    log("Browser is being triggered, please wait...")

    # Enforce a minimum wait time to give WhatsApp Web enough time to load.
    # Group chats often take longer to load before the message box is ready.
    min_wait = 25 if group_id else 5
    wait_time = max(args.wait_time, min_wait)
    if wait_time > args.wait_time:
        log(f"Wait time too low, setting to minimum {min_wait} seconds.", level="info")

    try:
        if group_id:
            pywhatkit.sendwhatmsg_to_group_instantly(
                group_id,
                message,
                wait_time=wait_time,
                tab_close=True,
                close_time=10,
            )
        else:
            pywhatkit.sendwhatmsg_instantly(
                number,
                message,
                wait_time=wait_time,
                tab_close=True
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
