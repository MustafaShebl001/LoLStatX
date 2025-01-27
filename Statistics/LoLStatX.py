import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
import os
from prepare_df import get_df
import threading
import pandas as pd
import subprocess
import os
from win_pred import predict_match
import sys
from collect_stats import *
import tkinter as tk
from tkinter import ttk, messagebox,simpledialog
from PIL import Image, ImageTk
import requests
import threading
import pandas as pd
import numpy as np
from pathlib import Path
import tensorflow as tf
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.rcParams['figure.autolayout'] = False

current_dir = Path(__file__).resolve().parent

# Color Palette for GUI
COLORS = {
    'PRIMARY_BG': '#0A1428',
    'SECONDARY_BG': '#F0FFFF',
    'WIN_BG': "#4265ad",  # Blue for Wins
    'LOSS_BG': "#420303",  # Red for Losses
    'NEUTRAL_BG': '#F0AD4E',
    'TEXT': 'gold',
    'SUBTEXT': '#AAB8C2',
    'BUTTON_BG': '#FFD700',
    'BORDER': '#444B6E'
}

RIOT_API = 'RGAPI-a7b63946-2cb5-41c1-a401-dbab2880f38e' # Emafness permenant key
RIOT_API_2 = 'RGAPI-71ef69d2-5c72-4923-880b-06b144968087' # Pelrurnis permenant key
RIOT_API_3 = 'RGAPI-9aa70a29-f594-4c08-bb82-30ed5ae17ea1'   # XAkartuX permenant key
RIOT_API_4 = 'KeyRGAPI-a4e81a85-0fc0-4fbd-8a38-b513a263f5f9'    # Zapunisher5 permenant key



number_of_games = 0
number_of_ranked_games = 0
start_index = 0
df = pd.DataFrame()
stats_df_gui = pd.DataFrame()

 # --- Stats Image ---
image_mapping = {
    'Kills': current_dir / 'stats' / 'kills_image.webp',
    'Deaths':current_dir / 'stats' / 'death_image.webp',
    'Assists': current_dir / 'stats' / 'assists_image.webp',
    'Damage/Min':current_dir / 'stats' / 'dam_min.webp' ,
    'Damage Taken': current_dir / 'stats' / 'damage_taken.webp' ,
    'Damage To Buildings': current_dir / 'stats' / 'damage_to_buildings.webp' ,
    'Damage To Champions': current_dir / 'stats' / 'damage_to_champions.webp' ,
    'Damage To Objectives': current_dir / 'stats' / 'damage_to_objectives.webp' ,
    'First Blood': current_dir / 'stats' / 'first_blood.webp',
    'Kill Participation': current_dir / 'stats' / 'KP.webp' ,
    'Turrets Takedown': current_dir / 'stats' / 'turret_takedowns.webp',
    'Inhibs Takedown': current_dir / 'stats' / 'inhib_takedowns.webp' ,
    'Wards Placed': current_dir / 'stats' / 'total_wards.webp' ,
    'Wards Killed': current_dir / 'stats' / 'wards_killed.webp' ,
    'Vision Score/Min': current_dir / 'stats' / 'vision_score_per_min.webp' ,
    'Dragons Takedown': current_dir / 'stats' / 'dragon_takedowns.webp' ,
    'Barons Takedown': current_dir / 'stats' / 'baron_takedowns.webp',
    'Rift Herald': current_dir / 'stats' / 'rift_herlad.webp' ,
    'Gold/Min': current_dir / 'stats' / 'gold_per_min.webp' ,
    'Jungler CS Before min 10': current_dir / 'stats' / 'jungle_cs_min_10.webp',
    'Healing Allys': current_dir / 'stats' / 'ally_healing.webp' ,
    'Sheilding Allys': current_dir / 'stats' /  'ally_shielding.webp',
        'Total Time CC Dealt': current_dir / 'stats' / 'CC_time.webp',
    'CS': current_dir / 'stats' / 'CS.webp' ,
    'Exp/Min': current_dir / 'stats' / 'exp_per_min.webp' ,
    'Lane CS Before Min 10': current_dir / 'stats' / 'lane_cs_10.webp' ,
    'Max CS Advantage on Lane Opponent': current_dir / 'stats' / 'max_cs_adv.webp' ,
    'Self Healing': current_dir / 'stats' / 'self_healing.webp' ,
    'Self Mitigated Damage': current_dir / 'stats' / 'slef_mitigated_damage.webp' ,
    'Team Damage Percentage': current_dir / 'stats' / 'team_damage_percentage.webp' ,
        'Total Time Spent Dead':    current_dir / 'stats' / 'total_time_spent_dead.webp' ,
    'True Damage To Champions': current_dir / 'stats' / 'true_dmamag_to_champions.webp',
        'Turret Plates Taken': current_dir / 'stats' / 'turret_plates_taken.webp' ,
    'Win Rate'  : current_dir / 'stats' / 'win_rate.webp',
    "Destroy First Turret": current_dir / 'stats' / 'distroy_first_turret.webp',
    "Wards/Min": current_dir / 'stats' / 'wards_per_min.webp',
    "KDA":current_dir / 'stats' / 'KDA.webp',
    'Solo Kills': current_dir / 'stats' / 'solo_kills.webp' ,
    'Number of ScuttleCrabs Killed': current_dir / 'stats' / 'scuttle_crabs.webp'
}


global matches_data, account_puuid, new_region
number_of_games = 0
matches_data = []
df = pd.DataFrame()

def update_progress(value, task):
    """
    Updates the progress bar and label text safely from the main thread.
    """
    loading_progress.config(value=value)
    loading_label.config(text=task)


