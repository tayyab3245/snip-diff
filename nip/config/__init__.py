"""
================================================================================
SNIP-DIFF - AI workflow tool for preparing code context outside agentic environments
================================================================================

Copyright (c) 2025 Tayyab. All Rights Reserved.

PROPRIETARY AND CONFIDENTIAL

This software and associated documentation files (the "Software") are the 
exclusive property of the copyright holder. This Software contains proprietary 
and confidential information and is protected by copyright laws and 
international treaty provisions.

RESTRICTIONS:
- No part of this Software may be reproduced, distributed, or transmitted 
  in any form or by any means without the prior written permission of the 
  copyright holder.
- This Software is not for sale, license, or distribution to third parties.
- Reverse engineering, decompilation, or disassembly of this Software is 
  strictly prohibited.
- Any unauthorized use, copying, or distribution may result in severe civil 
  and criminal penalties.

This Software is provided "AS IS" without warranty of any kind, express or 
implied, including but not limited to the warranties of merchantability, 
fitness for a particular purpose, and non-infringement.

For licensing inquiries, please contact: tayyab3245@github.com
================================================================================
"""


from .defaults import IGNORE_LIST, SNAPSHOT_FILE
from .theme import theme_manager, get_theme, apply_theme_to_widget, get_component_color, ThemeManager, STYLE
from .tokens import DESIGN_TOKENS
from .dark_theme_new import generate_dark_qss, DARK_UNIFIED
from .light_theme_fixed import generate_light_qss, LIGHT_UNIFIED

# Legacy compatibility
__all__ = [
    'IGNORE_LIST', 'SNAPSHOT_FILE', 
    'theme_manager', 'get_theme', 'apply_theme_to_widget', 'get_component_color', 'ThemeManager',
    'DESIGN_TOKENS', 'generate_dark_qss', 'DARK_UNIFIED', 'generate_light_qss', 'LIGHT_UNIFIED',
    'STYLE'  # Legacy support
]
