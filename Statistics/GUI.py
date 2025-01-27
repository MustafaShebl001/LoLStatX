import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
import sys

matplotlib.rcParams['figure.autolayout'] = False

# Load CSV


def statistics_graphs(df):
    # Your helper functions and logic remain unchanged here

    def show_statistics_page():
        stats_frame.pack(fill=tk.BOTH, expand=True)

        fig, panels = plt.subplots(2, 3, figsize=(30, 18), dpi=120, constrained_layout=True)
        fig.patch.set_facecolor(BACKGROUND_COLOR)

        # Metrics to display
        draw_metric(panels[0, 0], "Kills", blue_team, red_team, "Kills", fontsize=9)
        draw_metric(panels[0, 1], "Gold earned", blue_team, red_team, "Total Gold Earned", fontsize=9)
        draw_metric(panels[0, 2], "Damage dealt to champions", blue_team, red_team, 
                    "Total Damage dealt to Champions", fontsize=9)
        draw_metric(panels[1, 0], "Wards placed", blue_team, red_team, "Wards Placed", fontsize=9)
        draw_metric(panels[1, 1], "Damage taken", blue_team, red_team, "Total Damage taken", fontsize=9)
        draw_metric(panels[1, 2], "CS", blue_team, red_team, "CS", fontsize=9)

        # Add the canvas
        canvas = FigureCanvasTkAgg(fig, master=stats_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
    
    # Split data
    blue_team = df[:5].reset_index(drop=True)
    red_team  = df[5:].reset_index(drop=True)

    # Sort teams based on role order
    role_order = ['UTILITY', 'BOTTOM','MIDDLE','JUNGLE','TOP']
    blue_team = blue_team.set_index("Role").loc[role_order].reset_index()
    red_team = red_team.set_index("Role").loc[role_order].reset_index()


    COLOR_BLUE = "#4D79FF"
    COLOR_RED  = "#FF4D4D"
    BACKGROUND_COLOR = "#2E2E2E"

    def annotate_barh(ax, bars, values, total_bar_length=0.8, fontsize=8):
        """
        Annotate numeric labels inside the right edge of the full bar length.
        - bars: The filled bars.
        - values: The actual values to display.
        - total_bar_length: The total length of the bar (e.g., 0.8 for reduced length).
        """
        for bar, value in zip(bars, values):
            # Calculate the vertical center of the bar
            y_center = bar.get_y() + bar.get_height() / 2  

            # Position text at the right edge of the total bar length
            x_pos = total_bar_length - 0.02  # Slight inward shift for neatness

            # Display the actual numeric value passed in 'values'
            label_text = f"{value:,}"  

            ax.text(
                x_pos, y_center,       # Coordinates
                label_text,            # Actual numeric value
                va='center', ha='right',  # Align text to the right edge
                color='white', fontsize=fontsize
            )




    def create_donut_chart(ax, total_blue, total_red, fontsize=8):
        """
        Donut chart with two numbers in the center hole separated by a thin line.
        Adjust 'radius' and 'width' to make the donut ring thinner and bigger overall.
        """
        sizes = [total_blue, total_red]
        colors = [COLOR_BLUE, COLOR_RED]

        # Make the donut larger and the ring thinner.
        #   radius=1.2  => overall circle size
        #   width=0.3   => thickness of the ring (so hole radius = 1.2 - 0.3 = 0.9)
        wedges, _ = ax.pie(
            sizes,
            colors=colors,
            startangle=140,
            labels=["", ""],  # no wedge labels
            radius=1.2,       # bigger overall pie
            wedgeprops=dict(width=0.3, edgecolor='white')  # thinner ring
        )
        ax.axis('equal')  # keeps the pie chart circular

        # Place two numbers in the donut hole, top and bottom
        top_y = 0.3
        bot_y = -0.3
        ax.text(0,  top_y, f"{int(total_blue)}",
                color='white', ha='center', va='center', fontsize=10)
        ax.text(0, bot_y, f"{int(total_red)}",
                color='white', ha='center', va='center', fontsize=10)

        # Thin horizontal line between the two numbers
        ax.plot([-0.6, 0.6], [0, 0], color='white', linewidth=2)

        # Draw the donut hole. Its radius = (overall radius) - (donut ring width)
        hole_radius = 1.2 - 0.3   # = 0.9
        centre_circle = Circle((0, 0), hole_radius, fc=BACKGROUND_COLOR)
        ax.add_artist(centre_circle)
        ax.set_facecolor(BACKGROUND_COLOR)


    def add_champion_icons(ax, df, y_positions, zoom=0.1):
        """
        Attach champion icons at the same y-positions as the bars.
        'y_positions' must match the bar chart arrangement (like np.arange(len(df))*0.8).
        """
        for idx, row in df.iterrows():
            champion_name = row["Champion"]
            icon_path = current_dir / "tiles" / f"{champion_name}_0.jpg"
            if icon_path.exists():
                img = plt.imread(icon_path)
                image_box = OffsetImage(img, zoom=zoom)

                y_coord = y_positions[idx]  # align icon with the bar
                ab = AnnotationBbox(
                    image_box,
                    (0, y_coord),            
                    frameon=False,
                    box_alignment=(1.0, 0.5),
                    clip_on=False,
                    zorder=10
                )
                ax.add_artist(ab)

    import numpy as np
    def draw_metric(ax_container, metric_name, df_blue, df_red, column_name, fontsize=15):
        gs = ax_container.get_subplotspec().subgridspec(1, 3, wspace=0.06)
        ax_container.set_visible(False)

        left_ax = ax_container.figure.add_subplot(gs[0, 0])
        donut_ax = ax_container.figure.add_subplot(gs[0, 1])
        right_ax = ax_container.figure.add_subplot(gs[0, 2])

        # Get maximum value for scaling
        max_val = max(df_blue[column_name].max(), df_red[column_name].max())

        spacing = 0.25  # Vertical spacing between bars
        bar_height = 0.15
        y_pos_blue = np.arange(len(df_blue)) * spacing
        y_pos_red = np.arange(len(df_red)) * spacing

        bar_length_ratio = 0.8  # Total bar length is reduced to 80% of axis width

        # ------------------------- LEFT BAR CHART (BLUE) -------------------------
        # Draw reduced-length background bars
        left_ax.barh(
            y_pos_blue, 
            [bar_length_ratio] * len(df_blue), 
            color="gray", 
            height=bar_height, 
            alpha=0.3
        )
        # Draw filled bars proportional to max_val
        bars_blue = left_ax.barh(
            y_pos_blue, 
            (df_blue[column_name] / max_val) * bar_length_ratio, 
            color=COLOR_BLUE, 
            height=bar_height
        )
        # Annotate numeric values
        annotate_barh(left_ax, bars_blue, df_blue[column_name], total_bar_length=bar_length_ratio, fontsize=12)

        # Add champion icons
        add_champion_icons(left_ax, df_blue, y_pos_blue)

        # Format left axis
        left_ax.set_facecolor(BACKGROUND_COLOR)
        left_ax.set_yticks([])
        left_ax.set_xticks([])
        for spine in ["top", "right", "left", "bottom"]:
            left_ax.spines[spine].set_visible(False)

        # ------------------------- MIDDLE DONUT CHART ---------------------------
        total_blue = df_blue[column_name].sum()
        total_red = df_red[column_name].sum()
        create_donut_chart(donut_ax, total_blue, total_red, fontsize=fontsize)
        donut_ax.set_facecolor(BACKGROUND_COLOR)
        donut_ax.set_title(metric_name, color=COLORS['TEXT'], fontsize=fontsize + 2, pad=15)

        # ------------------------- RIGHT BAR CHART (RED) -------------------------
        # Draw reduced-length background bars
        right_ax.barh(
            y_pos_red, 
            [bar_length_ratio] * len(df_red), 
            color="gray", 
            height=bar_height, 
            alpha=0.3
        )
        # Draw filled bars proportional to max_val
        bars_red = right_ax.barh(
            y_pos_red, 
            (df_red[column_name] / max_val) * bar_length_ratio, 
            color=COLOR_RED, 
            height=bar_height
        )
        # Annotate numeric values
        annotate_barh(right_ax, bars_red, df_red[column_name], total_bar_length=bar_length_ratio, fontsize=12)

        # Add champion icons
        add_champion_icons(right_ax, df_red, y_pos_red)

        # Format right axis
        right_ax.set_facecolor(BACKGROUND_COLOR)
        right_ax.set_yticks([])
        right_ax.set_xticks([])
        for spine in ["top", "right", "left", "bottom"]:
            right_ax.spines[spine].set_visible(False)

        # ------------------------- UNIFY X-LIMITS -------------------------------
        left_ax.set_xlim([0, 1])  # Fix the total width to 1
        right_ax.set_xlim([0, 1])


    from matplotlib.lines import Line2D


    # ---------------------- TKINTER BOILERPLATE ----------------------
    root = tk.Tk()
    root.title("League of Legends Statistics")
    root.geometry("1600x900")
    stats_frame = tk.Frame(root)
    stats_frame.pack(fill=tk.BOTH, expand=True)

    fig, panels = plt.subplots(2, 3, figsize=(30, 18), dpi=120, constrained_layout=True)
    fig.patch.set_facecolor(BACKGROUND_COLOR)
    stats_frame.pack(fill=tk.BOTH, expand=True)

    fig, panels = plt.subplots(2, 3, figsize=(30, 18), dpi=120, constrained_layout=True)
    fig.patch.set_facecolor(BACKGROUND_COLOR)

    # Row 0, col 0: Kills
    draw_metric(
        panels[0, 0],
        "Kills",
        blue_team,
        red_team,
        "Kills",
        fontsize=12
    )
    # Row 0, col 1: Gold
    draw_metric(
        panels[0, 1],
        "Gold earned",
        blue_team,
        red_team,
        "Total Gold Earned",
        fontsize=12
    )
    # Row 0, col 2: Damage Dealt
    draw_metric(
        panels[0, 2],
        "Damage dealt to champions",
        blue_team,
        red_team,
        "Total Damage dealt to Champions",
        fontsize=12
    )
    # Row 1, col 0: Wards
    draw_metric(
        panels[1, 0],
        "Wards placed",
        blue_team,
        red_team,
        "Wards Placed",
        fontsize=12
    )
    # Row 1, col 1: Damage Taken
    draw_metric(
        panels[1, 1],
        "Damage taken",
        blue_team,
        red_team,
        "Total Damage taken",
        fontsize=12
    )
    # Row 1, col 2: CS
    draw_metric(
        panels[1, 2],
        "CS",
        blue_team,
        red_team,
        "CS",
        fontsize=12
    )

    # ---------------------- Add Separator Lines ----------------------
    # These lines are drawn in figure-relative coordinates:
    # The x-coords or y-coords range from 0 to 1 across the figure.

    # Vertical lines between the 3 subplot columns:
    line1 = Line2D([0.33, 0.33], [0, 1], transform=fig.transFigure,
                color='white', linewidth=1, alpha=0.6)
    line2 = Line2D([0.66, 0.66], [0, 1], transform=fig.transFigure,
                color='white', linewidth=1, alpha=0.6)
    fig.add_artist(line1)
    fig.add_artist(line2)

    # Horizontal line between row 0 and row 1:
    line3 = Line2D([0, 1], [0.5, 0.5], transform=fig.transFigure,
                color='white', linewidth=1, alpha=0.6)
    fig.add_artist(line3)

    # Now place the figure on the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=stats_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    root.mainloop()