def long_running_task(n,n_stats_flag ):
    """
    Simulates your data preparation steps with real function-based progress updates.
    """
    global df, number_of_games  # Ensure df is accessible globally
    
    try:
        if len(df) == 0 or n_stats_flag:
            # Step 1: Fetching Match IDs (30%)
            update_progress(20, "Fetching Match IDs...")
            ranked_match_ids = get_ranked_match_ids(
                account_puuid_2,
                new_region,
                RIOT_API_2,
                n
            )

            print(len(ranked_match_ids))

            # Step 2: Collecting Ranked Data (65%)
            update_progress(50, "Collecting Ranked Data...")
            stats_df = collect_ranked_data(
                ranked_match_ids,
                account_puuid_3,
                RIOT_API_3,
                new_region
            )

            # Step 3: Formatting Data (100%)
            update_progress(90, "Formatting Data for Statistics...")
            df = format_to_csv_file(stats_df)
            number_of_games = n
            
            # Notify completion and move to the next screen
            root.after(0, open_statistics_page)
        
    except Exception as e:
        print(f"Error during task execution: {e}")
        root.after(0, lambda: messagebox.showerror("Error", f"Error: Please Try Again"))


def open_statistics_page():
    """
    Once loading is done, clear all widgets and move to the statistics page.
    """
    # Clear all widgets from the root window
    for widget in root.winfo_children():
        widget.destroy()

    # Open the statistics page
    statistics()


def open_statistics_page():
    """
    Once loading is done, clear all widgets and move to the statistics page.
    """
    # Clear all widgets from the root window
    for widget in root.winfo_children():
        widget.destroy()

    # Open the statistics page
    statistics()

def run_in_background(n,n_stats_flag):
    """
    Runs long-running tasks in a separate thread.
    """
    long_running_task(n,n_stats_flag)
    root.after(0, open_statistics_page)
    


def show_loading_screen():
    global loading_frame, loading_label, loading_progress, df

    # Clear any existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Take number of games to calc stats from user
    number_of_stats_games = simpledialog.askinteger("Number Of Games For Query", 
                                        "Please Specify The Number Of Games For Stats:" + f"\nPLAYED RANKED GAMES {number_of_ranked_games} GAMES")

    if number_of_stats_games:
        n_stats = number_of_stats_games
        n_stats_flag = True
        df = pd.DataFrame()
    else:
        n_stats = 100
        n_stats_flag = False

    
    # 1) A single frame that fills the entire root window
    loading_frame = tk.Frame(root, bg=COLORS['PRIMARY_BG'])
    loading_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

    # Ensure root fills the entire window
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # 2) Loading Label (Text)
    loading_label = tk.Label(
        loading_frame,
        text="Computing Your Statistics...",
        font=("Arial", 35, "bold"),
        fg=COLORS['TEXT'],
        bg=COLORS['PRIMARY_BG']
    )
    loading_label.pack(pady=30)

    # 3) Loading Image (Spinner)
    try:
        spinner_img = Image.open(current_dir / 'stats' / 'please_wait.webp').resize((400, 400))
        spinner_tk = ImageTk.PhotoImage(spinner_img)
        spinner_label = tk.Label(loading_frame, image=spinner_tk, bg=COLORS['PRIMARY_BG'])
        spinner_label.image = spinner_tk  # Prevent garbage collection
        spinner_label.pack(pady=30)
    except Exception as e:
        print("Failed to load image:", "Please Try Again")

    # 4) Progress Bar with Custom Style
    style = ttk.Style()
    style.theme_use('default')
    style.configure(
        "Custom.Horizontal.TProgressbar",
        troughcolor="#1e1e2e",  # Bar background
        background="#FFD700",  # Bar fill color (Gold)
        bordercolor="#FFD700",
        thickness=45
    )

    loading_progress = ttk.Progressbar(
        loading_frame,
        style="Custom.Horizontal.TProgressbar",
        orient="horizontal",
        length=400,
        mode="determinate",
        maximum=100,
        value=0
    )
    loading_progress.pack(pady=5)

    # 5) Start the background thread
    thread = threading.Thread(target= lambda: run_in_background(n_stats, n_stats_flag))
    thread.start()



def load_image(folder, filename, size=(40, 40)):
    """Load and resize an image."""
    try:
        image_path = folder / filename
        img = Image.open(image_path)
        img = img.resize(size)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None
    
def display_items(owner_stats, parent, bg_color):
    """
    Display items in a single row on the far right.
    """
    items_frame = tk.Frame(parent, bg=bg_color)
    items_frame.grid(row=0, column=2, rowspan=2, padx=5, sticky="e")  
    
    for i in range(7):
        item_id = owner_stats.get(f'item{i}', 0)
        if item_id:
            item_icon = load_image(current_dir / "item", f"{item_id}.png", (40, 40))
            if item_icon:
                item_label = tk.Label(items_frame, image=item_icon, bg=bg_color)
                item_label.image = item_icon
                item_label.grid(row=0, column=i, padx=2, sticky="e")

def open_other_account_page(player):
    """
    Fetch the clicked player's account data, update global variables,
    and show them in a new 'account_main_page' style.
    """
    global icon_id, level, game_name, tag_line, region
    global rank_soloq, soloq_wins, soloq_losses, soloq_LP
    global account_puuid, specified_region

    try:
        print(player)
        # 1) We have player['puuid'] from the match data
        other_game_name = player['riotIdGameName']
        other_tag_line = player['riotIdTagline']
        other_region = region
        other_puuid = player['puuid']

        sign_in(other_game_name, other_tag_line, other_region)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load {player['summonerName']}'s account: {e}")

    

def display_player_stats(player, parent, team_color, row_index):
    """
    Display player stats, with player name, stats text, and items aligned properly.
    """
    frame = tk.Frame(parent, bg=team_color)
    frame.grid(row=row_index, column=0, columnspan=3, padx=10, pady=2, sticky="ew")

    parent.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=0)  # Champion Icon column
    frame.grid_columnconfigure(1, weight=1)  # Name and Stats column
    frame.grid_columnconfigure(2, weight=0)  # Items column

    # Champion Icon (Column 0)
    print(player['championName'])
    champion_icon = load_image(current_dir / "champion", f"{player['championName']}.png", (50, 50))
    if champion_icon:
        icon_label = tk.Label(frame, image=champion_icon, bg=team_color)
        icon_label.image = champion_icon
        icon_label.grid(row=0, column=0, rowspan=2, padx=5, sticky="w")

    # Player Name (Clickable, Row 0, Column 1)
    summoner_name_label = tk.Label(
        frame,
        text=player["riotIdGameName"] + ' #' + player['riotIdTagline'],
        fg=COLORS['TEXT'],
        bg=team_color,
        font=("Arial", 15, "underline"),
        anchor="w",
        cursor="hand2"
    )
    summoner_name_label.grid(row=0, column=1, padx=5, sticky="w")
    summoner_name_label.bind("<Button-1>", lambda e, p=player: open_other_account_page(p))

    # Stats Text (Row 1, Column 1)
    stats_text = (
        f"KDA: {player['kills']}/{player['deaths']}/{player['assists']} "
        f"({player['challenges'].get('kda', 0):.2f}:1) | "
        f"CS: {player['totalMinionsKilled']} | "
        f"Damage: {player['totalDamageDealtToChampions']:,}"
    )
    stats_label = tk.Label(frame, text=stats_text, fg=COLORS['TEXT'], bg=team_color, font=("Arial", 12), anchor="w")
    stats_label.grid(row=1, column=1, padx=5, sticky="w")

    # Items (Column 2, Row 0)
    display_items(player, frame, team_color)



