from manimlib import *
import numpy as np

class AIInvestmentGraph(Scene):
    def construct(self):
        # Create a title for the animation
        title = Text("AI Advancement by Country (2017-2023)")
        title.scale(1.2)
        title.to_edge(UP)
        
        # Define the axes
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 100, 20],
            width=10,
            height=6,
            axis_config={
                "stroke_width": 2,
                "include_ticks": True,
                "include_tip": False,
            }
        )
        axes.center()
        axes.shift(DOWN * 0.5)
        
        # Add labels to the axes
        x_label = Text("Year")
        x_label.next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("AI Advancement Score")
        y_label.next_to(axes.y_axis.get_end(), UP)
        
        # Year labels
        years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
        x_ticks = VGroup()
        for i, year in enumerate(years):
            x_pos = i
            tick = Text(str(year), font_size=24)
            tick.next_to(axes.c2p(x_pos, 0), DOWN, buff=0.1)
            x_ticks.add(tick)
        
        # Country data (estimated AI advancement scores)
        # Format: [country_name, color, [yearly_scores]]
        countries_data = [
            ["USA", "#FF0000", [65, 70, 78, 84, 88, 92, 95]],
            ["China", "#FFCC00", [52, 58, 68, 75, 82, 89, 93]],
            ["EU", "#0000FF", [60, 64, 70, 74, 79, 84, 89]],
            ["UK", "#800080", [58, 62, 67, 72, 76, 81, 86]],
            ["Japan", "#00FF00", [55, 59, 63, 68, 72, 77, 83]]
        ]
        
        # Create lines and points for each country
        country_lines = VGroup()
        country_dots = VGroup()
        country_labels = VGroup()
        
        # Create legend
        legend_items = VGroup()
        legend_pos = axes.c2p(5.5, 95)
        
        for country, color, scores in countries_data:
            # Create points
            dots = VGroup()
            points = []
            
            for i, score in enumerate(scores):
                point = axes.c2p(i, score)
                points.append(point)
                dot = Dot(point, radius=0.05, color=color)
                dots.add(dot)
            
            # Create line through points
            line = VMobject()
            line.set_points_as_corners(points)
            line.set_color(color)
            line.set_stroke(width=3)
            
            # Create label that will travel with the last point
            label = Text(country, font_size=24)
            label.next_to(dots[-1], RIGHT, buff=0.1)
            label.set_color(color)
            
            # Add to groups
            country_lines.add(line)
            country_dots.add(dots)
            country_labels.add(label)
            
            # Add legend item
            legend_dot = Dot(color=color)
            legend_dot.scale(0.8)
            legend_text = Text(country, font_size=20)
            legend_text.set_color(color)
            legend_text.next_to(legend_dot, RIGHT, buff=0.1)
            legend_item = VGroup(legend_dot, legend_text)
            legend_items.add(legend_item)
        
        # Arrange legend items vertically
        legend_items.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend_items.move_to(legend_pos, aligned_edge=UP + RIGHT)
        legend_box = SurroundingRectangle(legend_items, buff=0.1, color=WHITE, fill_opacity=0.1)
        legend = VGroup(legend_box, legend_items)
        
        # Animation sequence
        self.play(Write(title))
        self.play(ShowCreation(axes), Write(x_label), Write(y_label))
        self.play(AnimationGroup(*[FadeIn(tick) for tick in x_ticks], lag_ratio=0.1))
        self.wait(0.5)
        
        # Show legend
        self.play(FadeIn(legend))
        
        # Show the lines and dots with a sequential animation
        for i in range(len(countries_data)):
            self.play(
                ShowCreation(country_lines[i]),
                AnimationGroup(*[FadeIn(dot) for dot in country_dots[i]], lag_ratio=0.2),
                run_time=1.5
            )
            self.play(Write(country_labels[i]))
        
        self.wait(2)
        
        # Add a highlight animation for specific achievements or milestones
        milestone = Text("GPT-4 Release", font_size=24)
        milestone.next_to(axes.c2p(5, 92), UP + RIGHT, buff=0.1)
        arrow = Arrow(milestone.get_left(), axes.c2p(5, 92), buff=0.1, color=WHITE)
        
        self.play(
            Write(milestone),
            ShowCreation(arrow)
        )
        
        self.wait(3)
        
        # Cleanup
        self.play(
            FadeOut(VGroup(
                title, axes, x_label, y_label, x_ticks,
                country_lines, country_dots, country_labels,
                legend, milestone, arrow
            ))
        )
