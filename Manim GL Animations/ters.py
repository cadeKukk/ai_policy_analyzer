from manimlib import *

class AISourcesScene(Scene):
    def construct(self):
        # Dark background
        self.camera.background_color = BLACK
        
        # List of sources with acronyms
        sources = [
            "NAIIA - National Artificial Intelligence Initiative Act",
            "NAIIO - National Artificial Intelligence Initiative Office",
            "NAIRRTF - National AI Research Resource Task Force",
            "NITRD - Networking & Information Technology Research & Development",
            "NIST - National Institute of Standards and Technology AI Risk Management Framework",
            "NSF AI - National Science Foundation AI Research Institutes",
            "DOE AITO - Department of Energy Artificial Intelligence & Technology Office",
            "OSTP - Office of Science and Technology Policy",
            "OECD AIPO - OECD AI Policy Observatory",
            "GPAI - Global Partnership on Artificial Intelligence",
            "UNESCO AIETHICS - UNESCO Recommendation on AI Ethics",
            "EU AI ACT - European Union Artificial Intelligence Act",
            "WEF AI - World Economic Forum AI Governance Alliance",
            "Stanford HAI - Stanford Human-Centered Artificial Intelligence",
            "AAAI - Association for the Advancement of Artificial Intelligence",
            "IEEE ECAI - IEEE Global Initiative on Ethics of Autonomous and Intelligent Systems",
            "AI100 - Stanford One Hundred Year Study on Artificial Intelligence",
            "WIPO - World Intellectual Property Organization AI Patent Analytics",
            "CDEI - Centre for Data Ethics and Innovation",
            "UN AI - United Nations Artificial Intelligence",
            "ITU AI - International Telecommunication Union AI for Good",
            "CAHAI - Council of Europe Ad Hoc Committee on Artificial Intelligence",
            "ELLIS - European Laboratory for Learning and Intelligent Systems",
            "AI INDEX - Stanford AI Index Annual Report",
            "CGAI - Canadian Global Affairs Institute AI Policy",
            "JAII - Japan Artificial Intelligence Industrial Initiative",
            "UKRI - UK Research and Innovation AI Roadmap",
            "BAAI - Beijing Academy of Artificial Intelligence",
            "AIDP - AI Development Playbook",
            "MLAI - Machine Learning Artificial Intelligence Research",
            "IAIA - International Association for Impact Assessment AI",
            "McKinsey GI - McKinsey Global Institute AI Analysis",
            "Statista AI - Statista Artificial Intelligence Statistics Portal",
            "NSCAI - National Security Commission on Artificial Intelligence",
            "IMF AI - International Monetary Fund AI Economic Impact Analysis",
            "WB DITE - World Bank Digital Economy for Africa Initiative",
            "UNDP AI - United Nations Development Programme AI Strategy",
            "NAII - National Artificial Intelligence Initiative",
            "CIFAR - Canadian Institute for Advanced Research AI Strategy",
            "OII - Oxford Internet Institute AI Ethics Framework",
            "CAIDP - Center for AI and Digital Policy",
            "GAIA - Global AI Action Alliance",
            "AIAAIC - AI, Algorithmic and Automation Incident and Controversy Repository",
            "IRCAI - International Research Centre on Artificial Intelligence",
            "MIT CSAIL - MIT Computer Science and Artificial Intelligence Laboratory",
            "MILA - Montreal Institute for Learning Algorithms",
            "UKAIC - UK AI Council",
            "CNAS AI - Center for a New American Security AI Security Initiative",
            "UNU AI - United Nations University Centre on AI and Data",
            "CLAIRE - Confederation of Laboratories for AI Research in Europe",
            "IIIM - Icelandic Institute for Intelligent Machines",
            "DTI AI - Digital Transformation Institute AI Research",
            "SAIL - Stanford Artificial Intelligence Laboratory",
            "KAUST AI - King Abdullah University of Science and Technology AI Initiative",
            "AIA - AI Alignment Archive",
            "ILPC - Institute of Leadership & Public Policy AI Governance",
            "ASEAN AI - Association of Southeast Asian Nations AI Consortium",
            "JAIC - Joint Artificial Intelligence Center",
            "AISC - Artificial Intelligence Standards Committee"
        ]
        
        # Define clear boundaries for the two sections
        left_section_width = FRAME_WIDTH * 0.55  # Width of the left section for text
        right_section_width = FRAME_WIDTH * 0.45  # Width of the right section for QR code
        
        # Horizontal position for text (centered in left section)
        text_x_position = -right_section_width/2
        
        # Create text list aligned to the left side of screen
        text_group = VGroup()
        for source in sources:
            text = Text(source, font_size=20, color=WHITE)
            # Limit the width of the text to fit in left section
            max_text_width = left_section_width - 1  # Leave some margin
            if text.get_width() > max_text_width:
                text.set_width(max_text_width)
            text_group.add(text)
        
        # Arrange vertically with all text left-aligned
        text_group.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        
        # Position text group in left section and ensure full visibility
        text_group.move_to([text_x_position, 0, 0])
        text_group.to_edge(UP)
        
        # Ensure text doesn't get cut off on the left edge
        if text_group.get_left()[0] < -FRAME_WIDTH/2 + 0.5:
            text_group.shift(RIGHT * ((-FRAME_WIDTH/2 + 0.5) - text_group.get_left()[0]))
        
        # Load QR code image
        qr_code = ImageMobject("AISET.png")
        
        # Set QR code size and position it on the right
        qr_code.height = 4
        qr_code.move_to([FRAME_WIDTH/4, 0, 0])  # Position in right section
        
        # Create a background rectangle for the QR code to ensure no text overlap
        qr_background = Rectangle(
            width=qr_code.get_width() + 1,
            height=qr_code.get_height() + 1,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0
        )
        qr_background.move_to(qr_code.get_center())
        
        # Add a title for the QR code
        qr_title = Text("Scan for Resources", font_size=24, color=YELLOW)
        qr_title.next_to(qr_code, UP, buff=0.5)
        
        # Add elements in the correct order to ensure proper visibility
        self.add(qr_background, text_group, qr_code, qr_title)
        
        # Ensure all of the text is visible by starting it lower and scrolling it completely through
        self.play(
            text_group.animate.shift(UP * (text_group.get_height() + FRAME_HEIGHT)),
            rate_func=linear,
            run_time=16
        )
