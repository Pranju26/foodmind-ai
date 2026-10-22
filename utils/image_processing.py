"""
Image processing utilities for FoodMind AI
Handles food image validation, resizing, and processing using Pillow
"""

from PIL import Image
import io


def validate_image(uploaded_file, max_size_mb=5):
    """
    Validate uploaded image file
    
    Args:
        uploaded_file: Streamlit uploaded file object
        max_size_mb: Maximum file size in megabytes
    
    Returns:
        Tuple (is_valid, error_message)
    """
    if uploaded_file is None:
        return False, "No file uploaded"
    
    # Check file size
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return False, f"File size exceeds {max_size_mb}MB limit"
    
    # Check file type
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
    if uploaded_file.type not in allowed_types:
        return False, "File must be JPEG, PNG, or WebP format"
    
    # Try to open as image
    try:
        image = Image.open(uploaded_file)
        image.verify()
        return True, None
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"


def process_food_image(uploaded_file, max_width=800, max_height=800):
    """
    Process and resize uploaded food image
    
    Args:
        uploaded_file: Streamlit uploaded file object
        max_width: Maximum width for resized image
        max_height: Maximum height for resized image
    
    Returns:
        PIL Image object or None if processing fails
    """
    try:
        # Open image
        image = Image.open(uploaded_file)
        
        # Convert RGBA to RGB if necessary
        if image.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])  # Use alpha channel as mask
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if needed
        original_width, original_height = image.size
        
        if original_width > max_width or original_height > max_height:
            # Calculate aspect ratio
            ratio = min(max_width / original_width, max_height / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            # Resize with high-quality resampling
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return image
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def get_image_info(image):
    """
    Get information about an image
    
    Args:
        image: PIL Image object
    
    Returns:
        Dictionary with image information
    """
    if image is None:
        return None
    
    return {
        'width': image.width,
        'height': image.height,
        'mode': image.mode,
        'format': image.format
    }


def image_to_bytes(image, format='JPEG', quality=85):
    """
    Convert PIL Image to bytes
    
    Args:
        image: PIL Image object
        format: Output format (JPEG, PNG, etc.)
        quality: JPEG quality (1-100)
    
    Returns:
        Image as bytes
    """
    if image is None:
        return None
    
    try:
        buffer = io.BytesIO()
        image.save(buffer, format=format, quality=quality)
        return buffer.getvalue()
    except Exception as e:
        print(f"Error converting image to bytes: {e}")
        return None


def create_thumbnail(image, size=(200, 200)):
    """
    Create a thumbnail of an image
    
    Args:
        image: PIL Image object
        size: Tuple of (width, height) for thumbnail
    
    Returns:
        Thumbnail PIL Image object
    """
    if image is None:
        return None
    
    try:
        thumbnail = image.copy()
        thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
        return thumbnail
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return None
