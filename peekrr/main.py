import argparse
import sys
from rich.console import Console
from peekrr.config import load_config, save_config, get_config_path, prompt_for_config
from peekrr.api import JellyseerrAPI
from peekrr.interactive import interactive_select, interactive_home

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Peekrr CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for a title")
    search_parser.add_argument("query", nargs='+', help="Search query and optional filters")

    # Request command
    request_parser = subparsers.add_parser("request", help="Request a title")
    request_parser.add_argument("title", nargs='+', help="Title to request")

    # Requests command
    requests_parser = subparsers.add_parser("requests", help="Show current requests")
    requests_parser.add_argument("--status", help="Filter by status (pending, processing, partial, available, unavailable, all)", default="all")

    # Config Command
    config_parser = subparsers.add_parser("config", help="View or modify config")
    config_parser.add_argument("--set", nargs=1, help="Set a config value (key=value)")
    config_parser.add_argument("--edit", action="store_true", help="Re-run interactive setup")


    args = parser.parse_args()
    cfg = load_config()

    if args.command == "search":
        query = " ".join(args.query)
        api = JellyseerrAPI(cfg["jellyseerr_url"], cfg["api_key"])
        results = api.search(query)
        interactive_select(results)
        return

    if args.command == "request":
        title = " ".join(args.title)
        api = JellyseerrAPI(cfg["jellyseerr_url"], cfg["api_key"])
        results = api.search(title)
        selected = results[0] if results else None
        if not selected:
            console.print(f"[red]❌ No results found for:[/red] {title}")
            return
        response = api.request(selected["id"], selected.get("mediaType", "movie"))
        if response:
            console.print(f"✅ Requested [green]{selected.get('title') or selected.get('name')}[/green]")
        else:
            console.print("[red]❌ Request failed[/red]")
        return

    if args.command == "requests":
        api = JellyseerrAPI(cfg["jellyseerr_url"], cfg["api_key"])
        requests = api.get_requests()
        status_map = {
            "pending": 2,
            "processing": 3,
            "partial": 4,
            "available": 5,
            "unavailable": 1,
            "all": None
        }
        target_status = status_map.get(args.status.lower())
        filtered = []

        for r in requests:
            media_info = r.get("media")
            if not media_info:
                continue
            if target_status is None or media_info.get("status") == target_status:
                filtered.append(media_info)

        if not filtered:
            console.print("[yellow]No matching requests found[/yellow]")
        else:
            interactive_select(filtered)
        return

    if args.command == "config":
        path = get_config_path()
        current = load_config()

        if args.edit:
            updated = prompt_for_config()
            save_config(updated)
            console.print("[green]✅ Config updated via prompt.[/green]")
            return

        if args.set:
            keyval = args.set[0].split("=", 1)
            if len(keyval) != 2:
                console.print("[red]❌ Use --set key=value format[/red]")
                return
            key, value = keyval
            current[key.strip()] = value.strip()
            save_config(current)
            console.print(f"[green]✅ Updated:[/green] {key} = {value}")
        else:
            console.print("[cyan]Current config:[/cyan]")
            for k, v in current.items():
                console.print(f"{k}: {v}")
        return


    # No command, launch menu
    api = JellyseerrAPI(cfg["jellyseerr_url"], cfg["api_key"])
    interactive_home(api)