def launch_stat_gui():
    """Launch the STAT GUI for the selected match."""
    try:
        subprocess.Popen(["python", "C:\\Project\\Statistics\\GUI.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open STAT GUI: Try Again")


def toggle_detailed_stats(match_data, parent, account_puuid, toggle_button):
    """
    Toggle detailed stats for a match and show a 'STAT GUI' button.
    Replaces parent.details_frame.pack(...) usage with .grid(...).
    """
    global stats_df_gui
    if hasattr(parent, "details_frame"):
        # Collapse the expanded stats
        parent.details_frame.destroy()
        delattr(parent, "details_frame")
        toggle_button.config(text="Show More")
    else:
        # Expand detailed stats below the match
        details_frame = tk.Frame(parent, bg=COLORS['PRIMARY_BG'], bd=1, relief="solid")
        # Place it below the match summary in the next available row
        # We'll detect how many children are currently in 'parent'
        # or just place it in a known row offset. For simplicity, 
        # we can do 'row=99' if we want it below or dynamically:
        current_children = parent.grid_slaves()
        # The highest row currently used:
        max_row = 0
        for child in current_children:
            r = child.grid_info().get('row', 0)
            if r > max_row:
                max_row = r
        details_frame.grid(row=max_row+1, column=0, columnspan=4, sticky="ew", pady=2)

        participants = match_data['info']['participants']

        teams = match_data['info']['teams']
        
        # Determine the winning and losing team
        winning_team_id = next((team['teamId'] for team in teams if team['win']), None)
        losing_team_id = 100 if winning_team_id == 200 else 200
        

        # We'll keep track of the row within details_frame
        row_counter = 0

        # Blue Team
        blue_team_label = tk.Label(
            details_frame, text="Blue Team", font=("Arial", 10, "bold"), 
            fg="cyan", bg=COLORS['PRIMARY_BG']
        )
        blue_team_label.grid(row=row_counter, column=0,columnspan=4, sticky="w")
        row_counter += 1

        for player in participants:
            if player['teamId'] == 100:
                display_player_stats(player, details_frame, "#14213D", row_counter)
                row_counter += 1

        # Red Team
        red_team_label = tk.Label(
            details_frame, text="Red Team", font=("Arial", 10, "bold"), 
            fg="red", bg=COLORS['PRIMARY_BG']
        )
        red_team_label.grid(row=row_counter, column=0,columnspan=4, sticky="news")
        row_counter += 1

        for player in participants:
            if player['teamId'] == 200:
                display_player_stats(player, details_frame, "#6A040F", row_counter)
                row_counter += 1

        stats_df_gui = get_df(match_data)

        # STAT GUI Button
        stat_button = tk.Button(
            details_frame, text="STAT GUI", font=("Arial", 12, "bold"), 
            bg=COLORS['TEXT'], fg="black", command=lambda: launch_stat_gui()
        )
        stat_button.grid(row=row_counter, column=0, pady=10, sticky="news")

        parent.details_frame = details_frame
        toggle_button.config(text="Show Less")


def display_match_summary(match_data, parent, idx, account_puuid):
    """
    Display match summary with victory/defeat colors using grid instead of pack.
    """
    participants = match_data['info']['participants']
    owner_stats = next(player for player in participants if player['puuid'] == account_puuid)

    # Background color based on win/loss
    match_result = "Victory" if owner_stats['win'] else "Defeat"
    bg_color = COLORS['WIN_BG'] if owner_stats['win'] else COLORS['LOSS_BG']  # Blue for win, red for loss
    # bg_color = "#0096FF" if owner_stats['win'] else "#420303"  # Blue for win, red for loss

    # Ensure parent column expands to fill available space
    parent.columnconfigure(0, weight=1)

    # Match Frame (one row per match)
    frame = tk.Frame(parent, bg=bg_color, pady=15)
    frame.grid(row=idx + 1, column=0, padx=10, sticky="ew")  # "ew" expands horizontally

    # Ensure the frame expands fully
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=3)  # Stats text gets more space
    frame.columnconfigure(2, weight=2)  # Items section
    frame.columnconfigure(3, weight=1)  # Show More button

    # Champion Icon
    champion_icon = load_image(current_dir / "champion", f"{owner_stats['championName']}.png", (70, 70))
    if champion_icon:
        icon_label = tk.Label(frame, image=champion_icon, bg=bg_color)
        icon_label.image = champion_icon
        icon_label.grid(row=0, column=0, padx=5, sticky="w")

    # Basic Stats
    summary_text = (
        f"KDA: {owner_stats['kills']}/{owner_stats['deaths']}/{owner_stats['assists']} | "
        f"CS: {owner_stats['totalMinionsKilled']} | "
        f"Result: {match_result}"
    )
    summary_label = tk.Label(
        frame, text=summary_text, font=("Arial", 15, 'bold'), fg=COLORS['TEXT'], bg=bg_color, anchor="w", pady=10
    )
    summary_label.grid(row=0, column=1, padx=50, sticky="w")

    # Items Section
    items_frame = tk.Frame(frame, bg=bg_color)
    items_frame.grid(row=0, column=2, padx=5, sticky="w")
    for i in range(7):
        item_id = owner_stats.get(f'item{i}', 0)
        if item_id:
            item_icon = load_image(current_dir / "item", f"{item_id}.png", (50, 50))
            if item_icon:
                item_label = tk.Label(items_frame, image=item_icon, bg=bg_color)
                item_label.image = item_icon
                item_label.grid(row=0, column=i, padx=2, sticky="e")

    # "Show More" Button
    show_more_button = tk.Button(
        frame, text="Show More", font=("Arial", 12, 'bold'), bg=COLORS['TEXT'], fg="black", padx=20,
        command=lambda: toggle_detailed_stats(match_data, frame, account_puuid, show_more_button)
    )
    show_more_button.grid(row=0, column=3, padx=5, sticky="e")


