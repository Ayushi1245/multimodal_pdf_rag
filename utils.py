import base64
import io
import time
from PIL import Image
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import config

def resize_image_to_base64(image: Image.Image, max_size=(800, 800)) -> str:
    """Resize image and convert to base64."""
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    if image.mode != "RGB":
        image = image.convert("RGB")
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def describe_image_with_groq(b64_image: str) -> str:
    """Use Groq Vision to describe an image."""
    model = ChatGroq(
        model=config.SUMMARIZER_MODEL,
        api_key=config.GROQ_API_KEY,
        max_tokens=500,
    )
    prompt = """Describe this image in extreme detail.
Focus on: exact numbers, axis labels, legend entries,
trend direction, anomalies, and key takeaways."""
    
    msg = model.invoke(
        [HumanMessage(content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}
            }
        ])]
    )
    # Slight rate limit backoff to avoid strict free tier limits
    time.sleep(2)
    return msg.content
