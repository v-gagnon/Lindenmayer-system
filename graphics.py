import sys
import math
from PIL import Image, ImageDraw

ANGLE_STEP = 25

def compute_bounding_box(instructions):
    """Calcule la taille du cadre."""
    x, y, angle = 0.0, 0.0, -90.0
    stack = []
    points = [(x, y)]
    
    for cmd in instructions:
        if cmd == 'F':
            rad = math.radians(angle)
            x += math.cos(rad)
            y += math.sin(rad)
            points.append((x, y))
        elif cmd == '+':
            angle += ANGLE_STEP
        elif cmd == '-':
            angle -= ANGLE_STEP
        elif cmd == '[':
            stack.append((x, y, angle))
        elif cmd == ']':
            if stack:
                x, y, angle = stack.pop()
                
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), max(xs), min(ys), max(ys)

def update_progress_bar(current_f, total_f, gen_idx, total_gens, bar_length=25):
    """Affiche une barre de progression ASCII."""
    fraction = current_f / total_f if total_f > 0 else 1.0
    percent = fraction * 100.0
    
    filled = int(bar_length * fraction)
    bar = '#' * filled + '*' * (bar_length - filled)
    
    sys.stdout.write(f"\r[Gen {gen_idx + 1}/{total_gens}] [{bar}] {percent:5.1f}%")
    sys.stdout.flush()

def render(generations, filename="plant.gif"):
    # Render bar parameters
    total_gens = len(generations)
    total_f = sum([gen.count('F') for gen in generations])
    
    width, height = 800, 800
    margin = 50
    
    last_gen = generations[-1]
    min_x, max_x, min_y, max_y = compute_bounding_box(last_gen)
    
    span_x = max(max_x - min_x, 1e-5)
    span_y = max(max_y - min_y, 1e-5)
    
    scale = min((width - 2 * margin) / span_x, (height - 2 * margin) / span_y)
    offset_x = margin + ((width - 2 * margin) - span_x * scale) / 2 - min_x * scale
    offset_y = margin + ((height - 2 * margin) - span_y * scale) / 2 - min_y * scale

    frames = []
    durations = []

    for gen_idx, gen_instructions in enumerate(generations):
        img = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(img)
        
        x, y = 0.0, 0.0
        angle = -90.0
        stack = []
        
        f_count = gen_instructions.count('F')
        frame_interval = max(1, f_count // 50) # 1 / frame_interval des frames sont dessinées
        
        f_drawn = 0

        update_progress_bar(0, total_f, gen_idx, total_gens)
        
        for cmd in gen_instructions:
            if cmd == 'F':
                rad = math.radians(angle)
                nx = x + math.cos(rad)
                ny = y + math.sin(rad)
                
                p1 = (offset_x + x * scale, offset_y + y * scale)
                p2 = (offset_x + nx * scale, offset_y + ny * scale)
                
                draw.line([p1, p2], fill="white", width=2)
                x, y = nx, ny
                
                f_drawn += 1
                if f_drawn % frame_interval == 0:
                    frames.append(img.copy())
                    durations.append(20)
                    update_progress_bar(f_drawn, total_f, gen_idx, total_gens)
                    
            elif cmd == '+':
                angle += ANGLE_STEP
            elif cmd == '-':
                angle -= ANGLE_STEP
            elif cmd == '[':
                stack.append((x, y, angle))
            elif cmd == ']':
                if stack:
                    x, y, angle = stack.pop()

        frames.append(img.copy())
        # Pause : 1200 ms entre les générations, 2500 ms sur la forme finale
        durations.append(2500 if gen_idx == total_gens - 1 else 1200)
        
    update_progress_bar(total_f, total_f, gen_idx, total_gens)
    sys.stdout.write(" [DONE]\n")
    sys.stdout.flush()

    print(f"\nGénération du GIF...")        
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0
    )
    print(f"GIF enregistré : {filename}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            raw_text = f.read()
    else:
        raw_text = sys.stdin.read()

    generations = []
    for line in raw_text.splitlines():
        cleaned = line.strip()
        if cleaned != "":
            generations.append(cleaned)

    render(generations)