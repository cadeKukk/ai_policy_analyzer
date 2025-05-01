from manimlib import *
import numpy as np

class AIGovernanceStructure(Scene):
    def construct(self):
        # Scale camera to fit everything
        self.camera.frame.scale(1.1)
        
        # Title
        title = Text("GOVERNMENT AI ASSESSMENT STRUCTURE", font_size=48, weight=BOLD).to_edge(UP)
        subtitle = Text("Oversight and Evaluation of AI in Public and Private Sectors", font_size=28)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Create background rectangle for title
        bg_rect = BackgroundRectangle(
            VGroup(title, subtitle),
            buff=0.3,
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
        
        # Move title and subtitle to top
        self.play(
            VGroup(bg_rect, title, subtitle).animate.scale(0.8).to_edge(UP, buff=0.3),
            run_time=1
        )
        
        # Define the agency hierarchy with adjusted positions
        
        # Create Federal Level Agencies
        federal = self.create_agency_box("FEDERAL OVERSIGHT", BLUE_D, 6.0, position=UP * 1.5)
        
        # Create agency boxes for federal level
        federal_agencies = {
            "White House Office of\nScience & Technology": {"color": BLUE, "width": 3.0},
            "National AI\nInitiative Office": {"color": BLUE_B, "width": 3.0},
            "NIST AI\nRisk Management": {"color": BLUE_B, "width": 3.0},
            "AI Bill of Rights\n(Blueprint)": {"color": BLUE_B, "width": 3.0}
        }
        
        federal_boxes = self.create_agency_group(federal_agencies, UP * 0.2)
        
        # Create Regulatory Agencies Level - adjusted position
        regulatory = self.create_agency_box("REGULATORY AGENCIES", GREEN_D, 6.0, position=DOWN * 0.8)
        
        # Create agency boxes for regulatory level
        regulatory_agencies = {
            "FTC": {"color": GREEN, "width": 1.8},
            "FDA": {"color": GREEN, "width": 1.8},
            "DOJ": {"color": GREEN, "width": 1.8},
            "SEC": {"color": GREEN, "width": 1.8},
            "CFPB": {"color": GREEN, "width": 1.8}
        }
        
        regulatory_boxes = self.create_agency_group(regulatory_agencies, DOWN * 1.6)
        
        # Create Assessment Frameworks - moved up to ensure visibility
        assessment = self.create_agency_box("ASSESSMENT FRAMEWORKS", PURPLE_D, 6.0, position=DOWN * 2.9)
        
        # Create framework boxes - moved up
        frameworks = {
            "AI Impact\nAssessments": {"color": PURPLE, "width": 2.5},
            "Algorithmic\nAuditing": {"color": PURPLE, "width": 2.5},
            "Responsible AI\nGuidelines": {"color": PURPLE, "width": 2.5}
        }
        
        framework_boxes = self.create_agency_group(frameworks, DOWN * 3.7)
        
        # Create connector lines from Federal to Regulatory
        federal_to_regulatory = self.create_connector_lines(federal, regulatory)
        
        # Create connector lines from Regulatory to Assessment
        regulatory_to_assessment = self.create_connector_lines(regulatory, assessment)
        
        # Create highlights for each level
        federal_highlight = SurroundingRectangle(
            VGroup(federal, federal_boxes),
            buff=0.2,
            stroke_color=BLUE,
            stroke_width=2,
            stroke_opacity=0.8,
            fill_opacity=0.0
        ).round_corners(0.2)
        
        regulatory_highlight = SurroundingRectangle(
            VGroup(regulatory, regulatory_boxes),
            buff=0.2,
            stroke_color=GREEN,
            stroke_width=2,
            stroke_opacity=0.8,
            fill_opacity=0.0
        ).round_corners(0.2)
        
        assessment_highlight = SurroundingRectangle(
            VGroup(assessment, framework_boxes),
            buff=0.2,
            stroke_color=PURPLE,
            stroke_width=2,
            stroke_opacity=0.8,
            fill_opacity=0.0
        ).round_corners(0.2)
        
        # Animation sequence
        
        # Show the federal level
        self.play(
            FadeIn(federal),
            run_time=1
        )
        self.play(
            LaggedStartMap(FadeIn, federal_boxes),
            run_time=1.5
        )
        
        # Show the regulatory level
        self.play(
            FadeIn(regulatory),
            run_time=1
        )
        self.play(
            LaggedStartMap(FadeIn, regulatory_boxes),
            run_time=1.5
        )
        
        # Show the assessment frameworks
        self.play(
            FadeIn(assessment),
            run_time=1
        )
        self.play(
            LaggedStartMap(FadeIn, framework_boxes),
            run_time=1.5
        )
        
        # Show connector lines
        self.play(
            ShowCreation(federal_to_regulatory),
            run_time=1.5
        )
        self.play(
            ShowCreation(regulatory_to_assessment),
            run_time=1.5
        )
        
        # Highlight each level in sequence
        self.play(ShowCreation(federal_highlight), run_time=1)
        self.wait(1)
        self.play(FadeOut(federal_highlight), run_time=0.5)
        
        self.play(ShowCreation(regulatory_highlight), run_time=1)
        self.wait(1)
        self.play(FadeOut(regulatory_highlight), run_time=0.5)
        
        self.play(ShowCreation(assessment_highlight), run_time=1)
        self.wait(1)
        self.play(FadeOut(assessment_highlight), run_time=0.5)
        
        # Create process flow path
        process_path = self.create_process_flow_path(federal, federal_boxes, regulatory, regulatory_boxes, assessment, framework_boxes)
        
        # Show the process flow
        self.play(
            ShowCreation(process_path),
            run_time=3
        )
        
        # Pulse animation to make the path more obvious
        self.play(
            process_path.animate.set_stroke(width=5),
            run_time=0.5
        )
        self.play(
            process_path.animate.set_stroke(width=3),
            run_time=0.5
        )
        
        # AFTER the process flow is complete, start the sequential deactivation
        
        # First fade AI Impact Assessment (first box in framework_boxes)
        self.play(
            framework_boxes[0].animate.set_opacity(0.3),
            run_time=0.7
        )
        
        # Then fade Algorithmic Auditing (second box)
        self.play(
            framework_boxes[1].animate.set_opacity(0.3),
            run_time=0.7
        )
        
        # Then fade Responsible AI Guidelines (third box)
        self.play(
            framework_boxes[2].animate.set_opacity(0.3),
            run_time=0.7
        )
        
        # Finally fade the main Assessment Frameworks title and connector lines
        self.play(
            assessment.animate.set_opacity(0.3),
            assessment_highlight.animate.set_stroke(opacity=0.2),
            regulatory_to_assessment.animate.set_opacity(0.3),
            run_time=1
        )
        
        # Final pause
        self.wait(2)
        
    def create_agency_box(self, name, color, width, position=ORIGIN):
        box = RoundedRectangle(
            width=width,
            height=0.7,
            corner_radius=0.2,
            fill_color=color,
            fill_opacity=0.8,
            stroke_width=2,
            stroke_color=WHITE
        )
        
        text = Text(name, font_size=28, weight=BOLD)
        text.move_to(box.get_center())
        
        result = VGroup(box, text)
        result.move_to(position)
        
        return result
    
    def create_agency_group(self, agencies, position=ORIGIN):
        boxes = VGroup()
        
        for i, (name, info) in enumerate(agencies.items()):
            box = RoundedRectangle(
                width=info["width"],
                height=0.7,
                corner_radius=0.2,
                fill_color=info["color"],
                fill_opacity=0.7,
                stroke_width=1.5,
                stroke_color=WHITE
            )
            
            text = Text(name, font_size=20, weight=BOLD)
            text.move_to(box.get_center())
            
            agency = VGroup(box, text)
            boxes.add(agency)
        
        boxes.arrange(RIGHT, buff=0.3)
        boxes.move_to(position)
        
        return boxes
    
    def create_connector_lines(self, top_box, bottom_box):
        lines = VGroup()
        
        # Create multiple lines between the boxes
        num_lines = 3
        top_points = [
            top_box[0].get_bottom() + LEFT * (i - (num_lines-1)/2) * 0.5
            for i in range(num_lines)
        ]
        
        bottom_points = [
            bottom_box[0].get_top() + LEFT * (i - (num_lines-1)/2) * 0.5
            for i in range(num_lines)
        ]
        
        for start, end in zip(top_points, bottom_points):
            line = Line(
                start, 
                end, 
                stroke_width=2,
                color=GREY_B
            )
            lines.add(line)
        
        return lines
    
    def create_process_flow_path(self, federal, federal_boxes, regulatory, regulatory_boxes, assessment, framework_boxes):
        # Create a path that hits both main category labels and specific nodes
        
        # Pick all the key points we need to hit
        federal_center = federal[0].get_center()  # Federal Oversight main label
        niai_center = federal_boxes[1][0].get_center()  # National AI Initiative Office
        
        regulatory_center = regulatory[0].get_center()  # Regulatory Agencies main label
        ftc_center = regulatory_boxes[0][0].get_center()  # FTC
        
        assessment_center = assessment[0].get_center()  # Assessment Frameworks main label
        impact_center = framework_boxes[0][0].get_center()  # AI Impact Assessment
        
        # Create a path with minimal bends that hits all required points
        path = VMobject()
        
        # Simplified path hitting all main labels and specific nodes
        path.set_points_as_corners([
            federal_center,  # Start at Federal Oversight label
            niai_center,  # Go to National AI Initiative Office
            np.array([niai_center[0], regulatory_center[1], 0]),  # Vertical line to Regulatory level
            regulatory_center,  # Hit Regulatory Agencies label
            ftc_center,  # Go to FTC
            np.array([ftc_center[0], assessment_center[1], 0]),  # Vertical line to Assessment level
            assessment_center,  # Hit Assessment Frameworks label
            impact_center  # End at AI Impact Assessment
        ])
        
        # Bold yellow styling for visibility
        path.set_stroke(color=YELLOW, width=4, opacity=0.9)
        
        return path
