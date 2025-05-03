import questionary
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from textwrap import dedent
from peekrr.constants import ICONS
from datetime import datetime

console = Console()

def extract_year(item):
    date = item.get("releaseDate") or item.get("firstAirDate") or ""
    return int(date[:4]) if date[:4].isdigit() else 0

def get_display_title(item):
    title = item.get("title") or item.get("name") or "Unknown"
    year = (item.get("releaseDate") or item.get("firstAirDate") or "")[:4]
    media_type = item.get("mediaType", "movie")
    emoji = ICONS.get(media_type, "🎬")
    return f"{emoji} {title} ({year})"

def get_status_label(item):
    media_info = item.get("mediaInfo", {})
    status_map = {
        0: ("🛑 Not Available", "📥 Request This Title"),  # Unknown status, treated as "Not Available"
        1: ("🛑 Not Available", "📥 Request This Title"),  # Unknown status, treated as "Not Available"
        2: ("🔄 Requested, Awaiting Approval", "🔄 Already Requested"),  # Pending/Requested
        3: ("🛠️ Request Approved and Processing", "🛠️ Processing"),  # Processing
        4: ("📥 Partially Available", "📥 Partially Available"),  # Partially Available
        5: ("📀 Available", "📀 Already Available (No Request Needed)"),  # Available
    }

    status = media_info.get("status", 1)  # Default to "UNKNOWN" if status is not available
    media_id = media_info.get("jellyfinMediaId") or media_info.get("ratingKey")
    label, action_button = status_map.get(status, status_map[1])  # Default to "Not Available"

    # Override if status is "Available" but no media ID is found
    if status == 5 and not media_id:
        label, action_button = status_map[1]  # If available but no media ID, treat as "Not Available"

    return label, action_button

