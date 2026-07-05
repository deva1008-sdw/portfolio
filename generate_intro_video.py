import os
import sys
import math
import shutil
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy import ImageSequenceClip, AudioFileClip
import imageio_ffmpeg

# Slide Data Definition
slides_data = [
    {
        "type": "intro",
        "title": "TULASI KRISHNA KUMAR",
        "subtitle": "Full-Stack Developer & Cybersecurity Architect",
        "narrative": "Hi, I am Tulasi Krishna Kumar, a Full-Stack Developer and Cybersecurity Architect. Welcome to my technical portfolio.",
    },
    {
        "type": "project",
        "title": "Cyber Nervous System",
        "role": "Backend & Graph Database Architect",
        "value": "$1,500 - $4,000+",
        "image": "images/cns_thumbnail.png",
        "description": "Built an AI code auditor utilizing tree-sitter AST parsing and a Neo4j knowledge graph to map software vulnerabilities. Integrated the OSV.dev API to map dependencies to known CVE databases, and integrated Google Gemini API to analyze graph structures and identify complex security risks.",
        "skills": ["Neo4j", "FastAPI", "Gemini API", "AST Parsing", "Security"],
        "narrative": "First, the Cyber Nervous System: an AI code auditor utilizing tree-sitter AST parsing and a Neo4j knowledge graph to map software vulnerabilities.",
    },
    {
        "type": "project",
        "title": "BugBounty-AI Scanner",
        "role": "Backend & Automation Engineer",
        "value": "$1,000 - $2,500",
        "image": "images/bugbounty_thumbnail.png",
        "description": "Created an automated reconnaissance and asset discovery engine that integrates offensive utilities with AI-driven threat triage. Built a FastAPI backend backed by Celery and Redis to execute subdomain discovery, port scanning, and web crawling concurrently, using OpenAI to filter exploits.",
        "skills": ["FastAPI", "Celery", "Redis", "PostgreSQL", "AI Automation"],
        "narrative": "Next, BugBounty-AI: an automated recon scanner using FastAPI, Celery, and OpenAI to parse logs and triage exploits.",
    },
    {
        "type": "project",
        "title": "Apex Quant Visualizer",
        "role": "Lead Full-Stack & Quant Developer",
        "value": "$800 - $2,000",
        "image": "images/apex_quant_thumbnail.png",
        "description": "Built an interactive quantitative trading analytics platform featuring a custom technical indicator engine and live charting. Integrated TradingView's Lightweight Charts library with Next.js and React 19 to display dynamic candlesticks, EMA ribbons, and WebSocket pricing feeds.",
        "skills": ["Next.js", "WebSockets", "Zustand", "TradingView Charts", "Express.js"],
        "narrative": "Apex Quant is an interactive trading Strategy Visualizer built with React, WebSockets, and real-time TradingView charts.",
    },
    {
        "type": "project",
        "title": "SafeTracker System",
        "role": "Lead Mobile & Backend Developer",
        "value": "$600 - $1,500",
        "image": "images/safetracker_thumbnail.png",
        "description": "Designed and built a consent-first GPS tracking ecosystem featuring a React Native mobile app, a Node.js backend, and a real-time web dashboard. Implemented robust background location services with a permanent Android notification bar and offline batch syncing.",
        "skills": ["React Native", "Node.js", "WebSockets", "Leaflet.js", "Mobile App"],
        "narrative": "SafeTracker is a consent-first GPS mobile app with offline batch syncing and real-time mapping dashboards.",
    },
    {
        "type": "project",
        "title": "IoT Guardian Pro",
        "role": "Full-Stack Cybersecurity Developer",
        "value": "$500 - $1,200",
        "image": "images/iot_guardian_thumbnail.png",
        "description": "Developed an educational cybersecurity platform and live network simulation dashboard. Engineered a FastAPI backend to safely model network attack vectors like DDoS floods and brute-forcing, displaying live packet rates, latency, and generating automated PDF audits.",
        "skills": ["FastAPI", "React.js", "WebSockets", "Network Security", "Python"],
        "narrative": "IoT Guardian Pro is a network security simulation dashboard with interactive live-packet metrics and PDF audits.",
    },
    {
        "type": "project",
        "title": "Nexalith Prime Portal",
        "role": "Frontend Developer & Animator",
        "value": "$300 - $800",
        "image": "images/nexalith_thumbnail.png",
        "description": "Designed and developed a highly interactive, futuristic corporate portal for a cybersecurity firm using React, Vite, and Tailwind CSS. Implemented a dark-mode design with smooth animations powered by Framer Motion and custom particle networks running at 60 FPS.",
        "skills": ["React.js", "Framer Motion", "Tailwind CSS", "SEO", "Responsive UI"],
        "narrative": "Finally, Nexalith Prime: an animated corporate portal built with React and Framer Motion running at sixty frames per second.",
    },
    {
        "type": "outro",
        "title": "LET'S BUILD SOMETHING SECURE & SCALABLE",
        "subtitle": "Available for contract work on Upwork",
        "narrative": "I build robust, secure, and performant systems. Let's collaborate on your next project on Upwork.",
    }
]

