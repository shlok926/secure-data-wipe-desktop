"""
SecureWipe Icon Generator
Creates a professional logo for the application
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_securewipe_icon():
    """Generate a professional SecureWipe icon"""
    
    # Icon size (256x256 for high quality)
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(img)
    
    # Color scheme
    bg_color = (15, 23, 42)  # Dark navy blue
    accent_color = (34, 197, 94)  # Bright green (security theme)
    lock_color = (59, 130, 246)  # Bright blue
    highlight = (255, 255, 255)  # White
    
    # Draw background circle
    padding = 10
    draw.ellipse(
        [(padding, padding), (size - padding, size - padding)],
        fill=bg_color,
        outline=accent_color,
        width=3
    )
    
    # Draw lock symbol (simple geometric design)
    
    # Lock body (rectangle)
    lock_left = 70
    lock_top = 90
    lock_right = 186
    lock_bottom = 180
    
    # Lock shackle (curved top part)
    shackle_box = [(90, 50), (166, 110)]
    draw.arc(shackle_box, 0, 180, fill=lock_color, width=8)
    
    # Lock body (main rectangle)
    draw.rectangle(
        [(lock_left, lock_top), (lock_right, lock_bottom)],
        fill=lock_color,
        outline=highlight,
        width=4
    )
    
    # Lock keyhole
    keyhole_x = size // 2
    keyhole_y = lock_top + 40
    keyhole_radius = 8
    draw.ellipse(
        [(keyhole_x - keyhole_radius, keyhole_y - keyhole_radius),
         (keyhole_x + keyhole_radius, keyhole_y + keyhole_radius)],
        fill=bg_color,
        outline=highlight,
        width=2
    )
    
    # Add security checkmark accent
    check_x, check_y = lock_right + 15, lock_bottom - 20
    draw.line(
        [(check_x - 10, check_y), (check_x - 2, check_y + 8), (check_x + 10, check_y - 8)],
        fill=accent_color,
        width=5
    )
    
    # Save as PNG first (transparent background)
    png_path = "icon.png"
    img.save(png_path, 'PNG')
    print(f"✅ PNG icon created: {png_path}")
    
    # Convert to ICO format (Windows icon)
    ico_path = "icon.ico"
    
    # Create different sizes for the ICO file
    sizes = [(16, 16), (32, 32), (64, 64), (128, 128), (256, 256)]
    icon_images = []
    
    img_rgb = img.convert('RGB')  # Convert to RGB for ICO format
    
    for size_tuple in sizes:
        resized = img_rgb.resize(size_tuple, Image.Resampling.LANCZOS)
        icon_images.append(resized)
    
    # Save as ICO with multiple resolutions
    icon_images[4].save(ico_path, 'ICO', sizes=[s for s in sizes])
    print(f"✅ ICO icon created: {ico_path}")
    
    return png_path, ico_path

def create_icon_for_build():
    """Create icon and place it in project directory"""
    
    print("🎨 Generating SecureWipe Professional Icon...")
    print("=" * 50)
    
    png_path, ico_path = create_securewipe_icon()
    
    print("=" * 50)
    print("✅ Icon Generation Complete!")
    print(f"\n📁 Files created:")
    print(f"  • {png_path} - PNG version (transparent)")
    print(f"  • {ico_path} - Windows icon (all sizes)")
    print(f"\n🔨 Next steps:")
    print(f"  1. Update build_exe.py to use: icon_path = '{ico_path}'")
    print(f"  2. Run: python build_exe.py")
    print(f"  3. Your EXE will have the new icon!\n")

if __name__ == "__main__":
    # Create icon
    create_icon_for_build()