def show_metadata_panel(item):
    title = item.get("title") or item.get("name") or "Unknown"
    year = (item.get("releaseDate") or item.get("firstAirDate") or "")[:4]
    description = item.get("overview", "No description available.")
    media_type = item.get("mediaType", "movie")
    type_label = "Movie" if media_type == "movie" else "TV Show"
    
    status_label, action_button = get_status_label(item)
    
    genres = ", ".join([g["name"] for g in item.get("genres", [])]) or "Unknown"
    media_info = item.get("mediaInfo", {})
    requester = media_info.get("requestedBy", {}).get("displayName", "Unknown")
    service = "Jellyfin" if media_info.get("jellyfinMediaId") else "Plex" if media_info.get("ratingKey") else "Unknown"

    def format_date(date_str):
        if not date_str:
            return "Unknown"
        return datetime.fromisoformat(date_str.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")

    created = format_date(media_info.get("createdAt"))
    added = format_date(media_info.get("mediaAddedAt"))

    text = dedent(f"""
        [bold]📄 Media Request Details[/bold]

        [bold]Title:[/bold] {title}
        [bold]Media Type:[/bold] {type_label}
        [bold]Request Status:[/bold] {status_label}
        [bold]Year:[/bold] {year}
        [bold]Genres:[/bold] {genres}
        [bold]Requested By:[/bold] {requester}
        [bold]Service:[/bold] {service}
        [bold]Request Created:[/bold] {created}
        [bold]Media Added:[/bold] {added}
        [bold]Description:[/bold] {description}
    """)

    panel = Panel.fit(Align.left(text), title="Metadata Preview", border_style="cyan")
    console.print(panel)

def interactive_select(results):
    if not results:
        console.print("[red]No results found.[/red]")
        return None

    sorted_results = sorted(results, key=extract_year, reverse=True)
    offset = 0
    step = 10
    total = len(sorted_results)

    while True:
        visible = sorted_results[offset:offset + step]
        choices = [
            questionary.Choice(get_display_title(item), value=item)
            for item in visible
        ]

        if offset > 0:
            choices.append(questionary.Choice("⬅️ Previous Page", value="__prev__"))
        if offset + step < total:
            choices.append(questionary.Choice("➡️ Next Page", value="__next__"))
        choices.append(questionary.Choice("❌ Cancel", value="__cancel__"))

        page_num = (offset // step) + 1
        is_last_page = (offset + step) >= total
        header = f"🎬 Select a title to view details or request (Page {page_num}{' (End)' if is_last_page else ''})"
        console.print(f"[dim]Showing {offset+1}–{min(offset+step, total)} of {total}[/dim]")

        selected = questionary.select(
            header,
            choices=choices,
            use_indicator=True,
            use_shortcuts=False
        ).ask()

        if selected == "__next__":
            offset += step
            continue
        elif selected == "__prev__":
            offset = max(0, offset - step)
            continue
        elif selected == "__cancel__" or not selected:
            return None

        console.clear()
        show_metadata_panel(selected)
        media_info = selected.get("mediaInfo", {})
        status = media_info.get("status", 1)
        media_id = media_info.get("jellyfinMediaId") or media_info.get("ratingKey")

        options = []

        label, action_button = get_status_label(selected)

        if status == 5 and media_info.get("mediaUrl"):
            options.append("🌐 Open in Jellyfin/Plex")
        elif status == 2:
            options.append("🔄 Retry Previous Request")
            options.append("🗑️ Delete This Request")
        else:
            options.append(action_button)

        options.append("↩️ Back to Results")
        options.append("❌ Cancel")

        action = questionary.select("What would you like to do?", choices=options).ask()

        if action == "📥 Request This Title" or action == "🔄 Retry Previous Request":
            return selected
        elif action == "🌐 Open in Jellyfin/Plex":
            import webbrowser
            webbrowser.open(media_info["mediaUrl"])
            continue
        elif action == "🗑️ Delete This Request":
            return {"delete": True, "item": selected}
        elif action == "↩️ Back to Results":
            console.clear()
            continue
        else:
            return None


def interactive_home(api):
    while True:
        console.clear()
        choice = questionary.select(
            "📺 Welcome to Peekrr — What would you like to do?",
            choices=[
                "🔍 Search",
                "🌟 Discover",
                "🎬 Movies",
                "📺 Series",
                "📋 Requests",
                "❌ Exit"
            ]).ask()

        if choice == "🔍 Search":
            query = questionary.text("Enter your search query:").ask()
            if query:
                results = api.search(query)
                interactive_select(results)

        elif choice == "🌟 Discover":
            results = api.discover()
            interactive_select(results)

        elif choice == "🎬 Movies":
            results = [r for r in api.discover() if r.get("mediaType") == "movie"]
            interactive_select(results)

        elif choice == "📺 Series":
            results = [r for r in api.discover() if r.get("mediaType") == "tv"]
            interactive_select(results)

        elif choice == "📋 Requests":
            raw_data = api.get_requests()
            raw_requests = raw_data.get("results", [])

            filter_choice = questionary.select(
                "Filter requests by status:",
                choices=[
                    "📋 All",
                    "🔄 Pending",
                    "🛠️ Processing",
                    "📥 Partially Available",
                    "📀 Available",
                    "🛑 Unavailable",
                    "↩️ Back"
                ]).ask()

            if filter_choice == "↩️ Back":
                continue

            status_map = {
                "🔄 Pending": 2,
                "🛠️ Processing": 3,
                "📥 Partially Available": 4,
                "📀 Available": 5,
                "🛑 Unavailable": 1
            }

            status_filter = status_map.get(filter_choice)

            filtered = []
            for r in raw_requests:
                media_info = r.get("media")
                if not media_info:
                    continue
                if status_filter is None or media_info.get("status") == status_filter:
                    filtered.append(media_info)

                for item in filtered:
                    title = item.get("title") or item.get("name") or item.get("externalServiceSlug") or f"TMDB ID: {item.get('tmdbId')}" or "Unknown"
                    item["title"] = title
                    item["mediaType"] = item.get("mediaType", "unknown")

            interactive_select(filtered)


        else:
            break
