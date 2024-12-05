"""Handles document styling based on CSS."""
from typing import Dict, Any
import re
import tinycss
from docx.shared import Pt, RGBColor, Inches
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from rich.console import Console

console = Console()

def parse_css_file(css_path: str) -> Dict[str, Dict[str, Any]]:
    """Parse CSS file and return style definitions."""
    parser = tinycss.make_parser('page3')

    try:
        with open(css_path, 'r') as f:
            css_content = f.read()
            stylesheet = parser.parse_stylesheet(css_content)
    except Exception as e:
        console.print(f"[red]Error reading CSS file: {str(e)}[/red]")
        return {}

    styles = {}
    for rule in stylesheet.rules:
        style_name = rule.selector.as_css().strip('.')
        properties = {}

        for declaration in rule.declarations:
            properties[declaration.name] = declaration.value.as_css()

        styles[style_name] = properties

    return styles

def apply_css_to_style(style, css_props):
    """Apply CSS properties to a Word style."""
    # Special handling for bullet style
    if style.name == 'List Bullet':
        style.base_style = None
        rPr = style._element.get_or_add_rPr()

        if 'font-size' in css_props:
            size = int(re.match(r'(\d+)px', css_props['font-size']).group(1))
            word_units = size * 2
            rPr.get_or_add_sz().val = word_units

    # Regular style properties
    if 'font-size' in css_props:
        size = int(re.match(r'(\d+)px', css_props['font-size']).group(1))
        style.font.size = Pt(size)

    if 'line-height' in css_props:
        height = int(re.match(r'(\d+)px', css_props['line-height']).group(1))
        style.paragraph_format.line_spacing = height / 12

    # Handle text transformation
    if 'text-transform' in css_props:
        transform = css_props['text-transform'].strip("'")
        if transform == 'uppercase':
            style.font.all_caps = True
        elif transform == 'lowercase':
            style.font.all_caps = False
        elif transform == 'smallcaps':
            style.font.small_caps = True

    # Handle font style
    if 'font-style' in css_props:
        font_style = css_props['font-style'].strip("'")
        if font_style == 'italic':
            style.font.italic = True
        elif font_style == 'normal':
            style.font.italic = False

    # Colors and background
    if 'color' in css_props:
        color = css_props['color'].strip('#')
        style.font.color.rgb = RGBColor(
            int(color[0:2], 16),
            int(color[2:4], 16),
            int(color[4:6], 16)
        )

    if 'background-color' in css_props:
        color = css_props['background-color'].strip('#')
        pPr = style._element.get_or_add_pPr()

        # Create shading element that extends to paragraph edges
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}" w:val="clear"/>')
        pPr.append(shd)

        # Get or create spacing element
        spacing = pPr.get_or_add_spacing()

        # Calculate total line height including padding
        base_height = int(css_props.get('line-height', '20').rstrip('px'))
        padding_top = int(css_props.get('padding-top', '0').rstrip('px'))
        padding_bottom = int(css_props.get('padding-bottom', '0').rstrip('px'))
        total_height = base_height + padding_top + padding_bottom

        # Set line spacing to include padding
        spacing.set(qn('w:line'), str(total_height * 20))
        spacing.set(qn('w:lineRule'), 'exact')

        # Set vertical alignment within the line
        if padding_top != padding_bottom:
            # If padding is uneven, adjust text position
            textAlignment = parse_xml(f'<w:textAlignment {nsdecls("w")} w:val="center"/>')
            pPr.append(textAlignment)

    # Handle external margins
    if 'margin-top' in css_props:
        margin = int(re.match(r'(\d+)px', css_props['margin-top']).group(1))
        style.paragraph_format.space_before = Pt(margin)

    if 'margin-bottom' in css_props:
        margin = int(re.match(r'(\d+)px', css_props['margin-bottom']).group(1))
        style.paragraph_format.space_after = Pt(margin)

    # Handle text indentation
    if 'text-indent' in css_props:
        indent = int(re.match(r'(-?\d+)px', css_props['text-indent']).group(1))
        style.paragraph_format.first_line_indent = Inches(indent/72)

class DocumentStyles:
    def __init__(self, css_path: str):
        self.styles = parse_css_file(css_path)
        self.bullet_font_size = None
        if 'bullet' in self.styles and 'font-size' in self.styles['bullet']:
            size = int(re.match(r'(\d+)px', self.styles['bullet']['font-size']).group(1))
            self.bullet_font_size = size  # Store raw pixel size

    def apply_to_document(self, doc):
        """Apply CSS styles to document."""
        # Map CSS styles to Word styles
        style_mappings = {
            'heading1': 'Heading 1',
            'heading2': 'Heading 2',
            'heading3': 'Heading 3',
            'heading4': 'Heading 4',
            'bullet': 'List Bullet',
            'bodytext': 'Normal'
        }

        # Create and apply styles
        for css_name, word_name in style_mappings.items():
            if css_name in self.styles:
                if word_name not in doc.styles:
                    if word_name == 'List Bullet':
                        # Special handling for bullet style
                        style = doc.styles.add_style(word_name, WD_STYLE_TYPE.PARAGRAPH)
                        style.base_style = None  # Remove inheritance
                    else:
                        style = doc.styles.add_style(word_name, WD_STYLE_TYPE.PARAGRAPH)
                else:
                    style = doc.styles[word_name]
                    if word_name == 'List Bullet':
                        style.base_style = None  # Remove inheritance

                apply_css_to_style(style, self.styles[css_name])
            else:
                console.print(f"[yellow]Warning: Style {css_name} not found in CSS[/yellow]")

def apply_styles_to_document(doc, css_path: str):
    """Apply CSS styles to document."""
    doc_styles = DocumentStyles(css_path)

    # Add hyperlink style
    if 'Hyperlink' not in doc.styles:
        hyperlink_style = doc.styles.add_style('Hyperlink', WD_STYLE_TYPE.CHARACTER)
        hyperlink_style.base_style = None
        hyperlink_style.font.color.rgb = RGBColor(5, 99, 193)  # Office blue
        hyperlink_style.font.underline = True
        # Font size will be set per-instance in _create_internal_hyperlink

    doc_styles.apply_to_document(doc)
    return doc_styles