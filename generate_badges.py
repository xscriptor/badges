import json
import os
import re
import itertools

def parse_palettes(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    palettes = {}
    
    # Split by headers
    sections = re.split(r'^##\s+(.+)$', content, flags=re.MULTILINE)
    
    current_name = None
    for section in sections:
        section = section.strip()
        if not section:
            continue
            
        if '\n' not in section and len(section) < 50: # Likely a name
            current_name = section
        else:
            # Look for json block
            match = re.search(r'```json\s*(\{.*?\})\s*```', section, re.DOTALL)
            if match and current_name:
                try:
                    color_data = json.loads(match.group(1))
                    palettes[current_name] = color_data
                    current_name = None # Reset
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for {current_name}: {e}")
            elif current_name:
                 pass
                 
    return palettes

def create_badge(text, bg_color, output_path, icon_type="terminal"):
    # Style configuration
    # bg_left is the vibrant color passed in
    bg_left = bg_color
    # bg_right is the text background - using dark hex matching the theme
    bg_right = "#161b22" 
    text_color = "#ffffff"
    
    # SVG Dimensions
    height = 28
    font_size = 14
    char_width = 8.5 # slightly adjusted
    text_width_approx = len(text) * char_width + 20
    
    icon_width = 35 # slightly wider for prompt
    total_width = icon_width + text_width_approx
    
    # Icon selection
    icon_svg = ""
    if icon_type == "terminal":
        # Terminal icon >_ or specific
        lower_text = text.lower()
        
        # Default
        icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="monospace" fill="{text_color}">&gt;_</text>'

        if "kitty" in lower_text:
             # Cat face
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 6})">
                <path d="M1,6 L1,10 C1,14 4,16 8,16 C12,16 15,14 15,10 L15,6 L13,1 L11,4 L5,4 L3,1 Z" fill="{text_color}"/>
             </g>
             '''
        elif "ghostty" in lower_text:
             # Ghost
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 8})">
                <path d="M7,0 C3,0 0,3 0,7 L0,16 L3,14 L7,16 L11,14 L14,16 L14,7 C14,3 11,0 7,0 Z" fill="{text_color}"/>
                <circle cx="5" cy="6" r="1.5" fill="{bg_left}"/>
                <circle cx="9" cy="6" r="1.5" fill="{bg_left}"/>
             </g>
             '''
        elif "wezterm" in lower_text:
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="14" fill="{text_color}">W</text>'
        elif "alacritty" in lower_text:
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="14" fill="{text_color}">A</text>'
        elif "hyper" in lower_text:
             # Bolt
             icon_content = f'''
             <g transform="translate({icon_width/2 - 5}, {height/2 - 8})">
                <path d="M6,0 L0,9 L4,9 L2,16 L10,6 L5,6 Z" fill="{text_color}"/>
             </g>
             '''
        elif "gnome" in lower_text:
             # Footprint shapeish or screen
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 7})">
                <rect x="0" y="0" width="16" height="12" rx="2" fill="{text_color}"/>
                <path d="M2,14 L14,14 L12,12 L4,12 Z" fill="{text_color}"/>
             </g>
             '''
        
        icon_svg = icon_content

    elif icon_type == "social":
        # Social icon @ or specific
        lower_text = text.lower()
        
        # Default
        icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" fill="{text_color}">@</text>'

        if "github" in lower_text:
             # Octocat silhouette
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <path d="M8,0 C3.6,0 0,3.6 0,8 C0,11.5 2.3,14.5 5.5,15.6 C5.9,15.7 6,15.4 6,15.2 L6,13.8 C3.8,14.3 3.3,12.7 3.3,12.7 C2.9,11.8 2.4,11.6 2.4,11.6 C1.7,11.1 2.5,11.1 2.5,11.1 C3.3,11.2 3.7,11.9 3.7,11.9 C4.4,13.1 5.5,12.8 6,12.6 C6.1,12.1 6.3,11.7 6.5,11.5 C4.7,11.3 2.9,10.6 2.9,7.5 C2.9,6.6 3.2,5.9 3.8,5.3 C3.7,5.1 3.4,4.2 3.9,3.1 C3.9,3.1 4.6,2.9 6.1,3.9 C6.7,3.7 7.4,3.6 8,3.6 C8.6,3.6 9.3,3.7 9.9,3.9 C11.4,2.9 12.1,3.1 12.1,3.1 C12.6,4.2 12.3,5.1 12.2,5.3 C12.8,5.9 13.1,6.6 13.1,7.5 C13.1,10.6 11.2,11.3 9.5,11.5 C9.8,11.8 10,12.3 10,13 L10,15.2 C10,15.4 10.1,15.7 10.5,15.6 C13.7,14.5 16,11.5 16,8 C16,3.6 12.4,0 8,0 Z" fill="{text_color}"/>
             </g>
             '''
        elif "twitter" in lower_text:
             # Bird
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 7})">
                 <path d="M16,3 C15.4,3.3 14.8,3.5 14.1,3.6 C14.8,3.2 15.3,2.5 15.5,1.7 C14.9,2.1 14.2,2.3 13.5,2.4 C12.9,1.8 12,1.4 11.1,1.4 C9.3,1.4 7.9,2.9 7.9,4.7 C7.9,5 7.9,5.2 8,5.5 C5.3,5.4 2.8,4.1 1.2,2.1 C0.9,2.6 0.7,3.2 0.7,3.8 C0.7,5 1.3,6 2.2,6.6 C1.7,6.6 1.2,6.4 0.7,6.2 L0.7,6.2 C0.7,7.8 1.9,9.1 3.4,9.4 C3.1,9.5 2.8,9.5 2.5,9.5 C2.3,9.5 2.1,9.5 1.9,9.5 C2.3,10.8 3.5,11.8 5,11.8 C3.8,12.7 2.3,13.3 0.6,13.3 C0.3,13.3 0,13.3 0,13.3 C1.6,14.3 3.5,14.9 5.5,14.9 C12.1,14.9 15.7,9.4 15.7,4.6 L15.7,4.2 C16.4,3.6 17,2.9 17.5,2.1 L16,3 Z" fill="{text_color}" transform="scale(0.9)"/>
             </g>
             '''
        elif "youtube" in lower_text:
             # Play button
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 6})">
                <rect x="0" y="0" width="16" height="12" rx="4" fill="{text_color}"/>
                <path d="M6,3 L11,6 L6,9 Z" fill="{bg_left}"/>
             </g>
             '''
        elif "discord" in lower_text:
             # Controller / face
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 6})">
                 <path d="M13.5,0 C12.4,0 11.4,0 11.4,0 C11.4,0 10,1.7 10,1.7 L6,1.7 C6,1.7 4.6,0 4.6,0 C4.6,0 3.6,0 2.5,0 C0.5,0.2 0,2 0,2 L0,9 C0,11 1.5,12 1.5,12 L4,9 L12,9 L14.5,12 C14.5,12 16,11 16,9 L16,2 C16,2 15.5,0.2 13.5,0 Z M5,7 C4.2,7 3.5,6.3 3.5,5.5 C3.5,4.7 4.2,4 5,4 C5.8,4 6.5,4.7 6.5,5.5 C6.5,6.3 5.8,7 5,7 Z M11,7 C10.2,7 9.5,6.3 9.5,5.5 C9.5,4.7 10.2,4 11,4 C11.8,4 12.5,4.7 12.5,5.5 C12.5,6.3 11.8,7 11,7 Z" fill="{text_color}"/>
             </g>
             '''
        elif "reddit" in lower_text:
             # Just circle + features or text
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                <circle cx="7" cy="7" r="7" fill="{text_color}"/>
                <circle cx="4.5" cy="6" r="1.5" fill="{bg_left}"/>
                <circle cx="9.5" cy="6" r="1.5" fill="{bg_left}"/>
                <path d="M4,10 Q7,12 10,10" stroke="{bg_left}" stroke-width="1.5" fill="none"/>
             </g>
             '''
        elif "linkedin" in lower_text:
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="14" fill="{text_color}">in</text>'
        
        elif "x" == lower_text:
             # X logo
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="14" fill="{text_color}">X</text>'
        
        elif "telegram" in lower_text:
              # Paper plane
              icon_content = f'''
              <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                 <path d="M0,7 L14,0 L11,14 L8,8 Z" fill="{text_color}"/>
              </g>
              '''
        elif "stack-overflow" in lower_text:
              # Stack
              icon_content = f'''
              <g transform="translate({icon_width/2 - 6}, {height/2 - 7})">
                 <path d="M0,10 L12,10 L12,14 L0,14 Z M0,10 L0,14" fill="{text_color}"/>
                 <rect x="2" y="10" width="8" height="2" fill="{text_color}"/>
                 <rect x="2" y="6" width="8" height="2" fill="{text_color}" transform="rotate(10 6 7)"/>
                 <rect x="4" y="2" width="8" height="2" fill="{text_color}" transform="rotate(25 8 3)"/>
              </g>
              '''

        icon_svg = icon_content

    elif icon_type == "software":
        # Software icon {} or specific
        lower_text = text.lower()
        
        # Default
        icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="monospace" fill="{text_color}">{{}}</text>'
        
        if "docker" in lower_text:
            # Whale shape
            icon_content = f'''
            <g transform="translate({icon_width/2 - 9}, {height/2 - 6})">
                <path d="M1,7 C1,7 3,12 9,12 C15,12 17,9 18,7 L18,5 L5,5 L5,3 L3,3 L3,5 L1,5 Z" fill="{text_color}"/>
                <rect x="5" y="1" width="2" height="2" fill="{text_color}"/>
                <rect x="8" y="1" width="2" height="2" fill="{text_color}"/>
                <rect x="5" y="3" width="2" height="2" fill="{text_color}"/>
                <rect x="8" y="3" width="2" height="2" fill="{text_color}"/>
                <rect x="11" y="3" width="2" height="2" fill="{text_color}"/>
            </g>
            '''
        elif "kubernetes" in lower_text:
            # Wheel
            icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="14" fill="{text_color}">K8s</text>'
        elif "linux" in lower_text:
            # Penguin (Tux) silhouette
            icon_content = f'''
            <g transform="translate({icon_width/2 - 7}, {height/2 - 8})">
                <path d="M7,0 C4,0 3,3 3,5 L1,8 L3,14 L6,16 L8,16 L11,14 L13,8 L11,5 C11,3 10,0 7,0 Z" fill="{text_color}"/>
                <path d="M5,4 C5,4 6,5 8,5 C10,5 11,4 11,4" stroke="{bg_left}" stroke-width="0.5" fill="none"/>
                <circle cx="5" cy="3" r="1" fill="{bg_left}"/>
                <circle cx="9" cy="3" r="1" fill="{bg_left}"/>
                <path d="M5,7 C5,7 6,14 8,14 C10,14 11,7 11,7" fill="{bg_left}"/>
            </g>
            '''
        elif "git" in lower_text and not "hub" in lower_text and not "lab" in lower_text:
             # Git branch
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                 <circle cx="3" cy="3" r="2" fill="{text_color}"/>
                 <circle cx="11" cy="3" r="2" fill="{text_color}"/>
                 <circle cx="7" cy="11" r="2" fill="{text_color}"/>
                 <path d="M3,3 L7,11 L11,3" stroke="{text_color}" stroke-width="2" fill="none"/>
             </g>
             '''
        elif "vim" in lower_text or "neovim" in lower_text:
             # V shape
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                <path d="M1,3 L5,13 L13,3 L9,3 L5,10 L5,3 Z" fill="{text_color}"/>
             </g>
             '''
        elif "code" in lower_text or "vscode" in lower_text:
             # Blue ribbon shape
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                <path d="M10,0 L12,2 L3,8 L12,14 L10,16 L0,8 Z" fill="{text_color}"/>
                <path d="M10,12 L6,8 L10,4" fill="{bg_left}"/>
             </g>
             '''
        elif "android" in lower_text:
             # Android head
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 6})">
                <path d="M1,6 L1,8 C1,11 3,13 7,13 C11,13 13,11 13,8 L13,6 Z" fill="{text_color}"/>
                <path d="M3,4 L1,1 M11,4 L13,1" stroke="{text_color}" stroke-width="1.5"/>
             </g>
             '''
             
        elif "xfetch" in lower_text:
            # Custom prompt icon for user tools
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="monospace" fill="{text_color}">&gt;</text>'
        elif "xtop" in lower_text:
            # Bar chart
             icon_content = f'''
             <g transform="translate({icon_width/2 - 6}, {height/2 - 6})">
                <rect x="0" y="8" width="3" height="4" fill="{text_color}"/>
                <rect x="4" y="4" width="3" height="8" fill="{text_color}"/>
                <rect x="8" y="0" width="3" height="12" fill="{text_color}"/>
             </g>
             '''

        icon_svg = icon_content
    elif icon_type == "languages":
        # Languages icon logic
        # Helper to create path icons
        
        # Default text icon
        icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="monospace" fill="{text_color}">&lt;/&gt;</text>'
        
        lower_text = text.lower()
        
        # Python: Stylized Snake (Two Snakes)
        if lower_text == "python":
            # Top snake and Bottom snake
            # Simplified geometric representation
            icon_content = f'''
            <g transform="translate({icon_width/2 - 8}, {height/2 - 8}) scale(0.8)">
                <!-- Top Snake -->
                <path d="M10,0 C13,0 16,1 16,4 L16,7 L13,7 L13,2 L5,2 L5,11 L8,11 L8,15 L0,15 L0,5 C0,1 3,0 6,0 L10,0 Z" fill="{text_color}"/>
                <rect x="11" y="1" width="2" height="2" fill="{bg_left}"/>
                
                <!-- Bottom Snake -->
                <path d="M10,20 C7,20 4,19 4,16 L4,13 L7,13 L7,18 L15,18 L15,9 L12,9 L12,5 L20,5 L20,15 C20,19 17,20 14,20 L10,20 Z" fill="{text_color}"/>
                <rect x="7" y="17" width="2" height="2" fill="{bg_left}"/>
            </g>
            '''
            
        # Java: Coffee Cup
        elif lower_text == "java":
            icon_content = f'''
            <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <!-- Cup -->
                <path d="M2,6 L2,12 C2,14 4,16 6,16 L10,16 C12,16 14,14 14,12 L14,6 Z" fill="{text_color}"/>
                <!-- Handle -->
                <path d="M14,8 L16,8 C17,8 17,11 16,11 L14,11" stroke="{text_color}" stroke-width="2" fill="none"/>
                <!-- Steam -->
                <path d="M4,2 Q5,1 4,4 M8,1 Q9,2 8,4 M12,2 Q13,1 12,4" stroke="{text_color}" stroke-width="1.5" fill="none"/>
            </g>
            '''

        # Database/SQL: Cylinder
        elif "sql" in lower_text or lower_text == "database":
            icon_content = f'''
            <g transform="translate({icon_width/2 - 6}, {height/2 - 7})">
                <ellipse cx="6" cy="2" rx="6" ry="2" stroke="{text_color}" stroke-width="1.5" fill="none"/>
                <path d="M0,2 v8 a6,2 0 0,0 12,0 v-8" stroke="{text_color}" stroke-width="1.5" fill="none"/>
                <path d="M0,6 a6,2 0 0,0 12,0" stroke="{text_color}" stroke-width="1.5" fill="none"/>
            </g>
            '''

        # PHP: Text
        elif lower_text == "php":
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 4}" font-weight="900" font-family="sans-serif" font-size="11" fill="{text_color}">php</text>'
             
        # Ruby: Diamond shape
        elif lower_text == "ruby":
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                 <path d="M4,0 L10,0 L14,5 L7,14 L0,5 Z" fill="{text_color}" />
                 <path d="M4,0 L7,5 M10,0 L7,5 M0,5 L14,5" stroke="{bg_left}" stroke-width="0.5"/>
             </g>
             '''

        # GO: Text
        elif lower_text == "go":
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="12" fill="{text_color}">GO</text>'

        # Rust: Gear
        elif lower_text == "rust":
             # Simple gear
             icon_content = f'''
             <g transform="translate({icon_width/2}, {height/2})">
                 <circle r="4" fill="none" stroke="{text_color}" stroke-width="2.5" stroke-dasharray="3,1.5" />
                 <circle r="6" fill="none" stroke="{text_color}" stroke-width="1.5" />
             </g>
             '''
             
        # C / C++ / C#: Text
        elif lower_text in ["c", "cpp", "c++", "csharp", "c#"]:
             disp = "C"
             if "pp" in lower_text or "++" in lower_text: disp = "C++"
             elif "#" in lower_text or "sharp" in lower_text: disp = "C#"
             size = "12" if len(disp) > 1 else "14"
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="{size}" fill="{text_color}">{disp}</text>'
             
        # JS/TS
        elif lower_text in ["javascript", "typescript", "js", "ts"]:
             disp = "JS"
             if "type" in lower_text or "ts" in lower_text: disp = "TS"
             # Square box style typical of JS/TS logos
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <rect width="16" height="16" rx="2" fill="{text_color}" />
                <text x="8" y="13" text-anchor="middle" font-weight="bold" font-family="sans-serif" font-size="10" fill="{bg_left}">{disp}</text>
             </g>
             '''

        # Shell/Terminal
        elif lower_text in ["shell", "bash", "zsh", "powershell", "terminal", "sh"]:
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="monospace" fill="{text_color}">&gt;_</text>'

        # Lua: Moon with Hole/Orbit
        elif lower_text == "lua":
             # Crescent moon with a dot
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                 <!-- Moon -->
                <path d="M10,0 A7,7 0 1,1 3,12 A7,7 0 0,0 10,0 Z" fill="{text_color}"/>
                <!-- Hole/Dot representing the planet/orbit -->
                <circle cx="10" cy="4" r="2" fill="{text_color}"/>
             </g>
             '''
             
        # Swift: Bird (Simplified)
        elif lower_text == "swift":
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 6})">
                <path d="M0,8 Q5,0 16,0 Q10,5 16,8 Q5,14 0,8" fill="{text_color}"/>
             </g>
             '''
             
        # HTML/CSS: Shield or Number
        elif lower_text == "html":
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="14" fill="{text_color}">5</text>'
        elif lower_text == "css":
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="14" fill="{text_color}">3</text>'
             
        icon_svg = icon_content
    elif icon_type == "frameworks":
        # Frameworks icon logic
        lower_text = text.lower()
        
        # Default: Stack icon
        icon_content = f'''
        <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
           <path d="M8,1 L15,4 L8,7 L1,4 L8,1 Z M1,8 L8,11 L15,8 M1,12 L8,15 L15,12" stroke="{text_color}" stroke-width="1.5" fill="none"/>
        </g>
        '''
        
        if "react" in lower_text:
            # React Atom (Simplified)
            icon_content = f'''
            <g transform="translate({icon_width/2}, {height/2}) scale(0.9)">
                <circle r="2" fill="{text_color}"/>
                <ellipse rx="9" ry="3" stroke="{text_color}" stroke-width="1" fill="none" transform="rotate(0)"/>
                <ellipse rx="9" ry="3" stroke="{text_color}" stroke-width="1" fill="none" transform="rotate(60)"/>
                <ellipse rx="9" ry="3" stroke="{text_color}" stroke-width="1" fill="none" transform="rotate(120)"/>
            </g>
            '''
        elif "vue" in lower_text:
             # Vue V
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 7})">
                <path d="M0,0 L8,14 L16,0 M3,0 L8,8 L13,0" stroke="{text_color}" stroke-width="2" fill="none"/>
             </g>
             '''
        elif "angular" in lower_text:
             # Shield A
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 8})">
                <path d="M7,0 L14,3 L14,11 L7,16 L0,11 L0,3 Z" stroke="{text_color}" stroke-width="1.5" fill="none"/>
                <text x="7" y="11" text-anchor="middle" font-weight="bold" font-family="sans-serif" font-size="10" fill="{text_color}">A</text>
             </g>
             '''
        elif lower_text == "svelte":
             # S shape
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="14" fill="{text_color}">S</text>'
        
        elif "django" in lower_text:
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 4}" font-weight="bold" font-family="sans-serif" font-size="11" fill="{text_color}">dj</text>'
             
        elif "flask" in lower_text:
             # Flask bottle
             icon_content = f'''
             <g transform="translate({icon_width/2 - 6}, {height/2 - 8})">
                <path d="M4,0 L8,0 L9,4 L12,14 C12,15 11,16 6,16 C1,16 0,15 0,14 L3,4 Z" stroke="{text_color}" stroke-width="1.5" fill="none"/>
             </g>
             '''
        
        elif "spring" in lower_text:
              # Leaf
              icon_content = f'''
              <g transform="translate({icon_width/2 - 6}, {height/2 - 8})">
                 <path d="M6,16 Q6,8 12,0 Q0,4 6,16" stroke="{text_color}" stroke-width="1.5" fill="none"/>
              </g>
              '''
              
        elif "laravel" in lower_text:
              # L
               icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="14" fill="{text_color}">L</text>'
               
        elif "tailwind" in lower_text:
              # Wave
              icon_content = f'''
              <g transform="translate({icon_width/2 - 8}, {height/2 - 4})">
                 <path d="M0,4 Q4,0 8,4 T16,4" stroke="{text_color}" stroke-width="2" fill="none"/>
              </g>
              '''
        elif "bootstrap" in lower_text:
               icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="14" fill="{text_color}">B</text>'
        
        elif "next" in lower_text:
               icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="14" fill="{text_color}">N</text>'
               
        elif "dotnet" in lower_text:
                icon_content = f'<text x="{icon_width/2}" y="{height/2 + 4}" font-weight="bold" font-family="sans-serif" font-size="10" fill="{text_color}">.NET</text>'

        icon_svg = icon_content
    elif icon_type == "ide":
        # IDE icon logic
        lower_text = text.lower()
        
        # Default: Box with I
        icon_content = f'''
        <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
           <rect x="0" y="0" width="16" height="16" rx="2" fill="{text_color}"/>
           <text x="8" y="13" text-anchor="middle" font-weight="bold" font-family="sans-serif" font-size="10" fill="{bg_left}">I</text>
        </g>
        '''
        
        if "intellij" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <rect x="0" y="0" width="16" height="16" rx="2" fill="{text_color}"/>
                <text x="8" y="13" text-anchor="middle" font-weight="bold" font-family="sans-serif" font-size="10" fill="{bg_left}">IJ</text>
             </g>
             '''
        elif "pycharm" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <rect x="0" y="0" width="16" height="16" rx="2" fill="{text_color}"/>
                <text x="8" y="13" text-anchor="middle" font-weight="bold" font-family="sans-serif" font-size="10" fill="{bg_left}">PC</text>
             </g>
             '''
        elif "webstorm" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <rect x="0" y="0" width="16" height="16" rx="2" fill="{text_color}"/>
                <text x="8" y="13" text-anchor="middle" font-weight="bold" font-family="sans-serif" font-size="10" fill="{bg_left}">WS</text>
             </g>
             '''
        elif "goland" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <rect x="0" y="0" width="16" height="16" rx="2" fill="{text_color}"/>
                <text x="8" y="13" text-anchor="middle" font-weight="bold" font-family="sans-serif" font-size="10" fill="{bg_left}">GO</text>
             </g>
             '''
        elif "rider" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <rect x="0" y="0" width="16" height="16" rx="2" fill="{text_color}"/>
                <text x="8" y="13" text-anchor="middle" font-weight="bold" font-family="sans-serif" font-size="10" fill="{bg_left}">RD</text>
             </g>
             '''
        elif "clion" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <rect x="0" y="0" width="16" height="16" rx="2" fill="{text_color}"/>
                <text x="8" y="13" text-anchor="middle" font-weight="bold" font-family="sans-serif" font-size="10" fill="{bg_left}">CL</text>
             </g>
             '''
        elif "eclipse" in lower_text:
             # Sun/Circle
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <circle cx="8" cy="8" r="7" fill="{text_color}"/>
                <circle cx="6" cy="6" r="7" fill="{bg_left}"/>
             </g>
             '''
        elif "xcode" in lower_text:
             # Hammer/A
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <path d="M8,1 L14,14 L8,11 L2,14 L8,1 Z" fill="{text_color}"/>
                <path d="M6,6 L10,6" stroke="{bg_left}" stroke-width="1"/>
             </g>
             '''
        elif "visual-studio" in lower_text:
             # Infinity/Ribbon
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <path d="M2,2 L8,9 L2,16 L2,2 Z M14,2 L8,9 L14,16 L14,2 Z" fill="{text_color}"/>
             </g>
             '''
        elif "antigravity" in lower_text:
             # Antigravity (Google / AG)
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <!-- G Shape -->
                <path d="M15,8 L8,8 L8,10 L13,10 C12.5,13 10.5,14 8,14 C5,14 3,11.5 3,8 C3,4.5 5,2 8,2 C10,2 11,3 12,4" stroke="{text_color}" stroke-width="1.5" fill="none"/>
                <!-- Orbital dot -->
                <circle cx="14" cy="2" r="1.5" fill="{bg_left}"/>
             </g>
             '''
        elif "trae" in lower_text:
             # Trae AI - Stylized T / Geometric
             # Abstract minimalist shape based on Trae branding
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <path d="M2,2 L14,2 L14,5 L9.5,5 L9.5,14 L6.5,14 L6.5,5 L2,5 Z" fill="{text_color}"/>
                <circle cx="8" cy="10" r="1.5" fill="{bg_left}"/>
                <path d="M8,10 L14,14 M8,10 L2,14" stroke="{bg_left}" stroke-width="0.5" opacity="0.8"/>
             </g>
             '''
             
        icon_svg = icon_content

    elif icon_type == "editors":
        # Text Editor icon logic
        lower_text = text.lower()
        
        # Default: Edit Icon
        icon_content = f'''
        <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
           <path d="M3,12 L12,3 L15,6 L6,15 L2,16 L3,12 Z" fill="{text_color}"/>
        </g>
        '''
        
        if "vscode" in lower_text or "code" in lower_text or "codium" in lower_text:
             # Blue ribbon shape
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                <path d="M10,0 L12,2 L3,8 L12,14 L10,16 L0,8 Z" fill="{text_color}"/>
                <path d="M10,12 L6,8 L10,4" fill="{bg_left}"/>
             </g>
             '''
        elif "vim" in lower_text or "neovim" in lower_text:
             # V shape
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                <path d="M1,3 L5,13 L13,3 L9,3 L5,10 L5,3 Z" fill="{text_color}"/>
             </g>
             '''
        elif "sublime" in lower_text:
             # S box
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <rect x="0" y="0" width="16" height="16" fill="{text_color}"/>
                <path d="M8,4 L12,8 L8,12 L4,8 Z" fill="{bg_left}"/>
             </g>
             '''
        elif "atom" in lower_text:
             # Atom ellipse
             icon_content = f'''
             <g transform="translate({icon_width/2}, {height/2})">
                <circle r="2" fill="{text_color}"/>
                <ellipse rx="8" ry="3" stroke="{text_color}" stroke-width="1" fill="none" transform="rotate(20)"/>
                <ellipse rx="8" ry="3" stroke="{text_color}" stroke-width="1" fill="none" transform="rotate(-20)"/>
                <circle cx="0" cy="-6" r="1" fill="{text_color}"/>
             </g>
             '''
        elif "notepad" in lower_text:
             # Note
             icon_content = f'''
             <g transform="translate({icon_width/2 - 6}, {height/2 - 8})">
                <rect x="1" y="1" width="10" height="14" fill="{text_color}"/>
                <path d="M3,4 L9,4 M3,8 L9,8 M3,12 L7,12" stroke="{bg_left}" stroke-width="1"/>
                <text x="8" y="11" font-size="8" fill="{bg_left}" font-weight="bold">+</text>
             </g>
             '''
        elif "emacs" in lower_text:
             # E stroke
             icon_content = f'''
             <g transform="translate({icon_width/2 - 6}, {height/2 - 7})">
                <text x="6" y="12" text-anchor="middle" font-weight="bold" font-family="sans-serif" font-size="14" fill="{text_color}">E</text>
             </g>
             '''
        elif "nano" in lower_text:
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="12" fill="{text_color}">N</text>'
             
        elif "cursor" in lower_text:
             # Cursor Arrow
             icon_content = f'''
             <g transform="translate({icon_width/2 - 6}, {height/2 - 8})">
                <path d="M0,0 L12,6 L6,8 L8,12 L4,13 L2,9 L0,11 Z" fill="{text_color}"/>
             </g>
             '''

        icon_svg = icon_content

    elif icon_type == "browsers":
         lower_text = text.lower()
         # Default: Globe
         icon_content = f'''
         <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
            <circle cx="8" cy="8" r="7" stroke="{text_color}" stroke-width="1.5" fill="none"/>
            <path d="M1,8 L15,8 M8,1 L8,15 M2,5 Q8,10 14,5 M2,11 Q8,6 14,11" stroke="{text_color}" stroke-width="1" fill="none"/>
         </g>
         '''
         if "chrome" in lower_text or "chromium" in lower_text:
             # Circle with dot
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                 <circle cx="8" cy="8" r="7" stroke="{text_color}" stroke-width="2" fill="none"/>
                 <circle cx="8" cy="8" r="3" fill="{bg_left}"/>
             </g>
             '''
         elif "firefox" in lower_text:
             # Fox tailish
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <path d="M8,16 C4,16 1,12 1,8 C1,5 3,2 6,1 C4,3 4,5 5,7 C7,4 11,2 13,4 C14,6 15,9 13,12 C12,15 10,16 8,16 Z" fill="{text_color}"/>
             </g>
             '''
         elif "safari" in lower_text:
             # Compass
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <circle cx="8" cy="8" r="7" stroke="{text_color}" stroke-width="1.5" fill="none"/>
                <path d="M8,2 L9,7 L14,8 L9,9 L8,14 L7,9 L2,8 L7,7 Z" fill="{text_color}"/>
             </g>
             '''
         elif "edge" in lower_text:
             # E wave
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <path d="M8,8 C4,8 4,14 8,14 L14,10 M14,2 C10,2 6,4 6,8" stroke="{text_color}" stroke-width="2" fill="none"/>
             </g>
             '''
         
         icon_svg = icon_content

    elif icon_type == "cloud":
         lower_text = text.lower()
         # Cloud shape default
         icon_content = f'''
         <g transform="translate({icon_width/2 - 8}, {height/2 - 6})">
            <path d="M4,12 C1,12 0,10 0,8 C0,6 2,5 2,5 C2,2 5,0 8,0 C11,0 13,2 13,4 C15,4 16,6 16,8 C16,11 14,12 12,12 Z" fill="{text_color}"/>
         </g>
         '''
         if "aws" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 6})">
                 <path d="M10,2 L12,4 L12,8 L2,8 L2,5 L5,2 Z M2,8 L2,10 L10,10" stroke="{text_color}" stroke-width="1.5" fill="none"/>
                 <path d="M4,12 Q7,14 10,12" stroke="{bg_left}" stroke-width="1.5" fill="none"/>
             </g>
             '''
         elif "azure" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                 <path d="M1,14 L5,2 L10,10 L14,7" stroke="{text_color}" stroke-width="2" fill="none"/>
             </g>
             '''
         elif "gcp" in lower_text or "google" in lower_text:
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="12" fill="{text_color}">G</text>'
         elif "vercel" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 7})">
                <path d="M8,1 L15,13 L1,13 Z" fill="{text_color}"/> # Triangle
             </g>
             '''
         elif "netlify" in lower_text:
              icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 8})">
                <path d="M2,4 L8,14 L14,4 L8,8 Z" fill="{text_color}"/>
             </g>
             '''
         icon_svg = icon_content

    elif icon_type == "files":
         lower_text = text.lower()
         # File doc
         icon_content = f'''
         <g transform="translate({icon_width/2 - 6}, {height/2 - 8})">
            <path d="M1,0 L8,0 L12,4 L12,16 L1,16 Z" fill="{text_color}"/>
            <path d="M8,0 L8,4 L12,4" fill="{bg_left}"/>
         </g>
         '''
         if "json" in lower_text:
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 4}" font-weight="bold" font-family="sans-serif" font-size="8" fill="{text_color}">{{}}</text>'
         elif "xml" in lower_text or "html" in lower_text:
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 4}" font-weight="bold" font-family="monospace" font-size="8" fill="{text_color}">&lt;&gt;</text>'
         elif "pdf" in lower_text:
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 4}" font-weight="bold" font-family="sans-serif" font-size="8" fill="{text_color}">PDF</text>'
         
         icon_svg = icon_content

    elif icon_type == "os":
         lower_text = text.lower()
         # Screen
         icon_content = f'''
         <g transform="translate({icon_width/2 - 8}, {height/2 - 7})">
             <rect x="0" y="0" width="16" height="11" rx="1" fill="{text_color}"/>
             <rect x="5" y="12" width="6" height="2" fill="{text_color}"/>
         </g>
         '''
         if "windows" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                <path d="M0,2 L6,1 L6,7 L0,7 Z M7,1 L14,0 L14,7 L7,7 Z M0,8 L6,8 L6,14 L0,13 Z M7,8 L14,8 L14,15 L7,14 Z" fill="{text_color}"/>
             </g>
             '''
         elif "apple" in lower_text or "macos" in lower_text or "ios" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 6}, {height/2 - 7})">
                <circle cx="6" cy="7" r="5" fill="{text_color}"/>
                <path d="M6,2 L6,0" stroke="{text_color}" stroke-width="2"/>
             </g>
             '''
         elif "linux" in lower_text:
             # Tux
            icon_content = f'''
            <g transform="translate({icon_width/2 - 7}, {height/2 - 8})">
                <path d="M7,0 C4,0 3,3 3,5 L1,8 L3,14 L6,16 L8,16 L11,14 L13,8 L11,5 C11,3 10,0 7,0 Z" fill="{text_color}"/>
                <path d="M5,4 C5,4 6,5 8,5 C10,5 11,4 11,4" stroke="{bg_left}" stroke-width="0.5" fill="none"/>
            </g>
            '''
         elif "android" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 6})">
                <path d="M1,6 L1,8 C1,11 3,13 7,13 C11,13 13,11 13,8 L13,6 Z" fill="{text_color}"/>
                <path d="M3,4 L1,1 M11,4 L13,1" stroke="{text_color}" stroke-width="1.5"/>
             </g>
             '''
         elif text.lower() == "x":
             # X Linux (Stylized X prompt)
             icon_content = f'''
             <g transform="translate({icon_width/2 - 6}, {height/2 - 6})">
                <path d="M2,2 L10,10 M10,2 L2,10" stroke="{text_color}" stroke-width="2.5" stroke-linecap="round"/>
                <rect x="0" y="0" width="12" height="12" fill="none" stroke="{text_color}" stroke-width="1" rx="1"/>
             </g>
             '''
         
         icon_svg = icon_content

    elif icon_type == "tools":
         lower_text = text.lower()
         # Wrench
         icon_content = f'''
         <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
             <path d="M14,0 L10,4 L11,7 L7,11 L4,10 L0,14" stroke="{text_color}" stroke-width="2"/>
         </g>
         '''
         if "docker" in lower_text:
            # Whale shape
            icon_content = f'''
            <g transform="translate({icon_width/2 - 9}, {height/2 - 6})">
                <path d="M1,7 C1,7 3,12 9,12 C15,12 17,9 18,7 L18,5 L5,5 L5,3 L3,3 L3,5 L1,5 Z" fill="{text_color}"/>
                <rect x="5" y="1" width="2" height="2" fill="{text_color}"/>
                <rect x="8" y="1" width="2" height="2" fill="{text_color}"/>
            </g>
            '''
         elif "kubernetes" in lower_text:
            icon_content = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" font-family="sans-serif" font-size="14" fill="{text_color}">K8s</text>'
         elif "git" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                 <circle cx="3" cy="3" r="2" fill="{text_color}"/>
                 <circle cx="11" cy="3" r="2" fill="{text_color}"/>
                 <circle cx="7" cy="11" r="2" fill="{text_color}"/>
                 <path d="M3,3 L7,11 L11,3" stroke="{text_color}" stroke-width="2" fill="none"/>
             </g>
             '''
         elif "npm" in lower_text:
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 4}" font-weight="bold" font-family="sans-serif" font-size="10" fill="{text_color}">NPM</text>'
             
         icon_svg = icon_content

    elif icon_type == "ai":
         lower_text = text.lower()
         # Brain/Sparkle
         icon_content = f'''
         <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
            <path d="M7,1 C4,1 2,4 2,7 C2,10 5,13 7,13 C9,13 12,10 12,7 C12,4 10,1 7,1 Z M7,3 C9,3 10,5 10,7 C10,9 9,11 7,11 C5,11 4,9 4,7 C4,5 5,3 7,3" stroke="{text_color}" stroke-width="1.5" fill="none"/>
            <path d="M7,5 L7,9 M5,7 L9,7" stroke="{text_color}" stroke-width="1.5"/>
         </g>
         '''
         if "openai" in lower_text or "chatgpt" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                <path d="M7,7 m-6,0 a6,6 0 1,0 12,0 a6,6 0 1,0 -12,0 M7,7 L7,1 M7,7 L12,10 M7,7 L2,10" stroke="{text_color}" stroke-width="1.5" fill="none"/>
             </g>
             '''
         
         icon_svg = icon_content

    elif icon_type == "design":
         lower_text = text.lower()
         # Pen tool / Palette
         icon_content = f'''
         <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
            <path d="M2,12 L6,12 L12,6 L8,2 L2,8 Z M3,11 L3,9" stroke="{text_color}" stroke-width="1.5" fill="none"/>
         </g>
         '''
         if "figma" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 6}, {height/2 - 8})">
                 <circle cx="3" cy="3" r="3" fill="{text_color}"/>
                 <circle cx="9" cy="3" r="3" fill="{text_color}"/>
                 <circle cx="3" cy="9" r="3" fill="{text_color}"/>
                 <circle cx="3" cy="15" r="3" fill="{text_color}"/>
                 <circle cx="9" cy="9" r="3" fill="{text_color}"/>
             </g>
             '''
         elif "photoshop" in lower_text:
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 4}" font-weight="bold" font-family="sans-serif" font-size="10" fill="{text_color}">Ps</text>'
         elif "illustrator" in lower_text:
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 4}" font-weight="bold" font-family="sans-serif" font-size="10" fill="{text_color}">Ai</text>'
         elif "sketch" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                 <path d="M3,1 L11,1 L14,6 L7,13 L0,6 Z" fill="{text_color}"/>
             </g>
             '''
         
         icon_svg = icon_content

    elif icon_type == "hardware":
         lower_text = text.lower()
         # Chip
         icon_content = f'''
         <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
            <rect x="2" y="2" width="10" height="10" fill="{text_color}"/>
            <path d="M2,4 L0,4 M2,7 L0,7 M2,10 L0,10 M4,2 L4,0 M7,2 L7,0 M10,2 L10,0 M12,4 L14,4 M12,7 L14,7 M12,10 L14,10 M4,12 L4,14 M7,12 L7,14 M10,12 L10,14" stroke="{text_color}" stroke-width="1.5"/>
         </g>
         '''
         if "apple" in lower_text:
              icon_content = f'<text x="{icon_width/2}" y="{height/2 + 4}" font-weight="bold" font-family="sans-serif" font-size="10" fill="{text_color}">M1</text>'
         
         icon_svg = icon_content

    elif icon_type == "licenses":
         lower_text = text.lower()
         # Scale / Key
         icon_content = f'''
         <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
             <circle cx="7" cy="7" r="6" stroke="{text_color}" stroke-width="1.5" fill="none"/>
             <text x="7" y="10" text-anchor="middle" font-weight="bold" font-family="sans-serif" font-size="8" fill="{text_color}">C</text>
         </g>
         '''
         if "mit" in lower_text:
              icon_content = f'<text x="{icon_width/2}" y="{height/2 + 4}" font-weight="bold" font-family="sans-serif" font-size="10" fill="{text_color}">MIT</text>'
         
         icon_svg = icon_content
    
    elif icon_type == "status":
         lower_text = text.lower()
         # Circle
         icon_content = f'''
         <g transform="translate({icon_width/2 - 5}, {height/2 - 5})">
            <circle cx="5" cy="5" r="5" fill="{text_color}"/>
         </g>
         '''
         if "passing" in lower_text or "stable" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 6}, {height/2 - 6})">
                <path d="M2,6 L5,10 L10,2" stroke="{text_color}" stroke-width="2" fill="none"/>
             </g>
             '''
         elif "failing" in lower_text or "deprecated" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 6}, {height/2 - 6})">
                <path d="M2,2 L10,10 M10,2 L2,10" stroke="{text_color}" stroke-width="2" fill="none"/>
             </g>
             '''
         
         icon_svg = icon_content

    elif icon_type == "gaming":
         lower_text = text.lower()
         # Gamepad
         icon_content = f'''
         <g transform="translate({icon_width/2 - 8}, {height/2 - 5})">
            <path d="M1,5 C1,2 3,1 5,1 L11,1 C13,1 15,2 15,5 C15,8 14,9 12,9 L10,9 L9,7 L7,7 L6,9 L4,9 C2,9 1,8 1,5 Z" fill="{text_color}"/>
            <circle cx="4" cy="5" r="1" fill="{bg_left}"/>
            <circle cx="12" cy="5" r="1" fill="{bg_left}"/>
         </g>
         '''
         if "steam" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                 <circle cx="7" cy="7" r="6" stroke="{text_color}" stroke-width="1.5" fill="none"/>
                 <path d="M7,1 L7,6 L3,10" stroke="{text_color}" stroke-width="1.5"/>
             </g>
             '''
         
         icon_svg = icon_content

    elif icon_type == "finance":
         lower_text = text.lower()
         # Dollar sign
         icon_content = f'''
         <g transform="translate({icon_width/2 - 6}, {height/2 - 7})">
             <path d="M6,1 L6,13 M3,3 L8,3 L8,6 L3,6 L3,10 L8,10" stroke="{text_color}" stroke-width="1.5" fill="none"/>
         </g>
         '''
         if "card" in lower_text or "mastercard" in lower_text or "visa" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 8}, {height/2 - 6})">
                <rect x="0" y="0" width="16" height="12" rx="2" fill="{text_color}"/>
                <line x1="0" y1="4" x2="16" y2="4" stroke="{bg_left}" stroke-width="2"/>
                <circle cx="12" cy="9" r="1.5" fill="{bg_left}"/>
             </g>
             '''
         elif "stripe" in lower_text:
             icon_content = f'<text x="{icon_width/2}" y="{height/2 + 4}" font-weight="bold" font-family="sans-serif" font-size="10" fill="{text_color}">S</text>'
         
         icon_svg = icon_content

    elif icon_type == "ci":
         lower_text = text.lower()
         # Gear / Cycle
         icon_content = f'''
         <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
             <path d="M7,2 A5,5 0 1,1 2,7" stroke="{text_color}" stroke-width="1.5" fill="none"/>
             <path d="M7,2 L9,4 M7,2 L5,4" stroke="{text_color}" stroke-width="1.5"/>
         </g>
         '''
         if "jenkins" in lower_text:
              icon_content = f'<text x="{icon_width/2}" y="{height/2 + 4}" font-weight="bold" font-family="sans-serif" font-size="10" fill="{text_color}">J</text>'
         elif "github" in lower_text:
              # Play button
              icon_content = f'''
              <g transform="translate({icon_width/2 - 5}, {height/2 - 6})">
                 <path d="M2,2 L10,6 L2,10 Z" fill="{text_color}"/>
              </g>
              '''
         
         icon_svg = icon_content

    elif icon_type == "crypto":
         lower_text = text.lower()
         # Coin
         icon_content = f'''
         <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
            <circle cx="7" cy="7" r="6" stroke="{text_color}" stroke-width="1.5" fill="none"/>
            <text x="7" y="10" text-anchor="middle" font-weight="bold" font-family="sans-serif" font-size="8" fill="{text_color}">₿</text>
         </g>
         '''
         if "ethereum" in lower_text:
             icon_content = f'''
             <g transform="translate({icon_width/2 - 6}, {height/2 - 8})">
                <path d="M6,0 L12,9 L6,16 L0,9 Z" fill="{text_color}"/>
             </g>
             '''
         
         icon_svg = icon_content

    elif icon_type == "analytics":
         lower_text = text.lower()
         # Bar chart
         icon_content = f'''
         <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
            <rect x="1" y="6" width="3" height="8" fill="{text_color}"/>
            <rect x="5" y="2" width="3" height="12" fill="{text_color}"/>
            <rect x="9" y="8" width="3" height="6" fill="{text_color}"/>
         </g>
         '''
         
         icon_svg = icon_content

    elif icon_type == "productivity":
         lower_text = text.lower()
         # Checkbox
         icon_content = f'''
         <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
             <rect x="1" y="1" width="12" height="12" rx="2" stroke="{text_color}" stroke-width="1.5" fill="none"/>
             <path d="M3,6 L6,9 L11,3" stroke="{text_color}" stroke-width="1.5" fill="none"/>
         </g>
         '''
         if "slack" in lower_text:
              icon_content = f'<text x="{icon_width/2}" y="{height/2 + 4}" font-weight="bold" font-family="sans-serif" font-size="10" fill="{text_color}">#</text>'
         
         icon_svg = icon_content

    elif icon_type == "misc":
         lower_text = text.lower()
         # Heart
         icon_content = f'''
         <g transform="translate({icon_width/2 - 7}, {height/2 - 6})">
            <path d="M7,13 L6,12 C2,8 0,6 0,4 C0,1 2,0 4,0 C5,0 6,1 7,2 C8,1 9,0 10,0 C12,0 14,1 14,4 C14,6 12,8 8,12 Z" fill="{text_color}"/>
         </g>
         '''
         if "sponsor" in lower_text:
              # Star
              icon_content = f'''
              <g transform="translate({icon_width/2 - 7}, {height/2 - 7})">
                 <path d="M7,1 L9,5 L13,6 L10,9 L11,13 L7,11 L3,13 L4,9 L1,6 L5,5 Z" fill="{text_color}"/>
              </g>
              '''
         
         icon_svg = icon_content

    elif icon_type == "desktops":
         lower_text = text.lower()
         # Tux (Penguin) for all desktop environments as requested
         icon_content = f'''
            <g transform="translate({icon_width/2 - 7}, {height/2 - 8})">
                <path d="M7,0 C4,0 3,3 3,5 L1,8 L3,14 L6,16 L8,16 L11,14 L13,8 L11,5 C11,3 10,0 7,0 Z" fill="{text_color}"/>
                <path d="M5,4 C5,4 6,5 8,5 C10,5 11,4 11,4" stroke="{bg_left}" stroke-width="0.5" fill="none"/>
            </g>
         '''
         
         icon_svg = icon_content

    else:
        # Fallback to X
        icon_svg = f'<text x="{icon_width/2}" y="{height/2 + 5}" font-weight="bold" fill="{text_color}">X</text>'
    
    # Middle X
    # Placed exactly at the boundary (x=icon_width)
    middle_x = f'<text x="{icon_width}" y="{height/2 + 5}" text-anchor="middle" font-weight="bold" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="{font_size}" fill="{text_color}">X</text>'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{height}" role="img" aria-label="{text}">
  <title>{text}</title>
  <g shape-rendering="crispEdges">
    <rect width="{icon_width}" height="{height}" fill="{bg_left}"/>
    <rect x="{icon_width}" width="{text_width_approx}" height="{height}" fill="{bg_right}"/>
  </g>
  <g fill="{text_color}" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="{font_size}">
    <!-- Icon area -->
    {icon_svg}
    
    <!-- Divider X -->
    {middle_x}
    
    <!-- Label -->
    <text x="{icon_width + text_width_approx/2}" y="{height/2 + 5}" font-weight="bold" fill="{text_color}">{text}</text>
  </g>
</svg>"""
    
    with open(output_path, 'w') as f:
        f.write(svg)

def generate_index_html():
    """Generates a modern index.html for GitHub Pages showcase."""
    
    # Collect all badges first
    all_categories = sorted(categories.keys())
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XScriptor Badges Collection</title>
    <style>
        :root {
            --bg-color: #0d1117;
            --card-bg: #161b22;
            --text-color: #c9d1d9;
            --accent-color: #58a6ff;
            --border-color: #30363d;
        }
        
        * { box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }
        
        header {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        h1 { margin: 0 0 10px; font-size: 2.5rem; background: linear-gradient(90deg, #58a6ff, #a371f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        p { margin: 0 0 20px; color: #8b949e; }
        
        .search-container {
            position: relative;
            max-width: 600px;
            margin: 0 auto;
        }
        
        #searchInput {
            width: 100%;
            padding: 12px 20px 12px 45px;
            font-size: 16px;
            background-color: #0d1117;
            border: 1px solid var(--border-color);
            border-radius: 50px;
            color: var(--text-color);
            outline: none;
            transition: all 0.2s ease;
        }
        
        #searchInput:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.3);
        }
        
        .search-icon {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            fill: #8b949e;
        }
        
        /* Main Container for Marquees */
        #marquee-view {
            padding: 40px 0;
            display: flex;
            flex-direction: column;
            gap: 40px;
        }
        
        .row-label {
            padding: 0 20px;
            margin-bottom: 10px;
            font-size: 1.2rem;
            color: var(--text-color);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.8;
            max-width: 1200px;
            margin: 0 auto 15px;
            display: block;
        }

        .marquee-container {
            position: relative;
            width: 100%;
            overflow: hidden;
            white-space: nowrap;
            mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent);
            -webkit-mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
        }
        
        .marquee-content {
            display: inline-flex;
            gap: 20px;
            will-change: transform;
        }
        
        /* Alternating animations */
        .marquee-left { animation: scrollLeft 40s linear infinite; }
        .marquee-right { animation: scrollRight 40s linear infinite; }
        
        .marquee-content:hover { animation-play-state: paused; }
        
        @keyframes scrollLeft {
            from { transform: translateX(0); }
            to { transform: translateX(-50%); }
        }
        
        @keyframes scrollRight {
            from { transform: translateX(-50%); }
            to { transform: translateX(0); }
        }
        
        .badge-item {
            cursor: pointer;
            transition: transform 0.2s;
            position: relative;
            display: flex;
            align-items: center;
        }
        
        .badge-item:hover {
            transform: scale(1.1);
            z-index: 10;
        }
        
        .badge-item img {
            height: 28px;
            display: block;
            border-radius: 4px;
        }

        /* Search Results Grid View */
        #search-view {
            display: none;
            padding: 40px 20px;
            max-width: 1200px;
            margin: 0 auto;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 20px;
        }
        
        .search-result-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            background: var(--card-bg);
            padding: 20px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .search-result-item:hover {
            border-color: var(--accent-color);
            transform: translateY(-2px);
        }
        
        .search-result-item span {
            margin-top: 10px;
            font-size: 0.9rem;
            color: #8b949e;
        }
        
        /* Toast Notification */
        #toast {
            visibility: hidden;
            min-width: 250px;
            background-color: #238636;
            color: #fff;
            text-align: center;
            border-radius: 4px;
            padding: 16px;
            position: fixed;
            z-index: 999;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        #toast.show {
            visibility: visible;
            animation: fadein 0.5s, fadeout 0.5s 2.5s;
        }
        
        @keyframes fadein {
            from {bottom: 0; opacity: 0;} 
            to {bottom: 30px; opacity: 1;}
        }
        
        @keyframes fadeout {
            from {bottom: 30px; opacity: 1;} 
            to {bottom: 0; opacity: 0;}
        }

    </style>
</head>
<body>

    <header>
        <h1>XScriptor Badges</h1>
        <p>Premium SVG Badges Collection. Click to copy GitHub Pages URL.</p>
        <div class="search-container">
            <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"><path d="M21.71 20.29L18 16.61A9 9 0 1 0 16.61 18l3.68 3.68a1 1 0 0 0 1.42 0 1 1 0 0 0 0-1.41zM10 16a6 6 0 1 1 6-6 6 6 0 0 1-6 6z" fill="#8b949e"/></svg>
            <input type="text" id="searchInput" placeholder="Search badges (e.g. 'python', 'docker')...">
        </div>
    </header>

    <div id="marquee-view">
"""
    
    # Generate Marquee Rows
    for i, category in enumerate(all_categories):
        subdir = subdirs_map.get(category, "misc")
        items = categories[category]
        if not items: continue
        
        direction = "marquee-left" if i % 2 == 0 else "marquee-right"
        
        html_content += f"""
        <div class="category-section">
            <span class="row-label">{category}</span>
            <div class="marquee-container">
                <div class="marquee-content {direction}">
        """
        
        # Repeat items significantly to ensure smooth infinite scroll
        # We loop enough times to cover a wide screen plus buffer
        extended_items = items * 6 if len(items) < 10 else items * 3
        
        for item in extended_items:
            safe_name = item.replace(" ", "_")
            url = f"https://xscriptordev.github.io/badges/{subdir}/{safe_name}.svg"
            local_path = f"{subdir}/{safe_name}.svg"
            html_content += f'<div class="badge-item" onclick="copyToClipboard(\'{url}\')" data-name="{item}" data-url="{url}"><img src="{local_path}" alt="{item}" loading="lazy"></div>'
            
        html_content += """
                </div>
            </div>
        </div>
        """
        
    html_content += """
    </div>

    <div id="search-view"></div>
    <div id="toast">URL Copied to Clipboard!</div>

    <script>
        const searchInput = document.getElementById('searchInput');
        const marqueeView = document.getElementById('marquee-view');
        const searchView = document.getElementById('search-view');
        
        // Collect all unique badges for search
        const allBadges = [];
        document.querySelectorAll('.marquee-content .badge-item').forEach(el => {
            const name = el.getAttribute('data-name');
            // Avoid duplicates in search index
            if (!allBadges.find(b => b.name === name)) {
                allBadges.push({
                    name: name,
                    url: el.getAttribute('data-url'),
                    src: el.querySelector('img').getAttribute('src')
                });
            }
        });

        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            
            if (query.trim() === '') {
                marqueeView.style.display = 'flex';
                searchView.style.display = 'none';
            } else {
                marqueeView.style.display = 'none';
                searchView.style.display = 'grid';
                
                const results = allBadges.filter(b => b.name.toLowerCase().includes(query));
                searchView.innerHTML = results.map(b => `
                    <div class="search-result-item" onclick="copyToClipboard('${b.url}')">
                        <img src="${b.src}" alt="${b.name}">
                        <span>${b.name}</span>
                    </div>
                `).join('');
                
                if (results.length === 0) {
                    searchView.innerHTML = '<p style="text-align:center; grid-column: 1/-1;">No results found.</p>';
                }
            }
        });

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                const toast = document.getElementById("toast");
                toast.className = "show";
                setTimeout(function(){ toast.className = toast.className.replace("show", ""); }, 3000);
            });
        }
    </script>
</body>
</html>
    """
    
    with open(os.path.join(base_dir, "index.html"), "w") as f:
        f.write(html_content)
    print("Generated index.html with marquee search Showcase")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    references_path = os.path.join(base_dir, 'references.md')
    
    # Create directories
    for subdir in ['terminal', 'social', 'software', 'languages', 'frameworks', 'ide', 'editors']:
        path = os.path.join(base_dir, subdir)
        if not os.path.exists(path):
            os.makedirs(path)
        
    # Hardcode to use only the "X" palette and filter for vibrant colors
    # We ignore the parse_palettes function results effectively, or rather we manually define the palette
    # based on the X scheme in references.md to ensure absolute correctness.
    
    # X Scheme Colors (Vibrant Subset)
    # color1: #fc618d (Pink)
    # color2: #7bd88f (Green)
    # color3: #fce566 (Yellow)
    # color4: #fd9353 (Orange)
    # color5: #948ae3 (Purple)
    # color6: #5ad4e6 (Cyan)
    
    vibrant_colors = [
        "#fc618d", "#7bd88f", "#fce566", "#fd9353", "#948ae3", "#5ad4e6"
    ]
    
    palette_cycle = itertools.cycle(vibrant_colors)

    if not vibrant_colors:
        print("Error setting up vibrant colors.")
        return

    terminal_items = [
        "alacritty", "assets", "foot", "ghostty", "gnome-terminal", "hyper", 
        "iterm", "kitty", "konsole", "LICENSE", "mobaxterm", "powershell", 
        "ptyxis", "putty", "README.md", "references.md", "roadmap.md", 
        "terminal.app", "terminator", "termux", "tilix", "warp", "wezterm", "xfce"
    ]
    
    social_items = [
        "github", "gitlab", "bitbucket",
        "linkedin", "twitter", "x", "mastodon", "bluesky",
        "discord", "telegram", "signal", "whatsapp",
        "medium", "dev.to", "hashnode",
        "hackthebox", "tryhackme", "kaggle", "leetcode",
        "stack-overflow", "reddit",
        "youtube", "twitch", "instagram"
    ]
    
    # Software items updated (Migrated Design tools)
    software_items = [
        "xfetch", "xtop",
        "wireshark", "burpsuite", "metasploit", "nmap", "john-the-ripper", "aircrack-ng", "hashcat", "ghidra"
    ]
    
    ide_items = [
        "intellij", "pycharm", "eclipse", "android-studio", "xcode", "visual-studio", "webstorm", "goland", "clion", "rider", "antigravity", "trae-ai"
    ]
    
    editors_items = [
         "vscode", "vim", "neovim", "sublime-text", "atom", "notepad++", "emacs", "nano", "cursor", "vscodium", "code-oss"
    ]
    
    browsers_items = [
        "chrome", "firefox", "edge", "brave", "safari", "opera", "vivaldi", "tor", "arc", "chromium"
    ]
    
    cloud_items = [
        "aws", "gcp", "azure", "digitalocean", "heroku", "vercel", "netlify", "cloudflare", "firebase", "supabase", "openstack"
    ]
    
    files_items = [
        "json", "yaml", "xml", "markdown", "csv", "pdf", "txt", "zip"
    ]
    
    os_items = [
        "linux", "windows", "macos", "android", "ios", "freebsd", "ubuntu", "debian", "arch", "fedora", "kali", "nixos", "gentoo", "parrot", "x"
    ]
    
    tools_items = [
        "git", "docker", "kubernetes", "npm", "yarn", "pnpm", "webpack", "vite", "babel", "eslint", "prettier", "postman", "insomnia", "ansible", "terraform", "pm2", "nginx"
    ]
    
    ai_items = [
        "openai", "chatgpt", "copilot", "gemini", "claude", "tensorflow", "pytorch", "keras", "huggingface", "midjourney", "stable-diffusion", "ollama", "mistral", "llama"
    ]
    
    design_items = [
        "figma", "canva", "photoshop", "illustrator", "inkscape", "gimp", "blender", "after-effects", "premiere", "xd", "sketch", "dribbble", "behance", "krita"
    ]
    
    hardware_items = [
        "arduino", "raspberry-pi", "nvidia", "intel", "amd", "apple-silicon", "esp32", "risc-v"
    ]
    
    licenses_items = [
        "mit", "apache", "gpl", "bsd", "cc0", "unlicense", "mozilla"
    ]
    
    status_items = [
        "build-passing", "build-failing", "stable", "beta", "alpha", "deprecated", "maintained", "wip"
    ]
    
    gaming_items = [
        "steam", "unity", "unreal-engine", "godot", "minecraft", "roblox", "nintendo", "playstation", "xbox"
    ]
    
    finance_items = [
        "stripe", "paypal", "mastercard", "visa", "amex", "klarna", "square", "google-pay", "apple-pay"
    ]
    
    ci_items = [
        "github-actions", "gitlab-ci", "jenkins", "circleci", "travis-ci", "drone", "azure-pipelines", "bitbucket-pipelines"
    ]
    
    crypto_items = [
        "bitcoin", "ethereum", "solana", "dogecoin", "tether", "binance", "coinbase", "monero"
    ]
    
    analytics_items = [
        "google-analytics", "matomo", "plausible", "grafana", "tableau", "powerbi", "mixpanel", "amplitude"
    ]
    
    productivity_items = [
        "notion", "obsidian", "trello", "asana", "jira", "clickup", "monday", "slack", "zoom", "microsoft-teams"
    ]
    
    misc_items = [
        "sponsors", "ko-fi", "patreon", "buymeacoffee", "liberapay", "donate"
    ]

    desktops_items = [
        "gnome", "kde", "plasma", "xfce", "hyprland", "i3", "sway", "cinnamon", "mate", "budgie", "lxqt", "openbox", "bspwm", "awesome", "qtile", "wayland", "x11"
    ]

    languages_items = [
        "python", "rust", "go", "c", "cpp", "java", "javascript", "typescript", "php", "ruby", "swift",
        "kotlin", "scala", "r", "matlab", "perl", "lua", "haskell", "julia", "dart",
        "html", "css", "sql", "assembly", "objective-c", "visual-basic", "groovy",
        "elixir", "clojure", "fsharp", "ocaml", "lisp", "fortran", "cobol", "pascal",
        "ada", "prolog", "solidity", "vala", "vhdl", "verilog", "elm", "nim", "crystal", "zig", "reason", "purescript",
        "shell", "powershell" 
    ]
    
    frameworks_items = [
        "react", "vue", "angular", "svelte", "solid",
        "nextjs", "nuxtjs", "astro", "remix", "gatsby",
        "django", "flask", "fastapi", "rails", "laravel", "spring", "express", "nestjs",
        "flutter", "react-native", "electron", "tauri",
        "bootstrap", "tailwind", "bulma", "sass", "less",
        "dotnet", "qt"
    ]

    # Sort items
    terminal_items.sort()
    social_items.sort()
    software_items.sort()
    ide_items.sort()
    editors_items.sort()
    browsers_items.sort()
    cloud_items.sort()
    files_items.sort()
    os_items.sort()
    tools_items.sort()
    ai_items.sort()
    design_items.sort()
    hardware_items.sort()
    licenses_items.sort()
    status_items.sort()
    gaming_items.sort()
    finance_items.sort()
    ci_items.sort()
    crypto_items.sort()
    analytics_items.sort()
    productivity_items.sort()
    misc_items.sort()
    desktops_items.sort()
    languages_items.sort()
    frameworks_items.sort()
    
    
    # Palette logic simplified to single cycle above

    
    # Helper for loop generation
    loop_configs = [
        ('terminal', terminal_items, 'terminal'),
        ('social', social_items, 'social'),
        ('software', software_items, 'software'),
        ('ide', ide_items, 'ide'),
        ('editors', editors_items, 'editors'),
        ('browsers', browsers_items, 'browsers'),
        ('cloud', cloud_items, 'cloud'),
        ('files', files_items, 'files'),
        ('os', os_items, 'os'),
        ('tools', tools_items, 'tools'),
        ('ai', ai_items, 'ai'),
        ('design', design_items, 'design'),
        ('hardware', hardware_items, 'hardware'),
        ('licenses', licenses_items, 'licenses'),
        ('status', status_items, 'status'),
        ('gaming', gaming_items, 'gaming'),
        ('finance', finance_items, 'finance'),
        ('ci', ci_items, 'ci'),
        ('crypto', crypto_items, 'crypto'),
        ('analytics', analytics_items, 'analytics'),
        ('productivity', productivity_items, 'productivity'),
        ('misc', misc_items, 'misc'),
        ('desktops', desktops_items, 'desktops'),
        ('languages', languages_items, 'languages'),
        ('frameworks', frameworks_items, 'frameworks')
    ]
    
    for subdir, items, icon_type in loop_configs:
        out_dir = os.path.join(base_dir, subdir)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
            
        for item in items:
            safe_name = item.replace(" ", "_")
            current_color = next(palette_cycle)
            
            file_path = os.path.join(out_dir, f"{safe_name}.svg")
            create_badge(item, current_color, file_path, icon_type=icon_type)
            print(f"Generated {file_path}")

    subdirs_map = {
        "Terminal Badges": "terminal",
        "IDEs": "ide",
        "Text Editors": "editors",
        "Browsers": "browsers",
        "Operating Systems": "os",
        "Desktop Environments": "desktops",
        "Programming Languages": "languages",
        "Frameworks": "frameworks",
        "Cloud Services": "cloud",
        "Development Tools": "tools",
        "AI & Machine Learning": "ai",
        "Design Tools": "design",
        "Hardware": "hardware",
        "Licenses": "licenses",
        "Project Status": "status",
        "Gaming": "gaming",
        "Finance": "finance",
        "CI/CD": "ci",
        "Crypto": "crypto",
        "Analytics": "analytics",
        "Productivity": "productivity",
        "Miscellaneous": "misc",
        "File Types": "files",
        "Software Badges": "software",
        "Social Badges": "social"
    }

    categories = {k: v for k, v in [
        ("Terminal Badges", terminal_items),
        ("IDEs", ide_items),
        ("Text Editors", editors_items),
        ("Browsers", browsers_items),
        ("Operating Systems", os_items),
        ("Desktop Environments", desktops_items),
        ("Programming Languages", languages_items),
        ("Frameworks", frameworks_items),
        ("Cloud Services", cloud_items),
        ("Development Tools", tools_items),
        ("AI & Machine Learning", ai_items),
        ("Design Tools", design_items),
        ("Hardware", hardware_items),
        ("Gaming", gaming_items),
        ("Finance", finance_items),
        ("CI/CD", ci_items),
        ("Crypto", crypto_items),
        ("Analytics", analytics_items),
        ("Productivity", productivity_items),
        ("Miscellaneous", misc_items),
        ("Licenses", licenses_items),
        ("Project Status", status_items),
        ("File Types", files_items),
        ("Software Badges", software_items),
        ("Social Badges", social_items)
    ]}
    
    # Custom main readme generation using new structure
    readme_path = os.path.join(base_dir, 'README.md')
    
    # Project Description
    content = "# Badges Collection\n\n"
    content += "A comprehensive collection of standardized, high-quality badges for your projects. Generated with repository-specific color palettes and custom SVG icons.\n\n"
    content += "## Usage\n\n"
    content += "You can use these badges directly from the GitHub repository or via GitHub Pages.\n\n"
    content += "<details>\n<summary><strong>Expand Usage Examples</strong></summary>\n\n"
    content += "### Markdown Example\n"
    content += "```markdown\n"
    content += "![Badge Name](https://xscriptordev.github.io/badges/category/badge-name.svg)\n"
    content += "```\n\n"
    content += "### HTML Example\n"
    content += "```html\n"
    content += '<img src="https://xscriptordev.github.io/badges/category/badge-name.svg" alt="Badge Name" />\n'
    content += "```\n\n"
    content += "</details>\n\n"
    
    content += "## Categories\n\n"
    
    # Sort categories alphabetically
    sorted_sections = sorted(categories.keys())
    
    for section in sorted_sections:
        items = categories[section]
        subdir = subdirs_map.get(section, "misc")
        
        # Collapsible section
        content += f"<details>\n"
        content += f"<summary><strong>{section}</strong></summary>\n\n"
        content += f"| Badge | Name |\n"
        content += f"| --- | --- |\n"
        
        for item in items:
             safe_name = item.replace(" ", "_")
             rel_path = f"./{subdir}/{safe_name}.svg"
             content += f"| ![{item}]({rel_path}) | `{item}` |\n"
        
        content += "\n</details>\n\n"
        
    with open(readme_path, 'w') as f:
        f.write(content)
    print(f"Generated {readme_path}")
    
    # Generate JSON for frontend
    generate_badges_json(categories, subdirs_map, base_dir)
import json

def generate_badges_json(categories, subdirs_map, base_dir):
    """Generates a badges.json file for the frontend to consume."""
    
    badges_data = {}
    
    # Collect all badges
    all_categories = sorted(categories.keys())
    
    for category in all_categories:
        subdir = subdirs_map.get(category, "misc")
        items = categories[category]
        if not items: continue
        
        badges_list = []
        for item in items:
            safe_name = item.replace(" ", "_")
            rel_path = f"{subdir}/{safe_name}.svg"
            url = f"https://xscriptordev.github.io/badges/{subdir}/{safe_name}.svg"
            
            badges_list.append({
                "name": item,
                "path": rel_path,
                "url": url
            })
            
        badges_data[category] = badges_list
        
    json_path = os.path.join(base_dir, "badges.json")
    with open(json_path, "w") as f:
        json.dump(badges_data, f, indent=2)
    print(f"Generated {json_path}") 

if __name__ == "__main__":
    main()
