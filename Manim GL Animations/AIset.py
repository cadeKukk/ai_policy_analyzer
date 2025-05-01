from manimlib import *
import numpy as np

class AIResearchCenters(Scene):
    def construct(self):
        # Data - countries with most AI research centers
        countries = [
            "United States", "China", "United Kingdom", "Germany", 
            "Canada", "Japan", "France", "Israel", "South Korea", "India"
        ]
        
        # Values represent number of AI research centers/relative strength
        # Based on research data with US having significantly more
        values = [100, 42, 30, 25, 22, 20, 18, 15, 14, 12]
        
        # Colors for gradient effect
        colors = [
            "#2D82B7", # Blue for top
            "#42B0D5", # Light blue
            "#55C1A7", # Teal
            "#68D090", # Light green
            "#9CDB58", # Yellow-green
            "#CFEB34", # Yellow
            "#FFD92F", # Light orange
            "#FFA927", # Orange
            "#FC7D22", # Dark orange
            "#FA4C1E"  # Red for bottom
        ]
        
        # Title
        title = Text("Nations with the Most AI Research Centers", font_size=48, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        subtitle = Text("Based on 2024 Research Data", font_size=28)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Create axes
        axes = Axes(
            x_range=[0, 110, 20],
            y_range=[0, 10, 1],
            axis_config={
                "include_tip": False,
                "include_numbers": True,
                "include_ticks": True,
                "line_to_number_buff": 0.2,
                "stroke_color": GREY_B,
                "stroke_width": 2,
                "tick_size": 0.05,
            },
            y_axis_config={
                "include_numbers": False,
            }
        )
        
        axes.center()
        axes.shift(DOWN * 0.5)
        
        # Create x-axis label
        x_label = Text("Number of Research Centers (normalized)", font_size=24)
        x_label.next_to(axes.x_axis, DOWN, buff=0.5)
        
        # Animate title and axes
        self.play(
            Write(title),
            Write(subtitle),
            Create(axes),
            Write(x_label),
            run_time=2
        )
        self.wait(0.5)
        
        # Create and animate bars and labels
        all_bars = VGroup()
        all_labels = VGroup()
        
        for i, (country, value, color) in enumerate(zip(countries, values, colors)):
            # Create bar
            bar = Rectangle(
                height=0.6,
                width=value / 100 * axes.x_axis.get_length(),
                fill_color=color,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=1,
            )
            
            # Position bar - reversed order so US is at the top
            y_pos = axes.y_axis.get_length() - i * 0.8 - 0.5
            bar.align_to(axes.c2p(0, 0), LEFT)
            bar.shift(UP * y_pos)
            
            # Create label with value
            label = Text(f"{country} ({value})", font_size=22)
            label.next_to(bar, LEFT, buff=0.25)
            
            all_bars.add(bar)
            all_labels.add(label)
            
            # Animate each bar and label with a growing effect
            self.play(
                GrowFromLeft(bar),
                FadeIn(label),
                run_time=0.7
            )
        
        # Add "America leads by a mile" annotation
        annotation = Text("America leads by a mile!", 
                          font_size=28, 
                          color=YELLOW)
        annotation.next_to(all_bars[0], RIGHT, buff=0.5)
        
        # Add an arrow pointing to the US bar
        arrow = Arrow(
            annotation.get_left() + DOWN * 0.2,
            all_bars[0].get_right() + DOWN * 0.2,
            buff=0.1,
            color=YELLOW
        )
        
        self.play(
            Write(annotation),
            GrowArrow(arrow),
            run_time=1
        )
        
        # Highlight the gap between US and other countries
        highlight_rect = Rectangle(
            width=all_bars[0].width - all_bars[1].width,
            height=3,
            fill_color=YELLOW,
            fill_opacity=0.2,
            stroke_color=YELLOW,
            stroke_width=2,
        )
        highlight_rect.align_to(all_bars[0], RIGHT)
        highlight_rect.align_to(all_bars[1], DOWN)
        
        self.play(
            FadeIn(highlight_rect),
            run_time=1
        )
        
        # "Innovation Gap" label
        gap_label = Text("Innovation Gap", 
                         font_size=24, 
                         color=YELLOW)
        gap_label.move_to(highlight_rect)
        gap_label.rotate(PI/2)  # Rotate vertically
        
        self.play(
            Write(gap_label),
            run_time=1
        )
        
        # Add note about investment
        investment_note = Text(
            "The US invests over $47B annually in AI - 3.5x more than China", 
            font_size=20,
            color=GREY_B
        )
        investment_note.to_edge(DOWN, buff=0.5)
        
        self.play(
            Write(investment_note),
            run_time=1.5
        )
        
        # Final pause
        self.wait(3)
        
        # Fade everything out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.5
        )


# Run this scene to create the animation
if __name__ == "__main__":
    scene = AIResearchCenters()
    scene.render()
