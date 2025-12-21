import os
import glob
from pathlib import Path
from PIL import Image
import io
import subprocess

EVOLUTION_DIR = "monkey_evolution"
OUTPUT_FILE = "monkey_evolution/evolution.gif"
DURATION = 500  # ms between frames

def create_animation():
    svg_files = sorted(glob.glob(os.path.join(EVOLUTION_DIR, "*_monkey*.svg")))
    
    if not svg_files:
        print("No SVG files found in monkey_evolution/")
        return

    print(f"Found {len(svg_files)} evolution steps.")
    
    frames = []
    for svg_path in svg_files:
        print(f"Processing {os.path.basename(svg_path)}...")
        try:
            # Use rsvg-convert CLI to convert SVG to PNG
            result = subprocess.run(
                ["rsvg-convert", svg_path], 
                capture_output=True, 
                check=True
            )
            png_data = result.stdout
            img = Image.open(io.BytesIO(png_data))
            frames.append(img)
        except subprocess.CalledProcessError as e:
            print(f"rsvg-convert failed for {svg_path}: {e}")
        except Exception as e:
            print(f"Error processing {svg_path}: {e}")

    if frames:
        print(f"Generating GIF with {len(frames)} frames...")
        # Save as GIF
        frames[0].save(
            OUTPUT_FILE,
            save_all=True,
            append_images=frames[1:],
            duration=DURATION,
            loop=0
        )
        print(f"✅ Animation saved to {OUTPUT_FILE}")
    else:
        print("No valid frames generated.")

if __name__ == "__main__":
    create_animation()
