from manimlib import *
import numpy as np

class ComputationalPowerComparison(Scene):
    def construct(self):
        # Define the axes with smaller dimensions
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 800, 200],
            width=9,
            height=5,
            axis_config={
                "stroke_width": 2,
                "include_ticks": True,
                "include_tip": False,
            }
        )
        axes.center()
        # Shift the graph left and slightly down
        axes.shift(LEFT * 1.0 + DOWN * 0.2)
        
        # Add labels to the axes - with adjusted positions
        x_label = Text("COMPLEXITY", weight=BOLD)
        # Move complexity label UP to avoid overlap with "EXTREME"
        x_label.next_to(axes.x_axis.get_end(), RIGHT + UP * 0.7)
        
        # Keep "COMPUTATIONAL" as the y-axis label
        y_label = Text("COMPUTATIONAL", weight=BOLD)
        # Shift computational label right to be more visible
        y_label.next_to(axes.y_axis.get_end(), UP)
        y_label.shift(RIGHT * 1.5)  # Move label more toward the middle
        
        # Add numerical y-axis labels (50, 100, 150, etc.)
        y_tick_values = [0, 200, 400, 600, 800]
        y_tick_labels = VGroup()
        
        for value in y_tick_values:
            label = Text(str(value), font_size=16, weight=BOLD)
            label.next_to(axes.c2p(0, value), LEFT, buff=0.2)
            y_tick_labels.add(label)
        
        # Complexity labels - NOW IN ALL CAPS AND BOLD
        complexity_levels = ["SIMPLE", "MODERATE", "COMPLEX", "VERY COMPLEX", "EXTREME"]
        x_ticks = VGroup()
        for i, level in enumerate(complexity_levels):
            x_pos = i
            tick = Text(level, font_size=22, weight=BOLD)
            tick.next_to(axes.c2p(x_pos, 0), DOWN, buff=0.15)
            if i == 3:  # "VERY COMPLEX" is two words and needs adjustment
                tick.scale(0.8)
            x_ticks.add(tick)
        
        # Model data (based on the image)
        models_data = [
            ["Claude", "#6495ED", [100, 180, 320, 500, 760]],
            ["DeepSeek", "#90EE90", [30, 60, 90, 130, 175]]
        ]
        
        # Create lines and points for each model
        model_lines = VGroup()
        model_dots = VGroup()
        
        # Create legend
        legend_items = VGroup()
        # Adjust legend position to account for the shifted graph
        legend_pos = UP * 3 + RIGHT * 2.5
        
        for model, color, scores in models_data:
            # Create points
            dots = VGroup()
            points = []
            
            for i, score in enumerate(scores):
                point = axes.c2p(i, score)
                points.append(point)
                dot = Dot(point, radius=0.08, color=color)
                dots.add(dot)
            
            # Create line through points
            line = VMobject()
            line.set_points_as_corners(points)
            line.set_color(color)
            line.set_stroke(width=3)
            
            # Add to groups
            model_lines.add(line)
            model_dots.add(dots)
            
            # Add legend item - model names stay as is (not all caps or bold)
            legend_dot = Dot(color=color)
            legend_dot.scale(0.8)
            legend_text = Text(model, font_size=20)
            legend_text.set_color(color)
            legend_text.next_to(legend_dot, RIGHT, buff=0.1)
            legend_item = VGroup(legend_dot, legend_text)
            legend_items.add(legend_item)
        
        # Arrange legend items horizontally
        legend_items.arrange(RIGHT, aligned_edge=UP, buff=0.5)
        legend_items.move_to(legend_pos, aligned_edge=UP)
        
        # Add grid lines
        grid_lines = VGroup()
        
        # Horizontal grid lines
        for y in range(0, 801, 200):
            line = DashedLine(
                axes.c2p(0, y),
                axes.c2p(4, y),
                stroke_width=0.5,
                stroke_opacity=0.4,
                dash_length=0.1
            )
            grid_lines.add(line)
        
        # Vertical grid lines
        for x in range(0, 5):
            line = DashedLine(
                axes.c2p(x, 0),
                axes.c2p(x, 800),
                stroke_width=0.5,
                stroke_opacity=0.4,
                dash_length=0.1
            )
            grid_lines.add(line)
        
        # Animation sequence
        self.play(
            ShowCreation(grid_lines, lag_ratio=0.1),
            ShowCreation(axes),
            Write(x_label),
            Write(y_label),
            run_time=1.5
        )
        
        # Show both x and y tick labels
        self.play(
            AnimationGroup(*[FadeIn(tick) for tick in x_ticks], lag_ratio=0.1),
            AnimationGroup(*[FadeIn(label) for label in y_tick_labels], lag_ratio=0.1),
            run_time=1.5
        )
        
        # Show legend
        self.play(FadeIn(legend_items))
        
        # Show each model's data one by one
        for i in range(len(models_data)):
            self.play(
                ShowCreation(model_lines[i]),
                AnimationGroup(*[FadeIn(dot) for dot in model_dots[i]], lag_ratio=0.2),
                run_time=2
            )
        
        # Calculate the difference at the extreme point (x=4)
        claude_extreme = models_data[0][2][-1]  # 760
        deepseek_extreme = models_data[1][2][-1]  # 175
        ratio = claude_extreme / deepseek_extreme
        ratio_formatted = f"{ratio:.1f}"  # Format to one decimal place WITHOUT the "x"
        
        # Position the bracket to the right of the extreme points
        x_pos = 4.2  # Position just right of the extreme point at x=4
        offset = 0.2  # Offset for the horizontal segments
        
        # Vertical line of the bracket
        bracket_line = Line(
            axes.c2p(x_pos, deepseek_extreme),
            axes.c2p(x_pos, claude_extreme),
            stroke_width=2,
            stroke_color=WHITE
        )
        
        # Top horizontal segment - pointing toward the Claude dot
        bracket_top = Line(
            axes.c2p(x_pos, claude_extreme),
            axes.c2p(x_pos - offset, claude_extreme),  # Point toward x=4 where the dot is
            stroke_width=2,
            stroke_color=WHITE
        )
        
        # Bottom horizontal segment - pointing toward the DeepSeek dot
        bracket_bottom = Line(
            axes.c2p(x_pos, deepseek_extreme),
            axes.c2p(x_pos - offset, deepseek_extreme),  # Point toward x=4 where the dot is
            stroke_width=2,
            stroke_color=WHITE
        )
        
        # Create the label - NOW IN ALL CAPS, BOLD, AND WITHOUT THE EXTRA "x"
        bracket_label = Text(f"{ratio_formatted}X", font_size=24, color=WHITE, weight=BOLD)
        # Position the label to the right of the bracket
        bracket_label.next_to(bracket_line, RIGHT, buff=0.3)
        
        # Show the bracket after all animations
        self.play(
            ShowCreation(bracket_line),
            ShowCreation(bracket_top),
            ShowCreation(bracket_bottom),
            run_time=1
        )
        
        self.play(Write(bracket_label), run_time=1)
        
        self.wait(2)
        
        # Now add ChatGPT with off-the-charts requirements
        chatgpt_color = "#FF9500"  # Orange color for ChatGPT
        
        # Create ChatGPT label for legend without modifying existing legend
        chatgpt_legend_dot = Dot(color=chatgpt_color)
        chatgpt_legend_dot.scale(0.8)
        chatgpt_legend_text = Text("ChatGPT", font_size=20)
        chatgpt_legend_text.set_color(chatgpt_color)
        chatgpt_legend_text.next_to(chatgpt_legend_dot, RIGHT, buff=0.1)
        chatgpt_legend_item = VGroup(chatgpt_legend_dot, chatgpt_legend_text)
        
        # Position the ChatGPT legend to the left of existing legend without changing its layout
        chatgpt_legend_item.next_to(legend_items, LEFT, buff=1.0)
        
        # CHANGED: ChatGPT points to create a spike effect
        # Simple point - starts relatively higher than others
        simple_point = axes.c2p(0, 300)  # Start high at "Simple"
        
        # Moderate point - place just below top of chart 
        moderate_point = axes.c2p(1, 750)  # Just below top at "Moderate"
        
        # Complex point - goes way off chart (will not be visible)
        complex_point = axes.c2p(2, 1500)  # Off chart at "Complex"
        
        # Create dots for visible points
        chatgpt_simple_dot = Dot(simple_point, radius=0.08, color=chatgpt_color)
        chatgpt_moderate_dot = Dot(moderate_point, radius=0.08, color=chatgpt_color)
        
        # Create the visible segment from Simple to Moderate
        chatgpt_visible_line = Line(
            simple_point,
            moderate_point,
            stroke_width=3,
            stroke_color=chatgpt_color
        )
        
        # Create the segment that goes off chart (from Moderate to Complex)
        # This will create the natural spike effect without using an arrow
        chatgpt_offchart_line = Line(
            moderate_point,
            complex_point,
            stroke_width=3,
            stroke_color=chatgpt_color
        )
        
        # Add ChatGPT to legend first
        self.play(FadeIn(chatgpt_legend_item), run_time=1)
        
        # Show ChatGPT's starting point at Simple
        self.play(FadeIn(chatgpt_simple_dot), run_time=0.5)
        
        # Show the line going up to Moderate and the Moderate dot
        self.play(
            ShowCreation(chatgpt_visible_line),
            FadeIn(chatgpt_moderate_dot),
            run_time=1
        )
        
        # Show the line continuing off the chart - creating a spike effect
        self.play(ShowCreation(chatgpt_offchart_line), run_time=1)
        
        self.wait(2)
        
        # Add a horizontal highlight line at computational level 250
        highlight_y = 250
        highlight_line = Line(
            axes.c2p(0, highlight_y),
            axes.c2p(4, highlight_y),
            stroke_width=2.5,
            stroke_color=YELLOW,
        )
        
        # Optional: Add a label for the highlight line
        highlight_label = Text("250", font_size=18, color=YELLOW, weight=BOLD)
        highlight_label.next_to(axes.c2p(0, highlight_y), LEFT, buff=0.2)
        
        # Show the highlight line with a pulsing animation
        self.play(
            ShowCreation(highlight_line),
            FadeIn(highlight_label),
            run_time=1.5
        )
        
        # Make the line pulse to draw attention to it
        self.play(
            highlight_line.animate.set_stroke(width=4),
            run_time=0.5
        )
        self.play(
            highlight_line.animate.set_stroke(width=2.5),
            run_time=0.5
        )
        
        self.wait(3)
