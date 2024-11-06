from pathlib import Path
import io
import base64
import re

import streamlit.components.v1 as components
from PIL import Image

frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "streamlit_latex_render", path=str(frontend_dir)
)

# _component_func = components.declare_component("streamlit_latex_render", path="./dist")

def latex_render(text):
    component_value = _component_func(data = text)
    return component_value