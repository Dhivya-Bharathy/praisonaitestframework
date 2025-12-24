"""
Test reporting and result visualization
"""

import json
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax


class TestReporter:
    """
    Generate test reports in various formats
    
    Usage:
        reporter = TestReporter()
        reporter.generate_report(results, format="json", output="report.json")
    """
    
    def __init__(self):
        self.console = Console()
    
    def generate_report(
        self,
        test_results: Dict[str, Any],
        format: str = "console",
        output: str = None
    ):
        """
        Generate test report
        
        Args:
            test_results: Test results from TestRunner
            format: "console", "json", "html", "junit"
            output: Output file path (optional)
        """
        if format == "console":
            self._report_console(test_results)
        elif format == "json":
            self._report_json(test_results, output)
        elif format == "html":
            self._report_html(test_results, output)
        elif format == "junit":
            self._report_junit(test_results, output)
        else:
            raise ValueError(f"Unknown format: {format}")
    
    def _report_console(self, test_results: Dict[str, Any]):
        """Print detailed console report"""
        results = test_results.get("results", [])
        summary = test_results.get("summary", {})
        
        # Overall summary
        self.console.print("\n[bold]Test Results[/bold]\n")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Test Name")
        table.add_column("Status")
        table.add_column("Duration")
        table.add_column("Details")
        
        for result in results:
            status_color = {
                "passed": "green",
                "failed": "red",
                "skipped": "yellow",
            }.get(result.status, "white")
            
            status_icon = {
                "passed": "✅",
                "failed": "❌",
                "skipped": "⏭️",
            }.get(result.status, "")
            
            details = result.error if result.error else "OK"
            if len(details) > 50:
                details = details[:47] + "..."
            
            table.add_row(
                result.test_name,
                f"[{status_color}]{status_icon} {result.status}[/{status_color}]",
                f"{result.duration:.2f}s",
                details
            )
        
        self.console.print(table)
        
        # Failed tests details
        failed_tests = [r for r in results if r.status == "failed"]
        if failed_tests:
            self.console.print("\n[bold red]Failed Tests Details[/bold red]\n")
            for result in failed_tests:
                panel = Panel(
                    f"[red]{result.error}[/red]",
                    title=f"[bold]{result.test_name}[/bold]",
                    border_style="red"
                )
                self.console.print(panel)
    
    def _report_json(self, test_results: Dict[str, Any], output: str = None):
        """Generate JSON report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": test_results.get("summary", {}),
            "results": [
                result.to_dict() for result in test_results.get("results", [])
            ]
        }
        
        json_str = json.dumps(report, indent=2)
        
        if output:
            Path(output).write_text(json_str)
            self.console.print(f"[green]Report saved to {output}[/green]")
        else:
            syntax = Syntax(json_str, "json", theme="monokai")
            self.console.print(syntax)
    
    def _report_html(self, test_results: Dict[str, Any], output: str = None):
        """Generate HTML report"""
        results = test_results.get("results", [])
        summary = test_results.get("summary", {})
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>PraisonAI Test Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            color: #666;
            font-size: 14px;
        }}
        .summary-card .value {{
            font-size: 32px;
            font-weight: bold;
        }}
        .passed {{ color: #10b981; }}
        .failed {{ color: #ef4444; }}
        .skipped {{ color: #f59e0b; }}
        table {{
            width: 100%;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #eee;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }}
        .status-passed {{
            background: #d1fae5;
            color: #065f46;
        }}
        .status-failed {{
            background: #fee2e2;
            color: #991b1b;
        }}
        .status-skipped {{
            background: #fef3c7;
            color: #92400e;
        }}
        .error-details {{
            background: #fef2f2;
            border-left: 4px solid #ef4444;
            padding: 12px;
            margin: 10px 0;
            border-radius: 4px;
            font-family: monospace;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 PraisonAI Test Report</h1>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    
    <div class="summary">
        <div class="summary-card">
            <h3>Total Tests</h3>
            <div class="value">{summary.get('total', 0)}</div>
        </div>
        <div class="summary-card">
            <h3>Passed</h3>
            <div class="value passed">{summary.get('passed', 0)}</div>
        </div>
        <div class="summary-card">
            <h3>Failed</h3>
            <div class="value failed">{summary.get('failed', 0)}</div>
        </div>
        <div class="summary-card">
            <h3>Skipped</h3>
            <div class="value skipped">{summary.get('skipped', 0)}</div>
        </div>
        <div class="summary-card">
            <h3>Duration</h3>
            <div class="value">{summary.get('duration', 0):.2f}s</div>
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Test Name</th>
                <th>Status</th>
                <th>Duration</th>
                <th>Details</th>
            </tr>
        </thead>
        <tbody>
"""
        
        for result in results:
            status_class = f"status-{result.status}"
            html += f"""
            <tr>
                <td><strong>{result.test_name}</strong></td>
                <td><span class="status-badge {status_class}">{result.status.upper()}</span></td>
                <td>{result.duration:.2f}s</td>
                <td>
"""
            if result.error:
                html += f'<div class="error-details">{result.error}</div>'
            else:
                html += "OK"
            
            html += """
                </td>
            </tr>
"""
        
        html += """
        </tbody>
    </table>
</body>
</html>
"""
        
        if output:
            Path(output).write_text(html)
            self.console.print(f"[green]HTML report saved to {output}[/green]")
        else:
            self.console.print(html)
    
    def _report_junit(self, test_results: Dict[str, Any], output: str = None):
        """Generate JUnit XML report for CI/CD"""
        results = test_results.get("results", [])
        summary = test_results.get("summary", {})
        
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<testsuites tests="{summary.get('total', 0)}" 
            failures="{summary.get('failed', 0)}" 
            skipped="{summary.get('skipped', 0)}" 
            time="{summary.get('duration', 0):.2f}">
    <testsuite name="PraisonAI Tests" 
               tests="{summary.get('total', 0)}" 
               failures="{summary.get('failed', 0)}" 
               skipped="{summary.get('skipped', 0)}" 
               time="{summary.get('duration', 0):.2f}">
"""
        
        for result in results:
            xml += f'        <testcase name="{result.test_name}" time="{result.duration:.2f}"'
            
            if result.status == "failed":
                xml += '>\n'
                xml += f'            <failure message="{self._escape_xml(result.error or "")}">'
                xml += self._escape_xml(result.error or "")
                xml += '</failure>\n'
                xml += '        </testcase>\n'
            elif result.status == "skipped":
                xml += '>\n'
                xml += '            <skipped/>\n'
                xml += '        </testcase>\n'
            else:
                xml += ' />\n'
        
        xml += """    </testsuite>
</testsuites>
"""
        
        if output:
            Path(output).write_text(xml)
            self.console.print(f"[green]JUnit report saved to {output}[/green]")
        else:
            self.console.print(xml)
    
    def _escape_xml(self, text: str) -> str:
        """Escape XML special characters"""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))