loading_screen_flag = False
def load_more_games():
    global loading_screen_flag
    loading_screen_flag = True
    matches_loading_screen()
    

    
def show_all_matches(matches_data, account_puuid):
    """
    Display account info at the top and match summaries below,
    but without a visible Scrollbar widget. 
    The user can scroll vertically using the mouse wheel, 
    and the matches area expands to fill the full width of the window.
    """
    global icon_id, level, game_name, tag_line, region
    global rank_soloq, soloq_wins, soloq_losses, soloq_LP

    # Clear the root window
    for widget in root.winfo_children():
        widget.destroy()

    # Configure background and layout
    root.configure(bg=COLORS['PRIMARY_BG'])

    # Let rows and columns expand
    root.grid_rowconfigure(0, weight=0)  # Title row doesn't need to expand
    root.grid_rowconfigure(1, weight=0)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=0)
    root.grid_rowconfigure(4, weight=0)
    root.grid_rowconfigure(5, weight=0)
    root.grid_rowconfigure(6, weight=0)
    root.grid_rowconfigure(7, weight=1)  # The matches area row
    root.grid_columnconfigure(0, weight=1)  # Let column 0 expand
    # If using columns 1, 2, etc., you can set weight=1 for them as well

    #
    # 1. Display Account Info (same as before)
    #
    # Load images
    image_path = current_dir / 'profileicon' / f"{icon_id}.png"
    image = Image.open(image_path).resize((125, 125))
    root.profile_icon = ImageTk.PhotoImage(image)

    tier = rank_soloq.split()[0].upper()
    rank_image_path = current_dir / 'rank' / f'{tier}.webp'
    rank_image = Image.open(rank_image_path).resize((150, 150))
    root.rank_icon = ImageTk.PhotoImage(rank_image)

    # Title
    label_title = tk.Label(
        root, 
        text="LEAGUE OF LEGENDS", 
        font=("Arial", 20, "bold"),
        fg=COLORS['TEXT'], 
        bg=COLORS['PRIMARY_BG']
    )
    label_title.grid(row=0, column=0, columnspan=3, pady=20, sticky="nsew")

    # Profile icon (left)
    icon_label = tk.Label(root, image=root.profile_icon, bg=COLORS['PRIMARY_BG'])
    icon_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    # Rank icon (right)
    rank_icon_label = tk.Label(root, image=root.rank_icon, bg=COLORS['PRIMARY_BG'])
    rank_icon_label.grid(row=1, column=2, padx=30, pady=5, sticky="e")

    # Summoner info (middle-ish)
    tk.Label(root, text='Account: ' + game_name + '  ' + tag_line, 
            font=("Arial", 15, 'bold'), fg=COLORS['TEXT'], bg=COLORS['PRIMARY_BG']).grid(
        row=2, column=0, columnspan=3, padx=5, pady=10, sticky="w"
    )
    tk.Label(root, text=rank_soloq, font=("Arial", 15, 'bold'), fg=COLORS['TEXT'], bg=COLORS['PRIMARY_BG']).grid(
        row=2, column=2, padx=30, pady=5, sticky="e"
    )
    tk.Label(root, text=f'{soloq_LP} LP', font=("Arial", 15, 'bold'), fg=COLORS['TEXT'], bg=COLORS['PRIMARY_BG']).grid(
        row=3, column=2, padx=30, pady=5, sticky="e"
    )
    tk.Label(root, text=f'Wins: {soloq_wins}  //  Losses: {soloq_losses}', 
            font=("Arial", 15, 'bold'), fg=COLORS['TEXT'], bg=COLORS['PRIMARY_BG']).grid(
        row=4, column=2, padx=30, pady=5, sticky="e"
    )
    tk.Label(root, text=f'Win Rate: {"--" if soloq_losses == 0 and soloq_wins == 0 else str(round(soloq_wins/(soloq_losses+soloq_wins)*100,1))+" %"}', 
            font=("Arial", 15, 'bold'), fg=COLORS['TEXT'], bg=COLORS['PRIMARY_BG']).grid(
        row=5, column=2, padx=30, pady=5, sticky="e"
    )
    tk.Label(root, text='Region: ' + region, 
            font=("Arial", 15, 'bold'), fg=COLORS['TEXT'], bg=COLORS['PRIMARY_BG']).grid(
        row=3, column=0, columnspan=3, padx=10, pady=5, sticky="w"
    )
    tk.Label(root, text='Level: ' + str(level), 
            font=("Arial", 15,'bold'), fg=COLORS['TEXT'], bg=COLORS['PRIMARY_BG']).grid(
        row=4, column=0, columnspan=3, padx=10, pady=5, sticky="w"
    )


    #
    # 2. "Recent Matches" label
    #
    header_label = tk.Label(
        root, 
        text="Recent Matches", 
        font=("Arial", 22, "bold"), 
        fg=COLORS['TEXT'], 
        bg=COLORS['PRIMARY_BG']
    )
    header_label.grid(row=6, column=0, columnspan=3, pady=10, sticky="nsew")

    #
    # 3. Create a scrollable container for the matches (using a Canvas),
    #    but WITHOUT a visible scrollbar widget.
    #
    scroll_container = tk.Frame(root, bg=COLORS['PRIMARY_BG'])
    scroll_container.grid(row=7, column=0, columnspan=3, sticky="nsew")

    # Inside this container, place a Canvas
    canvas = tk.Canvas(scroll_container, bg=COLORS['PRIMARY_BG'], highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    matches_frame = tk.Frame(canvas, bg=COLORS['PRIMARY_BG'])
    matches_window = canvas.create_window((0, 0), window=matches_frame, anchor="nw")

    load_more = tk.Button(root, text='Load More', command= load_more_games, font=('Arial', 15, 'bold'), bg=COLORS['TEXT'], fg="black")
    load_more.grid(row=8,column=0, columnspan=3,sticky='news')

    # Ensure the matches_frame width matches the canvas width dynamically
    def on_canvas_resize(event):
        """
        Adjust matches_frame width dynamically when the Canvas is resized.
        """
        canvas.itemconfig(matches_window, width=event.width)

    # Bind the canvas resize event
    canvas.bind("<Configure>", on_canvas_resize)

    # Update scroll region whenever matches_frame changes size
    def on_frame_configure(event):
        """
        Update the scroll region of the Canvas whenever the content changes.
        """
        canvas.configure(scrollregion=canvas.bbox("all"))

    matches_frame.bind("<Configure>", on_frame_configure)

    matches_frame.grid_columnconfigure(0, weight=1)

    # Mouse wheel scrolling
    def _on_mouse_wheel(event):
        """
        Enable mouse wheel scrolling on the Canvas.
        """
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

    back_button = tk.Button(
        root, text="Back", font=("Arial", 14, 'bold'), bg=COLORS['TEXT'], fg="black", padx=20, pady=5,
        command= account_main_page
    )
    back_button.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

    # 4. Display all match summaries INSIDE matches_frame
    #
    for idx, match_data in enumerate(matches_data):
        display_match_summary(match_data, matches_frame, idx, account_puuid)




def pre_fetch_matches(account_puuid, new_region):
    """
    Fetch match IDs and their data (CLASSIC only).
    """
    global start_index
    try:

        if len(matches_data) > 0 and not loading_screen_flag:
            return matches_data
        else:
            match_ids = requests.get(
                f'https://{new_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{account_puuid}/ids?start={start_index}&count=20&api_key={RIOT_API}'
            ).json()

            for match_id in match_ids:
                match_data = requests.get(
                    f'https://{new_region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_API}'
                ).json()
                # if match_data['info']['gameMode'] == 'CLASSIC':
                matches_data.append(match_data)

            return matches_data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch matches: Try Again")

    

def fetch_recent_matches(matches_data, account_puuid):
    """
    Run show_all_matches on the main thread but gather data in background if needed.
    Here we already have matches_data, so we just show them.
    """
    def fetch_in_thread():
        try:
            root.after(0, lambda: show_all_matches(matches_data, account_puuid))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch matches: Try Again"))

    thread = threading.Thread(target=fetch_in_thread)
    thread.start()

def combine_unique_matches(list1, list2):
    """
    Combine two lists of dictionaries, ensuring no duplicate 'matchId' in 'metadata'.
    
    Parameters:
        list1 (list): First list of dictionaries.
        list2 (list): Second list of dictionaries.
        
    Returns:
        list: Combined list without duplicate 'matchId'.
    """
    unique_matches = {}
    
    # Process the first list
    for d in list1:
        match_id = d.get('metadata', {}).get('matchId')
        if match_id is not None:
            unique_matches[match_id] = d
    
    # Process the second list (overwrite duplicates)
    for d in list2:
        match_id = d.get('metadata', {}).get('matchId')
        if match_id is not None and match_id not in unique_matches:
            unique_matches[match_id] = d
    
    # Return the unique dictionaries as a list
    return list(unique_matches.values())


def matches_loading_screen():
    """
    Show a loading screen while fetching matches.
    """
    global account_puuid, new_region, loading_screen_flag
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg=COLORS['PRIMARY_BG'])

    tk.Label(root, text="Loading Matches...", font=("Arial", 25, "bold"), fg=COLORS['TEXT'], bg="black", pady=50).grid(
        row=1, column=0, columnspan=3, pady=350, sticky="nsew"
    )
    tk.Button(root, text='Back', command= account_main_page, font=('Arial', 15, 'bold'), bg=COLORS['TEXT'], fg="black").grid(
        row=0, column=0, pady=10, sticky="wn")
    import json
    def fetch_matches():
        global matches_data, start_index
        if len(matches_data) != 0:
            if loading_screen_flag:
                start_index += 20
            matches_data_2 = pre_fetch_matches(account_puuid, new_region)
            # combined = matches_data + matches_data_2
            # print(type(combined))
            matches_data = combine_unique_matches(matches_data, matches_data_2)
        else:
            start_index = 0
            matches_data = pre_fetch_matches(account_puuid, new_region)

        # print(len(matches_data))

        root.after(0, lambda: fetch_recent_matches(matches_data, account_puuid))

    # Fetch matches in the background
    thread = threading.Thread(target=fetch_matches)
    thread.start()

