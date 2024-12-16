from pathlib import Path
import io
import base64
import re

import streamlit.components.v1 as components
from PIL import Image

frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "streamlit_image_label", path=str(frontend_dir)
)

# _component_func = components.declare_component("streamlit_image_process", path="./dist")

def image_label(image_base64):
    component_value = _component_func(data = image_base64)
    return component_value