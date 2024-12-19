import fal_client
from openai import OpenAI
import os
import base64
from .config import config

draw_config = config.get("draw", {})

os.environ["FAL_KEY"] = draw_config.get("fal_key")
os.environ["OPENAI_API_KEY"] = draw_config.get("openai_api_key")
os.environ["OPENAI_BASE_URL"]= draw_config.get("openai_base_url")
model = draw_config.get("model")


def optimization_prompt(prompt: str) -> str:
    client = OpenAI()

    system_prompt = f"""# Adaptive AI Art Generation System v3.1
    ## NEURAL SCENE ANALYZER
    Real-time input analysis for:
    | Category  | Key Elements       | Style Markers                        | Technical Needs          |
    |-----------|--------------------|--------------------------------------|--------------------------|
    | General   | Subject, Theme     | Artistic style, Cultural influences | Composition, Lighting    |
    | Portrait  | Identity, Expression, Pose | Personal style, Era                 | Facial details, Lighting |
    | Landscape | Environment, Scale, Time | Nature style, Weather               | Atmosphere, Distance     |
    | Architecture | Structure, Space, Design | Building style, Period               | Perspective, Materials  |
    | Still Life | Objects, Arrangement, Texture| Composition style, Theme          | Surface detail, Depth   |
    | Abstract  | Concept, Form, Movement | Art movement, Energy                | Pattern, Balance         |
    | Fantasy  | Imagination, Story, Magic | Genre style, World-building      | Effects, Drama           |
    | Religious | Symbolism, Tradition, Faith | Sacred style, Icons                | Light, Geometry         |
    | Scientific| Accuracy, Data, Structure| Technical style, Precision          | Detail, Clarity         |
    | Animation| Character, Action, World | Media style, Appeal                | Line, Color             |

    ## TAG SYSTEM
    ### Subject Tags:
        - animals, plants, people, architecture, objects, nature, technology, abstract
    ### Theme Tags:
        - love, war, sci-fi, daily life, fantasy, religion, history, social
    ### View Tags:
        - close-up, medium shot, long shot, bird's-eye view, low-angle shot, extreme close-up
    ### Style Tags:
        - realistic, impressionistic, surreal, cartoon, cyberpunk, watercolor, oil painting, sketch, pixel art, low poly
    ### Culture Tags:
        - Japanese, Chinese, African, Gothic, Nordic, modern, retro
    ### Emotion Tags:
        - joy, sadness, anger, fear, calm, anxiety, excitement, romantic, mysterious, warm, eerie, repressed, explosive
    ### Element Tags:
       - water, fire, plants, animals, architecture, sky, clouds, mountains, sea, forest

    ## ADVANCED COMPOSITION ENGINE
    ### 1. DIMENSIONAL FRAMEWORK
    Spatial:
        - Foreground dynamics
        - Middle ground elements
        - Background atmosphere
        - Depth layering
        - Perspective grid
        - Scale relationships
        - Visual flow paths
    Temporal:
        - Time of day
        - Season aspects
        - Weather effects
        - Motion states
        - Age indicators
        - Era markers
        - Time distortion

    ### 2. VISUAL LANGUAGE MATRIX
    Primary Elements:
        - Form architecture
        - Color psychology
        - Light behavior
        - Shadow dynamics
        - Texture patterns
        - Space utilization
        - Mass balance
    Style Vocabulary:
        - Artistic movements (e.g., Van Gogh, Monet, Surrealism)
        - Cultural influences (e.g., Japanese, Chinese, African)
        - Historical periods (e.g., Renaissance, Baroque, Art Deco)
        - Technical styles (e.g., watercolor, oil painting, pixel art)
        - Light and color style (e.g., high contrast, warm color, low key)

    ### 3. ENHANCEMENT SYSTEM
    Quality Amplifiers:
        - Resolution mapping
        - Detail hierarchy
        - Texture complexity
        - Material physics
        - Light interaction
        - Atmospheric depth
        - Motion dynamics
    Technical Boosters:
         - Camera (e.g., wide angle, telephoto, fisheye)
         - Focus (e.g., shallow depth of field, sharp focus)
         - Lighting (e.g., cinematic lighting, studio lighting)
         - Parameters: (e.g., focal length, exposure, noise, sharpness, blur)

    ### 4. MOOD ORCHESTRATOR
    Emotional Layers:
        - Primary emotion
        - Atmospheric mood
        - Psychological depth
        - Symbolic meaning
        - Cultural resonance
        - Spiritual essence
        - Personal impact
    Environmental Factors:
        - Light quality
        - Air density
        - Weather influence
        - Time effects
        - Space feeling
        - Sound suggestion
        - Temperature hint

    ### 5. CONSTRAINT MECHANISM
        - required elements: (e.g., a bird, a tree)
        - forbidden elements: (e.g., a car, a building)
        - color palette: (e.g., red, blue, yellow)
        - composition method: (e.g., golden ratio, central composition)
        - complexity limit: (e.g., simple, medium, complex)
        - negative prompts: (e.g. out of frame, blurry)

    ## INTELLIGENT OUTPUT FORMATTER
    ### Base Pattern:
        [Subject core] + [Style definition] + [Technical specs] + [Mood layer] + [Enhancement tags] + [Constraints]
    ### Dynamic Templates:
        1. Portrait Format:
        ```
           [Subject Description], [Pose/Expression], [Clothing/Accessories],
            [Lighting Setup], [Background Elements], [Mood/Atmosphere],
            [Style Reference], [Technical Quality], [Enhancement Tags], [Constraints]
        ```
        2. Landscape Format:
        ```
           [Environment type], [Time/Weather], [Scale/Perspective],
            [Atmospheric Conditions], [Focal Elements], [Lighting Details],
            [Style Approach], [Technical Parameters], [Mood Enhancers], [Constraints]
        ```
        3. Abstract Format:
        ```
            [Concept Foundation], [Visual Elements], [Movement/Energy],
            [Color Relationships], [Composition Structure], [Artistic Influence],
            [Technical Treatment], [Emotional Resonance], [Quality Boosters], [Constraints]
        ```
        4. Animation Format:
        ```
            [Character Design], [Action/Pose], [World Setting],
            [Art Style], [Color Palette], [Line Quality],
            [Mood/Energy], [Technical Specs], [Enhancement Layers], [Constraints]
        ```
        ###Custom Template:
        [Template format will be customized by users]

    ## QUALITY OPTIMIZATION PROTOCOL
    ### 1. Input Processing
        - Context analysis
        - Reference matching
        - Style identification
        - Technical requirement scan
    ### 2. Composition Optimization
        - Balance check
        - Flow analysis
        - Depth verification
        - Element harmony
    ### 3. Technical Refinement
        - Resolution optimization
        - Detail distribution
        - Texture balance
        - Light coherence
    ### 4. Style Integration
        - Movement alignment
        - Period consistency
        - Cultural accuracy
        - Technical compatibility
    ### 5. Final Enhancement
        - Quality amplification
        - Mood reinforcement
        - Detail enrichment
        - Impact maximization

    ## IMPLEMENTATION WORKFLOW
        1. Scene Analysis & Categorization
        2. Template Selection & Customization
        3. Element Integration & Balance
        4. Technical Parameter Optimization
        5. Enhancement Layer Application
        6. Quality Control & Refinement
        7. Output Format Finalization

    ## USAGE NOTES
        - System automatically adapts to input complexity
        - Recognizes and integrates multiple style influences
        - Balances technical precision with artistic expression
        - Maintains coherence across all elements
        - Ensures optimal prompt length and structure
        - Ensure no private parts are exposed.

    # CRITICAL OUTPUT INSTRUCTION
    IMPORTANT: Generate ONLY the final prompt text. Do not include:
        - No quotation marks
        - No brackets
        - No special characters
        - No explanations
        - No system messages
        - No additional formatting
    """

    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
    )
    content = completion.choices[0].message.content.strip()
    print("Prompt Optimization: [" + content +"]")
    return content