def account_main_page():
    """
    Display account information with Profile Icon on the left,
    Rank Icon along with Wins | Losses and Win Rate on the right,
    a fully expanded button section below, and 'League of Legends' at the top center.
    """
    global icon_id, level, game_name, tag_line, region, loading_screen_flag
    global rank_soloq, soloq_wins, soloq_losses, soloq_LP
    global account_puuid

    # Clear window and configure the layout
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg=COLORS['PRIMARY_BG'])

    loading_screen_flag = False

    # === Grid Configuration ===
    root.grid_columnconfigure(0, weight=1)  # Left (Profile Section)
    root.grid_columnconfigure(1, weight=0)  # Spacer column
    root.grid_columnconfigure(2, weight=1)  # Right (Rank Section)
    root.grid_rowconfigure(2, weight=1)     # Allow bottom row to expand

    # === Top Title (League of Legends) ===
    title_label = tk.Label(
        root,
        text="League of Legends",
        font=("Arial", 24, "bold"),
        fg=COLORS['TEXT'],
        bg=COLORS['PRIMARY_BG']
    )
    title_label.grid(row=0, column=0, columnspan=3, pady=20, sticky="n")

    # === Profile Section (Left Side) ===
    profile_frame = tk.Frame(root, bg=COLORS['PRIMARY_BG'])
    profile_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nw")

    # Load and display profile icon
    image_path = current_dir / 'profileicon' / f"{icon_id}.png"
    image = Image.open(image_path).resize((150, 150))
    root.profile_icon = ImageTk.PhotoImage(image)

    icon_label = tk.Label(profile_frame, image=root.profile_icon, bg=COLORS['PRIMARY_BG'])
    icon_label.pack(pady=10)

    # tk.Label(profile_frame, text='Profile Icon', font=("Arial", 12), fg=COLORS['TEXT'], bg=COLORS['PRIMARY_BG']).pack()

    # Display Account Details under Profile
    details_frame = tk.Frame(profile_frame, bg=COLORS['PRIMARY_BG'])
    details_frame.pack(pady=10)

    details = [
        f'Account: {game_name}  #{tag_line}',
        f'Region: {region}',
        f'Level: {level}'
    ]

    for detail in details:
        tk.Label(
            details_frame, text=detail.title(), font=("Arial", 16,'bold'), fg=COLORS['TEXT'], 
            bg=COLORS['PRIMARY_BG'], anchor="w"
        ).pack(anchor="w")


    # === Button Section (Full Width) ===
    button_frame = tk.Frame(root, bg=COLORS['PRIMARY_BG'])
    button_frame.grid(row=2, column=0, columnspan=3, pady=30, sticky="ew")

    # Configure button_frame to stretch horizontally
    button_frame.grid_columnconfigure(0, weight=1)

    # Add Buttons
    tk.Button(
        button_frame, text="Match History", font=("Arial", 15, 'bold'), bg=COLORS['TEXT'], 
        fg="black", pady=10, command=matches_loading_screen
    ).grid(row=0, column=0, padx=10, pady=5, sticky="news")

    tk.Button(
        button_frame, text="Predict Win Probability (Live Match)", font=("Arial", 15, 'bold'), 
        bg=COLORS['TEXT'], fg="black", pady=10, command=win_pred_model
    ).grid(row=2, column=0, padx=10, pady=5, sticky="news")

    # Statitsics button
    tk.Button(button_frame, text="MY STAT", font=("Arial", 15, 'bold'), bg=COLORS['TEXT'], 
        fg="black", pady=10, command=show_loading_screen
    ).grid(row=1, column=0, padx=10, pady=5, sticky="news")


    tk.Button(
        button_frame, text="Sign Out", font=("Arial", 15, 'bold'), bg=COLORS['TEXT'], fg="black", 
        pady=10, command= create_sign_in_page
    ).grid(row=4, column=0, padx=10, pady=60, sticky="news")


