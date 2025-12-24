"""
Test runner for AI agent tests
"""

import time
from typing import List, Type, Dict, Any
from pathlib import Path
import importlib.util
import sys
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from praisonai_test.agent_test import AgentTest, TestResult


class TestRunner:
    """
    Run AI agent tests and collect results
    
    Usage:
        runner = TestRunner()
        runner.discover_tests("tests/")
        results = runner.run_all()
    """
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.console = Console()
        self.test_classes: List[Type[AgentTest]] = []
        self.test_files: List[Path] = []
        
    def discover_tests(self, path: str = "tests"):
        """Discover test files and classes"""
        test_path = Path(path)
        
        if not test_path.exists():
            self.console.print(f"[red]Test path not found: {path}[/red]")
            return
        
        # Find all test_*.py files
        if test_path.is_file():
            self.test_files = [test_path]
        else:
            self.test_files = list(test_path.rglob("test_*.py"))
        
        # Load test classes
        for test_file in self.test_files:
            self._load_test_file(test_file)
        
        if self.verbose:
            self.console.print(f"[green]Discovered {len(self.test_files)} test files[/green]")
            self.console.print(f"[green]Found {len(self.test_classes)} test classes[/green]")
    
    def _load_test_file(self, file_path: Path):
        """Load test classes from a Python file"""
        spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[file_path.stem] = module
            spec.loader.exec_module(module)
            
            # Find AgentTest subclasses
            for name in dir(module):
                obj = getattr(module, name)
                if (isinstance(obj, type) and 
                    issubclass(obj, AgentTest) and 
                    obj is not AgentTest):
                    self.test_classes.append(obj)
    
    def run_all(self) -> Dict[str, Any]:
        """Run all discovered tests"""
        all_results = []
        total_passed = 0
        total_failed = 0
        total_skipped = 0
        start_time = time.time()
        
        if self.verbose:
            self.console.print("\n[bold]Running AI Agent Tests[/bold]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            disable=not self.verbose
        ) as progress:
            
            for test_class in self.test_classes:
                task = progress.add_task(
                    f"Running {test_class.__name__}...",
                    total=None
                )
                
                test_instance = test_class()
                results = self._run_test_class(test_instance)
                all_results.extend(results)
                
                passed = sum(1 for r in results if r.status == "passed")
                failed = sum(1 for r in results if r.status == "failed")
                skipped = sum(1 for r in results if r.status == "skipped")
                
                total_passed += passed
                total_failed += failed
                total_skipped += skipped
                
                progress.remove_task(task)
                
                if self.verbose:
                    status = "✅" if failed == 0 else "❌"
                    self.console.print(
                        f"{status} {test_class.__name__}: "
                        f"{passed} passed, {failed} failed, {skipped} skipped"
                    )
        
        duration = time.time() - start_time
        
        # Print summary
        if self.verbose:
            self._print_summary(total_passed, total_failed, total_skipped, duration)
        
        return {
            "results": all_results,
            "summary": {
                "total": len(all_results),
                "passed": total_passed,
                "failed": total_failed,
                "skipped": total_skipped,
                "duration": duration,
            }
        }
    
    def _run_test_class(self, test_instance: AgentTest) -> List[TestResult]:
        """Run all test methods in a test class"""
        results = []
        
        # Find all test methods
        test_methods = [
            getattr(test_instance, name)
            for name in dir(test_instance)
            if name.startswith("test_") and callable(getattr(test_instance, name))
        ]
        
        for test_method in test_methods:
            # Check if marked as agent test
            if hasattr(test_method, "_is_agent_test"):
                # Check if should skip
                if hasattr(test_method, "_skip_test"):
                    result = TestResult(
                        test_name=test_method.__name__,
                        status="skipped",
                        duration=0.0,
                        agent_output=None,
                        error=getattr(test_method, "_skip_reason", ""),
                    )
                    results.append(result)
                    continue
                
                # Check if parametrized
                if hasattr(test_method, "_parametrize"):
                    for params in test_method._parametrize:
                        result = test_instance.run_test(
                            lambda self, p=params: test_method(**p)
                        )
                        results.append(result)
                else:
                    result = test_instance.run_test(test_method)
                    results.append(result)
        
        return results
    
    def _print_summary(self, passed: int, failed: int, skipped: int, duration: float):
        """Print test summary"""
        self.console.print("\n[bold]Test Summary[/bold]\n")
        
        table = Table(show_header=True, header_style="bold")
        table.add_column("Status")
        table.add_column("Count", justify="right")
        
        table.add_row("[green]Passed[/green]", str(passed))
        table.add_row("[red]Failed[/red]", str(failed))
        table.add_row("[yellow]Skipped[/yellow]", str(skipped))
        table.add_row("[blue]Total[/blue]", str(passed + failed + skipped))
        table.add_row("[cyan]Duration[/cyan]", f"{duration:.2f}s")
        
        self.console.print(table)
        self.console.print()
        
        if failed == 0:
            self.console.print("[bold green]✅ All tests passed![/bold green]")
        else:
            self.console.print(f"[bold red]❌ {failed} test(s) failed[/bold red]")
    
    def run_file(self, file_path: str) -> Dict[str, Any]:
        """Run tests from a specific file"""
        self.test_classes = []
        self._load_test_file(Path(file_path))
        return self.run_all()
    
    def run_test(self, test_class_name: str, test_method_name: str = None) -> Dict[str, Any]:
        """Run a specific test or test class"""
        # Find test class
        test_class = None
        for tc in self.test_classes:
            if tc.__name__ == test_class_name:
                test_class = tc
                break
        
        if not test_class:
            self.console.print(f"[red]Test class not found: {test_class_name}[/red]")
            return {"results": [], "summary": {}}
        
        test_instance = test_class()
        
        if test_method_name:
            # Run specific method
            test_method = getattr(test_instance, test_method_name, None)
            if not test_method:
                self.console.print(f"[red]Test method not found: {test_method_name}[/red]")
                return {"results": [], "summary": {}}
            
            result = test_instance.run_test(test_method)
            return {
                "results": [result],
                "summary": {
                    "total": 1,
                    "passed": 1 if result.status == "passed" else 0,
                    "failed": 1 if result.status == "failed" else 0,
                    "skipped": 0,
                    "duration": result.duration,
                }
            }
        else:
            # Run all methods in class
            results = self._run_test_class(test_instance)
            return {
                "results": results,
                "summary": {
                    "total": len(results),
                    "passed": sum(1 for r in results if r.status == "passed"),
                    "failed": sum(1 for r in results if r.status == "failed"),
                    "skipped": sum(1 for r in results if r.status == "skipped"),
                    "duration": sum(r.duration for r in results),
                }
            }

