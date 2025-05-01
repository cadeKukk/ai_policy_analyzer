from manimlib import *

class NationalAIInitiativeAct(Scene):
    def construct(self):
        # Title - directly use uppercase in the string
        title = Text("NATIONAL AI INITIATIVE ACT", 
                     font_size=72, 
                     weight=BOLD).to_edge(UP)
        
        # Subtitle - directly use uppercase in the string
        subtitle = Text("OF 2020", 
                        font_size=48, 
                        weight=BOLD)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        # Background rectangle for the title section
        bg_rect = BackgroundRectangle(
            VGroup(title, subtitle),
            buff=0.5,
            fill_opacity=0.2,
            stroke_width=2,
            stroke_opacity=0.5
        )
        
        # Display title with animation
        self.play(
            FadeIn(bg_rect, scale=0.9),
            Write(title),
            run_time=1.5
        )
        self.play(Write(subtitle), run_time=1)
        self.wait(1)
        
        # Move title and subtitle to top to make room for goals
        self.play(
            VGroup(bg_rect, title, subtitle).animate.scale(0.8).to_edge(UP, buff=0.3),
            run_time=1
        )
        
        # Create the three main goals - already in uppercase
        goals = [
            "RESEARCH & DEVELOPMENT ADVANCEMENT",
            "ETHICS & GOVERNANCE FRAMEWORK",
            "U.S. GLOBAL COMPETITIVENESS"
        ]
        
        goal_texts = VGroup()
        
        # Create each goal text
        for i, goal in enumerate(goals):
            # Create goal text with bullet point
            bullet = Text("•", font_size=36, weight=BOLD)
            goal_text = Text(goal, font_size=36, weight=BOLD)
            
            # Group bullet and text
            goal_group = VGroup(bullet, goal_text)
            goal_group.arrange(RIGHT, buff=0.5, aligned_edge=LEFT)
            
            goal_texts.add(goal_group)
        
        # Arrange goals vertically in a list
        goal_texts.arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        goal_texts.next_to(VGroup(bg_rect, title, subtitle), DOWN, buff=1.0)
        
        # Center everything horizontally
        goal_texts.move_to(ORIGIN + DOWN * 0.5)
        
        # Play animation for each goal appearing one by one
        for goal in goal_texts:
            self.play(Write(goal), run_time=1.5)
            self.wait(0.5)
        
        # Highlight the first goal
        highlight_box1 = SurroundingRectangle(
            goal_texts[0],
            buff=0.3,
            stroke_color=YELLOW,
            stroke_width=4,
            stroke_opacity=1
        )
        
        # Animate the first highlight box appearing
        self.play(ShowCreation(highlight_box1), run_time=1)
        self.wait(1.5)
        
        # Remove first highlight and create highlight for second goal
        highlight_box2 = SurroundingRectangle(
            goal_texts[1],
            buff=0.3,
            stroke_color=YELLOW,
            stroke_width=4,
            stroke_opacity=1
        )
        
        # Remove first highlight and show second highlight
        self.play(
            FadeOut(highlight_box1),
            ShowCreation(highlight_box2),
            run_time=1
        )
        self.wait(1.5)
        
        # Remove second highlight and create highlight for third goal
        highlight_box3 = SurroundingRectangle(
            goal_texts[2],
            buff=0.3,
            stroke_color=YELLOW,
            stroke_width=4,
            stroke_opacity=1
        )
        
        # Remove second highlight and show third highlight
        self.play(
            FadeOut(highlight_box2),
            ShowCreation(highlight_box3),
            run_time=1
        )
        self.wait(1.5)
        
        # Hold the final frame with the third highlight
        self.wait(2)