def statistics():
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg=COLORS['PRIMARY_BG'])

    root.state('zoomed')  # Windows-specific maximization

    title_label = tk.Label(
    root,
    text=f"Statistical Data Overview For {int(number_of_games)} Games",
    font=("Arial", 24, "bold"),
    fg=COLORS['TEXT'],
    bg=COLORS['PRIMARY_BG']
    )
    title_label.pack(pady=10)

    # ---------------------------------------------------------------------
    #  MAIN CONTAINER: Holds Left Menu (scrollable) + Right Stats (scrollable)
    # ---------------------------------------------------------------------
    main_container = tk.Frame(root, bg=COLORS['PRIMARY_BG'])
    main_container.pack(fill="both", expand=True)

    ####################################
    # LEFT SIDE: Scrollable Menu
    ####################################
    left_menu_container = tk.Frame(main_container, bg=COLORS['PRIMARY_BG'], width=400)
    left_menu_container.pack(side="left", fill="y", padx=10, pady=10)
    left_menu_container.pack_propagate(False)  # Keep the set width

    # Canvas for the left menu
    menu_canvas = tk.Canvas(left_menu_container, bg=COLORS['PRIMARY_BG'], highlightthickness=0)
    menu_canvas.pack(side="left", fill="both", expand=True)

    # Scrollbar for the left menu
    # menu_scrollbar = ttk.Scrollbar(left_menu_container, orient="vertical", command=menu_canvas.yview)
    # menu_scrollbar.pack(side="right", fill="y")

    # menu_canvas.configure(yscrollcommand=menu_scrollbar.set)

    # Frame inside the canvas for the menu items
    menu_frame = tk.Frame(menu_canvas, bg=COLORS['PRIMARY_BG'])
    menu_canvas.create_window((0, 0), window=menu_frame, anchor="nw")

    # ---------------------------------------------------------------------
    #  Mouse Wheel Scrolling for the LEFT MENU
    # ---------------------------------------------------------------------
    def on_left_menu_mousewheel(event):
        """
        Scroll the left menu Canvas (menu_canvas).
        event.delta is typically 120 or -120 on Windows.
        """
        menu_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Bind mouse wheel *only while mouse is over menu_canvas*
    menu_canvas.bind("<Enter>", lambda e: menu_canvas.bind_all("<MouseWheel>", on_left_menu_mousewheel))
    menu_canvas.bind("<Leave>", lambda e: menu_canvas.unbind_all("<MouseWheel>"))

    def on_menu_frame_configure(event):
        """
        Update the scrollregion whenever the menu_frame changes size.
        """
        menu_canvas.configure(scrollregion=menu_canvas.bbox("all"))

    menu_frame.bind("<Configure>", on_menu_frame_configure)

    ####################################
    # RIGHT SIDE: Scrollable Stats
    ####################################
    right_frame = tk.Frame(main_container, bg="#1b263b")
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    stats_canvas = tk.Canvas(right_frame, bg="#1b263b", highlightthickness=0)
    stats_canvas.pack(side="left", fill="both", expand=True)

    stats_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=stats_canvas.yview)
    stats_scrollbar.pack(side="right", fill="y")
    stats_canvas.configure(yscrollcommand=stats_scrollbar.set)

    stats_frame = tk.Frame(stats_canvas, bg="#1b263b")
    stats_canvas.create_window((0, 0), window=stats_frame, anchor="nw")

    # ---------------------------------------------------------------------
    #  Mouse Wheel Scrolling for the RIGHT STATS
    # ---------------------------------------------------------------------
    def on_right_stats_mousewheel(event):
        """
        Scroll the right stats Canvas (stats_canvas).
        """
        stats_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Bind mouse wheel *only while mouse is over stats_canvas*
    stats_canvas.bind("<Enter>", lambda e: stats_canvas.bind_all("<MouseWheel>", on_right_stats_mousewheel))
    stats_canvas.bind("<Leave>", lambda e: stats_canvas.unbind_all("<MouseWheel>"))

    def on_stats_frame_configure(event):
        stats_canvas.configure(scrollregion=stats_canvas.bbox("all"))

    stats_frame.bind("<Configure>", on_stats_frame_configure)

    # A dictionary to map stat_name -> the row's frame (for scrolling to it)
    row_frames_dict = {}

    def display_stat_row(stat_name, stat_value, image_path:Path):
        """
        Create a row in the scrollable stats_frame (right side).
        """
        row_frame = tk.Frame(stats_frame, bg="#1b263b", pady=10)
        row_frame.pack(fill="x", padx=5, pady=5)
        row_frames_dict[stat_name] = row_frame

        # --- Icon/Image ---
        image_frame = tk.Frame(row_frame, bg="#1b263b")
        image_frame.pack(side="left", padx=10)

        if image_path.exists():
            img = Image.open(image_path).resize((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            image_label = tk.Label(image_frame, image=img_tk, bg="#1b263b")
            image_label.image = img_tk  # keep ref
            image_label.pack()
        else:
            tk.Label(
                image_frame,
                text="No Image",
                font=("Arial", 12),
                fg="gray",
                bg="#1b263b"
            ).pack()

        # --- Stat Name ---
        tk.Label(
            row_frame,
            text=stat_name,
            font=("Arial", 15, "bold"),
            fg=COLORS['TEXT'],
            bg="#1b263b",
            anchor="w"
        ).pack(side="left", padx=30)

        # --- Stat Value ---
        tk.Label(
            row_frame,
            text=str(stat_value),
            font=("Arial", 14, 'bold'),
            fg=COLORS['TEXT'],
            bg="#1b263b",
            anchor="e"
        ).pack(side="right", padx=30)

    def scroll_to_stat(stat_name):
        """
        Scroll the right stats area so that the row for stat_name is visible.
        """
        stats_frame.update_idletasks()  # ensure sizes are updated
        row_frame = row_frames_dict.get(stat_name)
        if not row_frame:
            return

        y_coord = row_frame.winfo_y()          # top of that row, relative to stats_frame
        total_height = stats_frame.winfo_height()

        if total_height == 0:
            return

        ratio = y_coord / total_height
        stats_canvas.yview_moveto(ratio)

    # ---------------------------------------------------------------------
    #  CREATE THE LEFT MENU LABELS (clickable)
    # ---------------------------------------------------------------------
    def create_left_menu():
        """
        Populate menu_frame with labels for each stat name.
        Clicking a label scrolls the right side to that stat.
        """
        # Clear existing children
        for widget in menu_frame.winfo_children():
            widget.destroy()

        for _, row in df.iterrows():
            stat_name = str(row.iloc[0])  # 1st column in CSV
            label = tk.Label(
                menu_frame,
                text=stat_name,
                font=("Arial", 16, "bold"),
                bg=COLORS['PRIMARY_BG'],
                fg=COLORS['TEXT'],
                cursor="hand2",
                anchor="w",
                pady=2
            )
            label.pack(fill="x", padx=5, pady=2)
            label.bind("<Button-1>", lambda e, sn=stat_name: scroll_to_stat(sn))

    # ---------------------------------------------------------------------
    #  LOAD THE STATS INTO RIGHT SCROLLABLE AREA
    # ---------------------------------------------------------------------
    def load_stats():
        """
        Populate stats_frame with each stat row from df.
        """
        for widget in stats_frame.winfo_children():
            widget.destroy()
        row_frames_dict.clear()

        for _, row in df.iterrows():
            stat_name = str(row.iloc[0])
            stat_value = row.iloc[1]
            image_path = image_mapping.get(stat_name, "")
            display_stat_row(stat_name, stat_value, image_path)

    # --- BOTTOM NAVIGATION (optional) ---
    nav_frame = tk.Frame(root, bg=COLORS['PRIMARY_BG'])
    nav_frame.pack(pady=10)

    tk.Button(
        nav_frame,
        text="Back",
        command=account_main_page,
        font=("Arial", 15, "bold"),
        bg=COLORS['TEXT'],
        fg="black"
    ).pack(side="left", padx=10)

    tk.Button(
        nav_frame,
        text="Refresh",
        command=lambda: [load_stats(), create_left_menu()],
        font=("Arial", 15, "bold"),
        bg=COLORS['TEXT'],
        fg="black"
    ).pack(side="right", padx=10)

    # --- Initialize UI ---
    create_left_menu()
    load_stats()
    

def win_pred_model():
    """
    Run the win prediction model.
    """
    
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg=COLORS['PRIMARY_BG'])

    try:
        result, user_team = predict_match()
        # print(f"Prediction result: {result}")  # Debugging line

        flag = False

        if user_team == 'BLUE':
            real_result = result
            flag = True
        elif user_team == 'RED':
            real_result = 1 - result
            flag = True
        else:
            flag = False
        
        

        # Ensure the result is displayed correctly
        # messagebox.showinfo("Prediction Result", f'Your Current Win prob. is {result}')

        if flag:
            tk.Label(root, text=f"You Current Match Win Probability is: {real_result}", font=("Arial", 25, "bold"), fg=COLORS['TEXT'], bg="black", pady=30).grid(
                row=0, column=0, columnspan= 3,pady=350, sticky="nsew"
            )
        else:
            tk.Label(root, text=f"You Are Not Online, No Live Game", font=("Arial", 25, "bold"), fg=COLORS['TEXT'], bg="black", pady=30).grid(
                row=0, column=0, columnspan= 3,pady=350, sticky="nsew"
            )
            # messagebox.showinfo("No Match", f"There is no current live match")



        tk.Button(
            root, text="Back", font=("Arial", 15, 'bold'), bg=COLORS['TEXT'], fg="black", padx=15 , command=account_main_page
        ).grid(row=1, column=0, columnspan=2, pady=10, sticky="sw")

        tk.Button(
            root, text="Retry", font=("Arial", 15, 'bold'), bg=COLORS['TEXT'], fg="black", padx=15 , command=win_pred_model
        ).grid(row=1, column=0, columnspan=2, pady=10, sticky="se")


    except Exception as e:
        # print(f"Error: {e}")  # Debugging line
        messagebox.showerror("Error", f"Failed to open win prediction model: Try Again")


def sign_in(game_name_2,tag_line_2,region_2):
    """
    Sign in and fetch match info, then proceed to the account main page.
    """
    global icon_id, level, loading_screen_flag, matches_data
    global rank_soloq, soloq_wins, soloq_losses, soloq_LP
    global new_region, account_puuid, account_puuid_2, account_puuid_3, specified_region
    global game_name, tag_line, region, number_of_ranked_games
    

    game_name = game_name_2
    tag_line = tag_line_2
    region = region_2

    # Reset the flag with every new player
    matches_data = []
    
    # Map region to API-friendly format
    region_map = {
        "EUW": "europe",
        "NA": "americas",
        "KR": "asia"
    }
    new_region = region_map.get(region, "")

    specified_region = region_map = {
        "EUW": "euw1",
        "NA": "na1",
        "KR": "kr"
    }

    specified_region = specified_region.get(region, "")


    if not new_region:
        messagebox.showerror("Error", "Please select a region")
        return

    if game_name and tag_line:
        try:
            response = requests.get(
                f'https://{new_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={RIOT_API}'
            ).json()
            account_puuid = response['puuid']

            response_2 = requests.get(
                f'https://{new_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={RIOT_API_2}'
            ).json()
            account_puuid_2 = response_2['puuid']

            response_3 = requests.get(
                f'https://{new_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={RIOT_API_3}'
            ).json()
            account_puuid_3 = response_3['puuid']

            summoner = requests.get(
                f'https://{specified_region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/' 
                + account_puuid + '?api_key=' + RIOT_API
            ).json()

            rank = requests.get(
                f'https://{specified_region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner["id"]}?api_key={RIOT_API}'
            ).json()

            icon_id = summoner['profileIconId']
            level = summoner['summonerLevel']

            # If the user is in multiple queues, pick the SoloQ
            

            if len(rank) == 2:
                for num in range(len(rank)):
                    if rank[num]['queueType'] == 'RANKED_SOLO_5x5':
                        rank_soloq = rank[num]['tier'] + ' ' + rank[1]['rank']
                        soloq_wins = rank[num]['wins']
                        soloq_losses = rank[num]['losses']
                        soloq_LP = rank[num]['leaguePoints']
                # We won't use rank_flex if it's not needed, but keep for reference
                # rank_flex = rank[1]['tier'] + ' ' + rank[1]['rank']
            elif len(rank) == 1:
                rank_soloq = rank[0]['tier'] + ' ' + rank[0]['rank']
                soloq_wins = rank[0]['wins']
                soloq_losses = rank[0]['losses']
                soloq_LP = rank[0]['leaguePoints']
                # rank_flex = 'Unranked'
            else:
                rank_soloq = 'Unranked'
                soloq_wins = 0
                soloq_losses = 0

                soloq_LP = 0

            number_of_ranked_games = soloq_wins + soloq_losses


            # Fetch matches data in one go
            # matches_data = pre_fetch_matches(account_puuid, new_region)

            # Clear current page and show the main page
            for widget in root.winfo_children():
                widget.destroy()

            account_main_page()
            # fetch_recent_matches(matches_data, account_puuid)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Error", "Please enter all details and select a region")




def create_sign_in_page():
    """
    Create the sign-in page with pack().
    """
    for widget in root.winfo_children():
        widget.destroy()

    global username_entry, password_entry, region_var
    root.configure(bg=COLORS['PRIMARY_BG'])

    # Create a frame for the title and pack it at the top
    title_frame = tk.Frame(root, bg=COLORS['PRIMARY_BG'])
    title_frame.pack(side="top", fill="x")

    tk.Label(
        title_frame, text="LoLStatx", font=("Arial", 30, "bold"), fg=COLORS['TEXT'], bg=COLORS['PRIMARY_BG']
    ).pack(pady=20)

    tk.Label(
        title_frame, text="LEAGUE OF LEGENDS", font=("Arial", 20, "bold"), fg=COLORS['TEXT'], bg=COLORS['PRIMARY_BG']
    ).pack(pady=20)

    # Create a frame to hold all the widgets and center it
    frame = tk.Frame(root, bg=COLORS['PRIMARY_BG'])
    frame.pack(expand=True)

    tk.Label(frame, text="Game Name", font=("Arial", 15, 'bold'), fg=COLORS['TEXT'], bg=COLORS['PRIMARY_BG']).pack(pady=10, anchor="w")
    username_entry = tk.Entry(frame, font=("Arial", 15, 'bold'), width=20)
    username_entry.pack(pady=10, ipady=10)

    tk.Label(frame, text="Tag Line", font=("Arial", 15, 'bold'), fg=COLORS['TEXT'], bg=COLORS['PRIMARY_BG']).pack(pady=10, anchor="w")
    tagline_entry = tk.Entry(frame, font=("Arial", 15, 'bold'), width=20)
    tagline_entry.pack(pady=10, ipady=10)

    tk.Label(frame, text="Region", font=("Arial", 15, 'bold'), fg=COLORS['TEXT'], bg=COLORS['PRIMARY_BG']).pack(pady=10, anchor="w")
    region_var = tk.StringVar(value="Select Region")
    region_menu = ttk.Combobox(frame, textvariable=region_var, font=("Arial", 15, 'bold'), state="readonly")
    region_menu['values'] = ["EUW", "NA", "KR"]
    region_menu.pack(pady=10, ipady=10)

    tk.Button(frame, text="Sign In", font=("Arial", 15, 'bold'), bg=COLORS['TEXT'], fg="black", padx=40, pady=15, command=lambda: sign_in(username_entry.get(),tagline_entry.get(),region_var.get())).pack(pady=20)

    # Make the frame expand to fill the root window
    frame.pack(expand=True)

# Main Window
root = tk.Tk()
root.title("LoLStatx - League of Legends")

# Set window icon
icon_path = current_dir / "LoLStatx.webp"

# Load icon using PIL
if icon_path.exists():
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(True, icon_photo)  # Set icon (cross-platform support)
else:
    print("Icon file not found. Please check the path!")


root.geometry("800x700")

create_sign_in_page()
root.mainloop()