# Helper to draw vertical gradient
def draw_vertical_gradient(width, height, color1, color2):
    base = Image.new('RGB', (1, height))
    for y in range(height):
        ratio = y / float(height - 1)
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        base.putpixel((0, y), (r, g, b))
    return base.resize((width, height))

# Load Background once globally
BACKGROUND_IMAGE = draw_vertical_gradient(1920, 1080, (11, 15, 25), (30, 27, 75))

# Helper to load system fonts
def load_font(font_name, size):
    try:
        path = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", font_name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
        return ImageFont.load_default()
    except Exception:
        return ImageFont.load_default()

# Load Fonts once globally
FONTS = {
    "title": load_font("segoeuib.ttf", 60),
    "subtitle": load_font("segoeui.ttf", 36),
    "role": load_font("seguisb.ttf", 32),
    "desc": load_font("segoeui.ttf", 26),
    "val": load_font("segoeuib.ttf", 30),
    "tag": load_font("consola.ttf", 20),
    "cta": load_font("consola.ttf", 26)
}

# Helper to wrap text
def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = font.getbbox(test_line)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    return lines

# Pre-cropped project image preparation
def prepare_slide_image(slide, card_w=780, card_h=470):
    if "image" not in slide:
        return None
    img_path = slide["image"]
    if not os.path.exists(img_path):
        return None
        
    img = Image.open(img_path)
    
    # Aspect crop
    img_aspect = img.width / float(img.height)
    card_aspect = card_w / float(card_h)
    if img_aspect > card_aspect:
        new_w = int(img.height * card_aspect)
        x0 = (img.width - new_w) // 2
        img_cropped = img.crop((x0, 0, x0 + new_w, img.height))
    else:
        new_h = int(img.width / card_aspect)
        y0 = (img.height - new_h) // 2
        img_cropped = img.crop((0, y0, img.width, y0 + new_h))
        
    img_card = img_cropped.resize((card_w, card_h), Image.Resampling.BILINEAR)
    return img_card

# Pre-calculate layout and font dimensions for a slide
def prepare_slide_layout(slide):
    layout = {}
    
    if slide["type"] == "intro":
        title_text = slide["title"]
        bbox = FONTS["title"].getbbox(title_text)
        w = bbox[2] - bbox[0]
        layout["title_x"] = (1920 - w) // 2
        
        sub_text = slide["subtitle"]
        sub_bbox = FONTS["subtitle"].getbbox(sub_text)
        sw = sub_bbox[2] - sub_bbox[0]
        layout["sub_x"] = (1920 - sw) // 2
        
    elif slide["type"] == "outro":
        title_text = slide["title"]
        bbox = FONTS["title"].getbbox(title_text)
        w = bbox[2] - bbox[0]
        layout["title_x"] = (1920 - w) // 2
        
        sub_text = slide["subtitle"]
        sub_bbox = FONTS["subtitle"].getbbox(sub_text)
        sw = sub_bbox[2] - sub_bbox[0]
        layout["sub_x"] = (1920 - sw) // 2
        
        cta_text = "github.com/deva1008-sdw  |  Let's Build Together"
        cta_bbox = FONTS["cta"].getbbox(cta_text)
        cx = (1920 - (cta_bbox[2] - cta_bbox[0])) // 2
        layout["cta_x"] = cx
        
    elif slide["type"] == "project":
        desc_text = slide["description"]
        layout["wrapped_desc_lines"] = wrap_text(desc_text, FONTS["desc"], 800)
        
        badges = []
        for tag in slide["skills"]:
            tag_bbox = FONTS["tag"].getbbox(tag)
            tw = tag_bbox[2] - tag_bbox[0]
            th = tag_bbox[3] - tag_bbox[1]
            badges.append({
                "tag": tag,
                "w": tw,
                "h": th,
                "rect_w": tw + 20,
                "rect_h": 36
            })
        layout["badges"] = badges
        
    return layout

