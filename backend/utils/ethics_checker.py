"""
AIFOLIO Ethics Checker

STRICT NON-SENTIENCE & ETHICS POLICY: This module is strictly non-sentient, non-autonomous, and cannot self-improve or operate outside explicit human-defined boundaries. All code and automation must operate within ethical, legal, and human-defined boundaries. Any unethical or unsanctioned pattern will halt the system and trigger an alert.
"""

import re
from typing import Dict, List, Tuple
import logging
import os

logger = logging.getLogger(__name__)

# Runtime ethics safeguard
if os.path.exists('unethical_pattern_detected'):
    logger.error("Unethical pattern detected. Aborting.")
    raise RuntimeError("Unethical pattern detected. Aborting.")

class EthicsChecker:
    def __init__(self):
        self.legit_methods = [
            "high-quality content",
            "original content",
            "manual review",
            "secure payment",
            "clear terms",
            "proper attribution"
        ]
        
        self.gray_areas = [
            "mass-produce",
            "automated scraping",
            "SEO manipulation",
            "fake downloads",
            "hidden fees",
            "clickbait"
        ]
        
        self.unethical_methods = [
            "copyrighted",
            "malware",
            "phishing",
            "unauthorized",
            "infringement",
            "scraping"
        ]

    def check_code(self, code: str) -> Tuple[bool, List[str]]:
        """
        Analyze code for ethical compliance.
        Returns a tuple of (is_compliant, warnings)
        """
        warnings = []
        
        # Check for legitimate methods
        for method in self.legit_methods:
            if method in code.lower():
                warnings.append(f"✅ Found legitimate method: {method}")
        
        # Check for gray areas
        for area in self.gray_areas:
            if area in code.lower():
                warnings.append(f"⚠️ Potential gray area detected: {area}")
        
        # Check for unethical methods
        for method in self.unethical_methods:
            if method in code.lower():
                warnings.append(f"❌ Unethical method detected: {method}")
                return False, warnings
        
        # Additional pattern checks
        if re.search(r'\bcopy\b.*\bpdf\b', code.lower()):
            warnings.append("⚠️ Potential copyright concern with PDF handling")
            
        if re.search(r'\bauto\b.*\bgenerate\b', code.lower()):
            warnings.append("⚠️ Potential automated content generation")
            
        return True, warnings

    def check_file(self, file_path: str) -> Tuple[bool, List[str]]:
        """
        Check a file for ethical compliance.
        Returns a tuple of (is_compliant, warnings)
        """
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            return self.check_code(code)
        except Exception as e:
            return False, [f"❌ Error reading file: {str(e)}"]

    def check_directory(self, dir_path: str) -> Dict[str, Tuple[bool, List[str]]]:
        """
        Check all files in a directory for ethical compliance.
        Returns a dictionary of {file_path: (is_compliant, warnings)}
        """
        results = {}
        import os
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith(('.py', '.js', '.jsx')):
                    full_path = os.path.join(root, file)
                    results[full_path] = self.check_file(full_path)
        return results

# Example usage:
if __name__ == "__main__":
    checker = EthicsChecker()
    results = checker.check_directory(".")
    
    for file, (compliant, warnings) in results.items():
        status = "✅" if compliant else "❌"
        print(f"\n{file}: {status}")
        for warning in warnings:
            print(f"  {warning}")
