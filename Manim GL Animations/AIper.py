from manimlib import *
import os
import numpy as np

class ModelsByCountryChart(Scene):
    def construct(self):
        # Set background color to light grey to match the image
        self.camera.background_color = "#E0E4E8"
        
        # Data for the chart - countries and their model counts
        countries = ["United States", "China", "France", "Germany", "Canada"]
        model_counts = [61, 15, 8, 5, 4]
        
        # Define colors
        bar_color = "#2A93D5"  # Blue color for bars
        dot_color = "#E56DB1"  # Pink color for dots
        
        # Create title
        title = Text(
            "NUMBER OF NOTABLE MACHINE",
            font_size=42,
            color=BLACK,
            weight=BOLD
        ).to_edge(UP, buff=0.3)
        
        subtitle = Text(
            "LEARNING MODELS BY COUNTRY, 2023",
            font_size=42,
            color=BLACK,
            weight=BOLD
        )
        subtitle.next_to(title, DOWN, buff=0.1)
        
        # Create source text
        source_text = Text(
            "SOURCE: EPOCH, 2023 | CHART: 2024 AI INDEX REPORT",
            font_size=20,
            color=BLACK,
            weight=BOLD
        )
        source_text.next_to(subtitle, DOWN, buff=0.2)
        
        # Create container for all chart elements
        chart_container = VGroup()
        
        # Create bars for each country
        bars = VGroup()
        max_height = 4  # Reduced maximum height for better fitting
        max_count = max(model_counts)
        bar_width = 1.0  # Slightly narrower bars
        
        # Calculate spacing
        total_width = len(countries) * (bar_width + 0.5) - 0.5
        start_x = -total_width / 2 + bar_width / 2
        
        # Create dot matrices for the bars
        dot_matrices = VGroup()
        
        # Country labels and flags
        country_labels = VGroup()
        country_flags = VGroup()
        number_labels = VGroup()  # Separate group for number labels
        
        # Loop through each country to create its bar and elements
        for i, (country, count) in enumerate(zip(countries, model_counts)):
            # Calculate bar position
            x_pos = start_x + i * (bar_width + 0.5)
            
            # Create the bar
            bar_height = (count / max_count) * max_height
            bar = Rectangle(
                height=bar_height,
                width=bar_width,
                fill_color=bar_color,
                fill_opacity=1,
                stroke_width=0
            )
            
            # Position bar from the bottom (vertical center aligned with bottom)
            bar.move_to(np.array([x_pos, -1 + bar_height/2, 0]))
            bars.add(bar)
            
            # Add count number ABOVE the bar (not inside)
            count_text = Text(
                str(count),
                font_size=36,
                color=BLACK,
                weight=BOLD
            )
            count_text.next_to(bar, UP, buff=0.2)
            number_labels.add(count_text)
            
            # Create dot matrix for this country
            dots_per_row = 5
            rows_needed = (count + dots_per_row - 1) // dots_per_row  # Ceiling division
            
            dot_matrix = VGroup()
            for row in range(rows_needed):
                for col in range(min(dots_per_row, count - row * dots_per_row)):
                    dot = Dot(
                        radius=0.07,  # Slightly smaller dots
                        color=dot_color,
                        fill_opacity=1
                    )
                    
                    # Place dots in a grid pattern inside the bar
                    dot_x = x_pos - bar_width/2 + 0.15 + col * 0.18
                    dot_y = bar.get_bottom()[1] + 0.15 + row * 0.18
                    
                    dot.move_to(np.array([dot_x, dot_y, 0]))
                    dot_matrix.add(dot)
            
            dot_matrices.add(dot_matrix)
            
            # Create country label with smaller font size
            # For United States, create two separate text objects and group them
            if country == "United States":
                label1 = Text("UNITED", font_size=20, color=BLACK, weight=BOLD)
                label2 = Text("STATES", font_size=20, color=BLACK, weight=BOLD)
                label = VGroup(label1, label2)
                label.arrange(DOWN, buff=0.1)
            else:
                label = Text(country.upper(), font_size=20, color=BLACK, weight=BOLD)
            
            label.next_to(bar, DOWN, buff=0.3)
            country_labels.add(label)
            
            # Create flag emoji (as text for simplicity)
            flag_emoji = ""
            if country == "United States":
                flag_emoji = "🇺🇸"
            elif country == "China":
                flag_emoji = "🇨🇳"
            elif country == "France":
                flag_emoji = "🇫🇷"
            elif country == "Germany":
                flag_emoji = "🇩🇪"
            elif country == "Canada":
                flag_emoji = "🇨🇦"
            
            flag = Text(
                flag_emoji,
                font_size=30
            )
            flag.next_to(label, DOWN, buff=0.15)
            country_flags.add(flag)
        
        # Add all elements to chart container
        chart_container.add(bars, dot_matrices, country_labels, country_flags, number_labels)
        
        # Move the chart container further down (increasing from 1.0 to 1.5 for an additional 15%)
        chart_container.shift(DOWN * 1.5)  # Changed from 1.0 to 1.5
        
        # New animation sequence for titles and all bars at once
        self.play(
            Write(title),
            Write(subtitle),
            run_time=1.5
        )
        self.play(Write(source_text), run_time=0.8)
        self.wait(0.5)
        
        # Animate all bars appearing at once
        self.play(
            *[GrowFromEdge(bar, DOWN) for bar in bars],
            run_time=1.2
        )
        
        # Add number labels after bars are drawn
        self.play(
            LaggedStartMap(FadeIn, number_labels, lag_ratio=0.2),
            run_time=1
        )
        
        # Show dot matrices filling in
        for dot_matrix in dot_matrices:
            self.play(
                LaggedStartMap(FadeIn, dot_matrix, lag_ratio=0.02),
                run_time=1
            )
        
        # Show country labels and flags
        self.play(
            LaggedStartMap(FadeIn, country_labels, lag_ratio=0.2),
            LaggedStartMap(FadeIn, country_flags, lag_ratio=0.2),
            run_time=1.5
        )
        
        # Hold the final frame
        self.wait(2)
