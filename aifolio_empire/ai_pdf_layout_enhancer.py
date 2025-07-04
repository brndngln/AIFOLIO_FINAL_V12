import fitz  # PyMuPDF
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIPDFLayoutEnhancer:
    """Enhances PDF layouts with AI-driven formatting."""
    
    def __init__(self):
        """Initialize the layout enhancer."""
        self.layout_sections = {
            'pain': {
                'styles': {
                    'font_size': 12,
                    'color': '#FF0000',
                    'bold': True,
                    'highlight': True
                },
                'markers': ['Problem', 'Challenge', 'Issue']
            },
            'promise': {
                'styles': {
                    'font_size': 14,
                    'color': '#00FF00',
                    'bold': True,
                    'highlight': False
                },
                'markers': ['Solution', 'Result', 'Outcome']
            },
            'proof': {
                'styles': {
                    'font_size': 11,
                    'color': '#0000FF',
                    'bold': False,
                    'highlight': True
                },
                'markers': ['Evidence', 'Case Study', 'Example']
            },
            'result': {
                'styles': {
                    'font_size': 16,
                    'color': '#FF00FF',
                    'bold': True,
                    'highlight': True
                },
                'markers': ['Success', 'Achievement', 'Transformation']
            }
        }
        
    def analyze_content(self, text: str) -> Dict[str, List[str]]:
        """Analyze content and categorize into sections."""
        sections = {key: [] for key in self.layout_sections}
        
        # Split text into paragraphs
        paragraphs = text.split('\n\n')
        
        for para in paragraphs:
            if not para.strip():
                continue
                
            # Determine section based on markers
            section = None
            for key, config in self.layout_sections.items():
                if any(marker.lower() in para.lower() for marker in config['markers']):
                    section = key
                    break
                    
            if section:
                sections[section].append(para)
                
        return sections
        
    def enhance_layout(self, input_path: str, output_path: str) -> None:
        """Enhance PDF layout with formatted sections."""
        try:
            # Open PDF
            doc = fitz.open(input_path)
            
            # Process each page
            for page in doc:
                # Get text
                text = page.get_text()
                
                # Analyze content
                sections = self.analyze_content(text)
                
                # Clear page and rebuild with enhanced layout
                page.clean_contents()
                
                # Add enhanced content
                y_pos = 72  # Starting position
                for section_name, paras in sections.items():
                    if not paras:
                        continue
                        
                    # Add section header
                    config = self.layout_sections[section_name]
                    header = section_name.upper()
                    page.insert_text(
                        (72, y_pos),
                        header,
                        fontsize=18,
                        color=(0, 0, 0),
                        fontname="helv"
                    )
                    y_pos += 30
                    
                    # Add content
                    for para in paras:
                        page.insert_text(
                            (72, y_pos),
                            para,
                            fontsize=config['styles']['font_size'],
                            color=self._hex_to_rgb(config['styles']['color']),
                            fontname="helv",
                            bold=config['styles']['bold']
                        )
                        y_pos += 20
                        
                        # Add highlight if needed
                        if config['styles']['highlight']:
                            text_instances = page.search_for(para)
                            for inst in text_instances:
                                highlight = page.add_highlight_annot(inst)
                                highlight.update()
                                
            # Save enhanced PDF
            doc.save(output_path)
            logger.info(f"Enhanced PDF saved to {output_path}")
            
        except Exception as e:
            logger.error(f"Error enhancing PDF layout: {e}")
            raise
            
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))

# Example usage
if __name__ == "__main__":
    enhancer = AIPDFLayoutEnhancer()
    enhancer.enhance_layout("input.pdf", "enhanced_output.pdf")
