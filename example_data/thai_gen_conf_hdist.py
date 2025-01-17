import inspect
import os
from pathlib import Path
import imgaug.augmenters as iaa

from text_renderer.effect import *
from text_renderer.corpus import *
from text_renderer.config import (
    RenderCfg,
    NormPerspectiveTransformCfg,
    GeneratorCfg,
)
from text_renderer.layout.same_line import SameLineLayout
from text_renderer.layout.extra_text_line import ExtraTextLineLayout

CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
OUT_DIR = CURRENT_DIR / "output"
DATA_DIR = CURRENT_DIR
BG_DIR = DATA_DIR / "bg"
CHAR_DIR = DATA_DIR / "char"
FONT_DIR = DATA_DIR / "font"
FONT_LIST_DIR = DATA_DIR / "font_list"
TEXT_DIR = DATA_DIR / "text"

font_cfg = dict(
    font_dir=FONT_DIR,
    font_list_file=FONT_LIST_DIR / "font_list.txt",
    font_size=(100, 101),
)

perspective_transform = NormPerspectiveTransformCfg(20, 20, 1.5)

def base_cfg(
    name: str, corpus, corpus_effects=None, layout_effects=None, layout=None, gray=False, height=30
):
    return GeneratorCfg(
        num_image=12500, # TODO: Edit num_image here
        save_dir=OUT_DIR / name,
        render_cfg=RenderCfg(
            bg_dir=BG_DIR,
            perspective_transform = perspective_transform,
            gray=gray,
            layout_effects=layout_effects,
            corpus=corpus,
            corpus_effects=corpus_effects,
            height = height
            
        ),
        
    )

def th_word_data(height=30):
    return base_cfg(
        inspect.currentframe().f_code.co_name,
        height=height,
        corpus= EnumCorpus(
                    EnumCorpusCfg(
                        text_paths=[TEXT_DIR / "th_text.txt"],
                        filter_by_chars=True,
                        chars_file=CHAR_DIR / "th.txt",
                        **font_cfg
                    )
                ),
        corpus_effects = 
            Effects(
                [
                    Padding(p=1, w_ratio=[0.2, 0.21], h_ratio=[0.7, 0.71], center=True),
                    DropoutRand(p=1, dropout_p=(0.2, 0.4)),
                    DropoutHorizontal(p=0.1, num_line=2, thickness=3),
                    DropoutVertical(p=0.1, num_line=15),
                    Line(p=0.05, thickness=(3, 4), line_pos_p=[1,0,0,0,0,0,0,0,0,0]),
                    Line(p=0.05, thickness=(3, 4), line_pos_p=[0,1,0,0,0,0,0,0,0,0]),
                    Line(p=0.05, thickness=(3, 4), line_pos_p=[0,0,1,0,0,0,0,0,0,0]),
                    Line(p=0.05, thickness=(3, 4), line_pos_p=[0,0,0,1,0,0,0,0,0,0]),
                    Line(p=0.05, thickness=(3, 4), line_pos_p=[0,0,0,0,1,0,0,0,0,0]),
                    Line(p=0.05, thickness=(3, 4), line_pos_p=[0,0,0,0,0,1,0,0,0,0]),
                    Line(p=0.05, thickness=(3, 4), line_pos_p=[0,0,0,0,0,0,1,0,0,0]),
                    Line(p=0.05, thickness=(3, 4), line_pos_p=[0,0,0,0,0,0,0,1,0,0]),
                    Line(p=0.05, thickness=(3, 4), line_pos_p=[0,0,0,0,0,0,0,0,1,0]),
                    Line(p=0.05, thickness=(3, 4), line_pos_p=[0,0,0,0,0,0,0,0,0,1])
                ]
            )
        
    )
    
# fmt: off
# The configuration file must have a configs variable
configs = [
    th_word_data(i) for i in range(30, 110, 5)
]
# fmt: on

# python .\main.py --config .\example_data\thai_gen_conf.py