# Frame Drawing Logic
def draw_frame(slide, prepared_img, layout, t, duration):
    frame = BACKGROUND_IMAGE.copy()
    
    entrance_dur = 0.6
    y_offset = 0
    alpha = 255
    if t < entrance_dur:
        ratio = t / entrance_dur
        ease = ratio * (2.0 - ratio) # Ease out quad
        y_offset = int((1.0 - ease) * 45)
        alpha = int(ratio * 255)
        
    overlay = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    if slide["type"] == "intro":
        title_text = slide["title"]
        x = layout["title_x"]
        y = (1080 - 150) // 2 - y_offset
        overlay_draw.text((x, y), title_text, fill=(255, 255, 255, alpha), font=FONTS["title"])
        
        sub_text = slide["subtitle"]
        sx = layout["sub_x"]
        sy = y + 85
        overlay_draw.text((sx, sy), sub_text, fill=(148, 163, 184, alpha), font=FONTS["subtitle"])
        
        # Accent gradient line
        line_w = 480
        line_x1 = (1920 - line_w) // 2
        line_y = sy + 70
        for lx in range(line_w):
            l_ratio = lx / float(line_w)
            lr = int(99 * (1 - l_ratio) + 236 * l_ratio)
            lg = int(102 * (1 - l_ratio) + 72 * l_ratio)
            lb = int(241 * (1 - l_ratio) + 153 * l_ratio)
            overlay_draw.line([(line_x1 + lx, line_y), (line_x1 + lx + 1, line_y)], fill=(lr, lg, lb, alpha), width=3)
            
    elif slide["type"] == "outro":
        title_text = slide["title"]
        x = layout["title_x"]
        y = (1080 - 180) // 2 - y_offset
        overlay_draw.text((x, y), title_text, fill=(255, 255, 255, alpha), font=FONTS["title"])
        
        sub_text = slide["subtitle"]
        sx = layout["sub_x"]
        sy = y + 90
        overlay_draw.text((sx, sy), sub_text, fill=(16, 185, 129, alpha), font=FONTS["subtitle"])
        
        cta_text = "github.com/deva1008-sdw  |  Let's Build Together"
        cx = layout["cta_x"]
        cy = sy + 80
        overlay_draw.text((cx, cy), cta_text, fill=(148, 163, 184, alpha), font=FONTS["cta"])
        
    elif slide["type"] == "project":
        lx = 100
        ly = 150 - y_offset
        
        overlay_draw.text((lx, ly), slide["title"], fill=(255, 255, 255, alpha), font=FONTS["title"])
        
        role_text = f"Role: {slide['role']}"
        ly += 85
        overlay_draw.text((lx, ly), role_text, fill=(148, 163, 184, alpha), font=FONTS["role"])
        
        val_text = f"Project Value: {slide['value']}"
        ly += 55
        overlay_draw.text((lx, ly), val_text, fill=(16, 185, 129, alpha), font=FONTS["val"])
        
        ly += 55
        overlay_draw.line([(lx, ly), (lx + 800, ly)], fill=(255, 255, 255, int(alpha * 0.12)), width=2)
        
        ly += 30
        for line in layout["wrapped_desc_lines"]:
            overlay_draw.text((lx, ly), line, fill=(203, 213, 225, alpha), font=FONTS["desc"])
            ly += 36
            
        ly += 35
        badge_x = lx
        for b in layout["badges"]:
            overlay_draw.rounded_rectangle(
                [badge_x, ly, badge_x + b["rect_w"], ly + b["rect_h"]],
                radius=6,
                fill=(255, 255, 255, int(alpha * 0.04)),
                outline=(255, 255, 255, int(alpha * 0.12)),
                width=1
            )
            overlay_draw.text((badge_x + 10, ly + (b["rect_h"] - b["h"])//2 - 2), b["tag"], fill=(203, 213, 225, alpha), font=FONTS["tag"])
            badge_x += b["rect_w"] + 12
            
        if prepared_img is not None:
            card_w = 780
            card_h = 470
            
            zoom = 1.0 + 0.05 * (t / duration)
            zoom_w = int(card_w * zoom)
            zoom_h = int(card_h * zoom)
            img_resized = prepared_img.resize((zoom_w, zoom_h), Image.Resampling.BILINEAR)
            
            cx0 = (zoom_w - card_w) // 2
            cy0 = (zoom_h - card_h) // 2
            img_card = img_resized.crop((cx0, cy0, cx0 + card_w, cy0 + card_h))
            
            mask = Image.new('L', (card_w, card_h), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.rounded_rectangle([0, 0, card_w, card_h], radius=16, fill=255)
            
            card_x = 1040
            card_y = (1080 - card_h) // 2 - y_offset
            
            frame.paste(img_card, (card_x, card_y), mask=mask)
            
            overlay_draw.rounded_rectangle(
                [card_x - 1, card_y - 1, card_x + card_w + 1, card_y + card_h + 1],
                radius=17,
                fill=(0, 0, 0, 0),
                outline=(255, 255, 255, int(alpha * 0.16)),
                width=2
            )
            
    progress_w = int(1920 * (t / duration))
    progress_h = 6
    for px in range(progress_w):
        p_ratio = px / float(1920)
        pr = int(99 * (1 - p_ratio) + 236 * p_ratio)
        pg = int(102 * (1 - p_ratio) + 72 * p_ratio)
        pb = int(241 * (1 - p_ratio) + 153 * p_ratio)
        overlay_draw.line([(px, 1080 - progress_h), (px, 1080)], fill=(pr, pg, pb, alpha), width=progress_h)
        
    frame_rgba = Image.alpha_composite(frame.convert("RGBA"), overlay)
    return frame_rgba.convert("RGB")

def main():
    fps = 24
    temp_dir = "temp_render"
    if os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass
            
    os.makedirs(temp_dir, exist_ok=True)
    
    slide_clips = []
    
    print("Starting fully optimized in-memory rendering pipeline...")
    for idx, slide in enumerate(slides_data):
        print(f"\n--- Processing Slide {idx} ({slide['title'] if 'title' in slide else 'Intro/Outro'}) ---")
        sys.stdout.flush()
        
        # 1. Generate Voiceover MP3 using gTTS
        print("  Generating voiceover narration...")
        sys.stdout.flush()
        tts = gTTS(text=slide["narrative"], lang="en", tld="com")
        audio_path = os.path.join(temp_dir, f"audio_{idx}.mp3")
        tts.save(audio_path)
        
        # 2. Get Audio Duration
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        print(f"  Duration: {duration:.2f} seconds")
        sys.stdout.flush()
        
        # 3. Pre-process Slide Image & Layout
        prepared_img = prepare_slide_image(slide)
        layout = prepare_slide_layout(slide)
        
        # 4. Generate Slide Frames in RAM
        print("  Rendering slide frames in memory...")
        sys.stdout.flush()
        slide_frames = []
        num_frames = int(duration * fps)
        for f_idx in range(num_frames):
            t = f_idx / fps
            frame_img = draw_frame(slide, prepared_img, layout, t, duration)
            slide_frames.append(np.array(frame_img))
            
        # 5. Create VideoClip from memory frames
        print("  Creating slide video clip...")
        sys.stdout.flush()
        slide_clip = ImageSequenceClip(slide_frames, fps=fps)
        
        if hasattr(slide_clip, "with_audio"):
            slide_clip = slide_clip.with_audio(audio_clip)
        else:
            slide_clip = slide_clip.set_audio(audio_clip)
            
        temp_slide_video = os.path.join(temp_dir, f"temp_slide_{idx}.mp4")
        print(f"  Writing slide temp video -> {temp_slide_video}...")
        sys.stdout.flush()
        slide_clip.write_videofile(
            temp_slide_video,
            fps=fps,
            codec="libx264",
            audio_codec="aac",
            logger=None
        )
        
        slide_clip.close()
        audio_clip.close()
        slide_frames.clear()
        slide_clips.append(temp_slide_video)
                
    # 6. Concatenate All Slides using FFmpeg stream copy (takes less than 1 second!)
    print("\n--- Compiling Final Video using FFmpeg ---")
    sys.stdout.flush()
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    # Write concat list file
    concat_list_path = os.path.join(temp_dir, "concat_list.txt")
    with open(concat_list_path, "w") as f:
        for clip in slide_clips:
            clip_name = os.path.basename(clip)
            f.write(f"file '{clip_name}'\n")
            
    output_filename = "intro_video.mp4"
    if os.path.exists(output_filename):
        try:
            os.remove(output_filename)
        except Exception:
            pass
            
    # Run FFmpeg concat command
    cmd = [
        ffmpeg_exe,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "concat_list.txt",
        "-c", "copy",
        output_filename
    ]
    
    print(f"Running FFmpeg: {' '.join(cmd)}")
    sys.stdout.flush()
    
    # Run the command with cwd set to temp_dir so relative file paths in concat_list.txt resolve correctly
    subprocess.run(cmd, cwd=temp_dir)
    
    # Move compiled file from temp_render back to the parent directory
    temp_output_path = os.path.join(temp_dir, output_filename)
    if os.path.exists(temp_output_path):
        shutil.move(temp_output_path, output_filename)
        
    # 7. Cleanup Temporary Assets
    print("Cleaning up temporary render files...")
    sys.stdout.flush()
    try:
        shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Warning: Could not remove temporary directory: {e}")
        sys.stdout.flush()
        
    print(f"\nDone! Intro video successfully compiled to '{output_filename}'!")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
