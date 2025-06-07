import os
import re
from typing import Dict, List, Tuple

class CodebaseScanner:
    def __init__(self):
        self.ethical_patterns = {
            # Legitimate automation patterns
            'testing': r'(test|pytest|unittest)',
            'deployment': r'(deploy|release|update)',
            'security': r'(security|auth|encryption)',
            'monitoring': r'(monitor|log|audit)',
            'optimization': r'(optimize|performance)',
            'accessibility': r'(accessibility|a11y)',
            'validation': r'(validate|check|verify)',
            'backup': r'(backup|restore)',
            'analytics': r'(analytics|metrics|stats)',
            'documentation': r'(doc|docs|readme)',
            'personalization': r'(personalize|recommend)',
            'user_feedback': r'(feedback|survey|review)',
            'error_handling': r'(error|exception|try)',
            'logging': r'(log|logger)',
            'version_control': r'(git|version|history)',
            'encryption': r'(encrypt|decrypt|hash)',
            'privacy': r'(privacy|gdpr|ccpa)',
            'compliance': r'(compliance|regulation)',
            'user_control': r'(user|auth|permission)',
            'data_quality': r'(data|validate|clean)',
            'performance': r'(perf|optimize|speed)',
            'security_updates': r'(update|patch|fix)',
            'access_control': r'(access|permission|role)',
            'audit': r'(audit|trail|log)',
        }
        
        self.unethical_patterns = {
            # Unethical automation patterns
            'scraping': r'(scrape|crawl|grab)',
            'spam': r'(spam|bulk|mass)',
            'malware': r'(malware|virus|trojan)',
            'infringement': r'(copy|clone|duplicate)',
            'false_info': r'(fake|false|mislead)',
            'privacy_violation': r'(steal|grab|take)',
            'manipulation': r'(manipulate|cheat|fake)',
            'violation': r'(violate|break|hack)',
            'unauthorized': r'(unauthorized|force)',
            'deception': r'(deceive|trick|fake)',
            'fraud': r'(fraud|scam|phish)',
            'violation': r'(violate|break|hack)',
            'unauthorized': r'(unauthorized|force)',
            'deception': r'(deceive|trick|fake)',
            'fraud': r'(fraud|scam|phish)',
        }

    def scan_file(self, file_path: str) -> Dict[str, List[str]]:
        """Scan a single file for ethical automation patterns."""
        results = {
            'ethical': [],
            'unethical': [],
            'warnings': []
        }
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
                # Check for ethical patterns
                for pattern_name, pattern in self.ethical_patterns.items():
                    if re.search(pattern, content, re.IGNORECASE):
                        results['ethical'].append(f"✅ Found ethical pattern '{pattern_name}'")
                
                # Check for unethical patterns
                for pattern_name, pattern in self.unethical_patterns.items():
                    if re.search(pattern, content, re.IGNORECASE):
                        results['unethical'].append(f"❌ Found unethical pattern '{pattern_name}'")
                
                # Additional checks
                if 'scrape' in content.lower() and not any(
                    x in content.lower() for x in ['test', 'unit', 'mock', 'example']
                ):
                    results['warnings'].append("⚠️ Potential scraping without proper context")
                    
                if 'copy' in content.lower() and not any(
                    x in content.lower() for x in ['test', 'unit', 'mock', 'example']
                ):
                    results['warnings'].append("⚠️ Potential copyright concerns")
                    
                return results
                
        except Exception as e:
            results['warnings'].append(f"❌ Error reading file: {str(e)}")
            return results

    def scan_directory(self, dir_path: str) -> Dict[str, Dict[str, List[str]]]:
        """Scan entire directory for ethical automation patterns."""
        results = {}
        
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith(('.py', '.js', '.jsx', '.ts', '.tsx')):
                    full_path = os.path.join(root, file)
                    results[full_path] = self.scan_file(full_path)
        
        return results

    def generate_report(self, scan_results: Dict[str, Dict[str, List[str]]]) -> str:
        """Generate a detailed report of the scan results."""
        report = "AIFOLIO V12 Codebase Ethics Report\n"
        report += "===================================\n\n"
        
        total_files = len(scan_results)
        ethical_files = 0
        unethical_files = 0
        warning_files = 0
        
        for file_path, results in scan_results.items():
            if results['unethical']:
                unethical_files += 1
                report += f"\n❌ Unethical Patterns Found in {file_path}:\n"
                for issue in results['unethical']:
                    report += f"  {issue}\n"
            
            if results['warnings']:
                warning_files += 1
                report += f"\n⚠️ Warnings in {file_path}:\n"
                for warning in results['warnings']:
                    report += f"  {warning}\n"
            
            if results['ethical']:
                ethical_files += 1
                report += f"\n✅ Ethical Patterns in {file_path}:\n"
                for pattern in results['ethical']:
                    report += f"  {pattern}\n"
        
        report += "\nSummary:\n"
        report += f"Total files scanned: {total_files}\n"
        report += f"Files with ethical patterns: {ethical_files}\n"
        report += f"Files with unethical patterns: {unethical_files}\n"
        report += f"Files with warnings: {warning_files}\n"
        
        return report

# Example usage
if __name__ == "__main__":
    scanner = CodebaseScanner()
    results = scanner.scan_directory(".")
    report = scanner.generate_report(results)
    print(report)
