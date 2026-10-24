import sys
import math
from PIL import Image, ImageDraw

def compute_bounding_box(instructions, angle_step):
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
            angle -= angle_step
        elif cmd == '-':
            angle += angle_step
        elif cmd == '[':
            stack.append((x, y, angle))
        elif cmd == ']':
            if stack:
                x, y, angle = stack.pop()
                
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), max(xs), min(ys), max(ys)

def render(angle_step, generations, filename):
    width, height = 800, 800
    margin = 50
    
    last_gen = generations[-1]
    min_x, max_x, min_y, max_y = compute_bounding_box(last_gen, angle_step)
    
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
        frame_interval = max(1, f_count // 50) 
        
        f_drawn = 0
        
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
                    
            elif cmd == '+':
                angle -= angle_step
            elif cmd == '-':
                angle += angle_step
            elif cmd == '[':
                stack.append((x, y, angle))
            elif cmd == ']':
                if stack:
                    x, y, angle = stack.pop()

        frames.append(img.copy())
        durations.append(2500 if gen_idx == len(generations) - 1 else 1200)

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
    filename = sys.argv[1] if len(sys.argv) > 1 else "animation.gif"
    filename = "animations/" + filename

    raw_text = sys.stdin.read()
    lines = [line.strip() for line in raw_text.splitlines() if line.strip() != ""]
    
    if lines:
        parsed_angle = float(lines[0])
        generations = lines[1:]
        render(parsed_angle, generations, filename=filename)