from dataclasses import dataclass, field
from typing import Optional, List
from PIL import Image

@dataclass
class PipelineState:
    # New consultation inputs
    duration: str = ""
    worsening: str = ""
    pain_level: str = ""
    skincare_routine: str = ""
    new_products: str = ""
    stress_change: str = ""
    sleep_change: str = ""
    image: Optional[Image.Image] = None
    image_base64: Optional[str] = None
    manual_type_override: Optional[str] = None

    # Intermediate results
    predicted_class: Optional[str] = None   # from image model
    image_result: Optional[str] = None      # severity from image model
    image_confidence: Optional[float] = None # raw confidence score
    all_predictions: dict = field(default_factory=dict)
    confidence_label: Optional[str] = None  # High / Medium / Low
    lifestyle_result: Optional[str] = None  # adjusted severity
    main_trigger: Optional[str] = None      # single prioritized trigger
    rag_chunks: List[str] = field(default_factory=list)
    recommended_products: List[dict] = field(default_factory=list)

    # Final output
    final_severity: Optional[str] = None
    ai_text: Optional[str] = None
    is_safe: bool = True