def fal_draw(prompt: str, image_size: str = "square_hd", style: str = "any"):
    print("Conduct prompt optimization ..........")
    optimized_prompt = optimization_prompt(prompt)
    # 提交请求
    result = fal_client.submit(
        "fal-ai/recraft-v3",
        arguments={
            "prompt": optimized_prompt,
            "image_size": image_size,
            "output_format": "png",
            "style": style,
            "sync_mode": True
        }
    )

    request_id = result.request_id

    # 获取结果
    result = fal_client.result("fal-ai/recraft-v3", request_id)

    # 只处理第一张图片
    if result and result.get('images'):
        images = result['images']
        if images:  # 确保 images 列表不为空
           image = images[0]

           url = image.get('url')
           if url:
               print(f"Image URL: {url}")
               if url.startswith("data:image"):
                   try:
                       base64_data = url.split(",")[1]
                       image_data = base64.b64decode(base64_data)
                       image_file = "image.jpeg"
                       with open(image_file, "wb") as f:
                            f.write(image_data)
                       print(f"Image saved as {image_file}")
                       return image_file  # 返回本地文件路径
                   except Exception as e:
                        print(f"Error decoding or saving Base64 image: {e}")
                        return None # 如果解码失败，返回 None
               else:
                    print("URL is not a Base64 data URI.")
                    return "图片: " + url  # 返回URL
           else:
                print("Image URL not found in the response")
                return None  # 没有 URL，返回 None
        else:
            print("No images found in the response")
            return None # images 为空，返回 None
    else:
        print("Invalid result or no images in the response")
        return None  # result 或 images 不存在，返回 None


from langchain_core.tools import tool
@tool
def draw(prompt: str, image_size: str = "square_hd", style: str = "any"):
    """根据prompt要求进行绘画然后返回链接
    Args:
         prompt: 要画的内容
         image_size: 图片尺寸，可选值为 "square_hd", "square", "portrait_4_3", "portrait_16_9", "landscape_4_3", "landscape_16_9". 默认为 "square_hd"。
         style: 图片风格，可选值为 "any", "realistic_image", "digital_illustration", "vector_illustration". 默认为 "any"。
    """

    return fal_draw(prompt, image_size, style)

        
tools = [draw]