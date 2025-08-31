"""
Tests for CLI functionality.
"""

import json
import pytest
from click.testing import CliRunner
from unittest.mock import patch

from py_healthcheck.cli import main, parse_check_spec, create_check_function


class TestCLIParsing:
    """Test CLI parsing functionality."""
    
    def test_parse_check_spec_valid(self):
        """Test parsing valid check specifications."""
        spec = "postgres:postgresql://user:pass@host/db"
        result = parse_check_spec(spec)
        
        assert result["type"] == "postgres"
        assert result["config"] == "postgresql://user:pass@host/db"
    
    def test_parse_check_spec_invalid_format(self):
        """Test parsing invalid check specification format."""
        with pytest.raises(Exception, match="Invalid check specification"):
            parse_check_spec("invalid_spec")
    
    def test_parse_check_spec_unknown_type(self):
        """Test parsing check specification with unknown type."""
        with pytest.raises(Exception, match="Unknown check type"):
            parse_check_spec("unknown:config")


class TestCLIExecution:
    """Test CLI execution."""
    
    def test_cli_no_checks(self):
        """Test CLI with no checks specified."""
        runner = CliRunner()
        result = runner.invoke(main, [])
        
        assert result.exit_code == 1
        assert "At least one --check option is required" in result.output
    
    def test_cli_single_check_success(self):
        """Test CLI with single successful check."""
        runner = CliRunner()
        
        with patch('py_healthcheck.cli.run_health_checks_sync') as mock_run:
            mock_run.return_value = {
                "status": "ok",
                "checks": {"postgres_1": "ok"},
                "summary": {"total": 1, "passed": 1, "failed": 0, "duration": 0.1}
            }
            
            result = runner.invoke(main, ["--check", "postgres:postgresql://user:pass@host/db"])
            
            assert result.exit_code == 0
            output = json.loads(result.output)
            assert output["status"] == "ok"
            assert output["checks"]["postgres_1"] == "ok"
    
    def test_cli_single_check_failure(self):
        """Test CLI with single failing check."""
        runner = CliRunner()
        
        with patch('py_healthcheck.cli.run_health_checks_sync') as mock_run:
            mock_run.return_value = {
                "status": "fail",
                "checks": {"postgres_1": "fail"},
                "details": {"postgres_1": "Connection failed"},
                "summary": {"total": 1, "passed": 0, "failed": 1, "duration": 0.1}
            }
            
            result = runner.invoke(main, ["--check", "postgres:postgresql://user:pass@host/db"])
            
            assert result.exit_code == 1
            output = json.loads(result.output)
            assert output["status"] == "fail"
            assert output["checks"]["postgres_1"] == "fail"
    
    def test_cli_multiple_checks(self):
        """Test CLI with multiple checks."""
        runner = CliRunner()
        
        with patch('py_healthcheck.cli.run_health_checks_sync') as mock_run:
            mock_run.return_value = {
                "status": "ok",
                "checks": {"postgres_1": "ok", "redis_2": "ok"},
                "summary": {"total": 2, "passed": 2, "failed": 0, "duration": 0.2}
            }
            
            result = runner.invoke(main, [
                "--check", "postgres:postgresql://user:pass@host/db",
                "--check", "redis:redis://localhost:6379"
            ])
            
            assert result.exit_code == 0
            output = json.loads(result.output)
            assert output["status"] == "ok"
            assert len(output["checks"]) == 2
    
    def test_cli_table_format(self):
        """Test CLI with table format output."""
        runner = CliRunner()
        
        with patch('py_healthcheck.cli.run_health_checks_sync') as mock_run:
            mock_run.return_value = {
                "status": "ok",
                "checks": {"postgres_1": "ok"},
                "summary": {"total": 1, "passed": 1, "failed": 0, "duration": 0.1}
            }
            
            result = runner.invoke(main, [
                "--check", "postgres:postgresql://user:pass@host/db",
                "--format", "table"
            ])
            
            assert result.exit_code == 0
            # Should contain table-like output
            assert "Health Check Results" in result.output or "postgres_1" in result.output
    
    def test_cli_quiet_mode(self):
        """Test CLI with quiet mode."""
        runner = CliRunner()
        
        with patch('py_healthcheck.cli.run_health_checks_sync') as mock_run:
            mock_run.return_value = {
                "status": "ok",
                "checks": {"postgres_1": "ok"},
                "summary": {"total": 1, "passed": 1, "failed": 0, "duration": 0.1}
            }
            
            result = runner.invoke(main, [
                "--check", "postgres:postgresql://user:pass@host/db",
                "--quiet"
            ])
            
            assert result.exit_code == 0
            assert result.output.strip() == "ok"
    
    def test_cli_verbose_mode(self):
        """Test CLI with verbose mode."""
        runner = CliRunner()
        
        with patch('py_healthcheck.cli.run_health_checks_sync') as mock_run:
            mock_run.return_value = {
                "status": "ok",
                "checks": {"postgres_1": "ok"},
                "summary": {"total": 1, "passed": 1, "failed": 0, "duration": 0.1}
            }
            
            result = runner.invoke(main, [
                "--check", "postgres:postgresql://user:pass@host/db",
                "--verbose"
            ])
            
            assert result.exit_code == 0
            output = json.loads(result.output)
            assert "summary" in output
    
    def test_cli_custom_timeout(self):
        """Test CLI with custom timeout."""
        runner = CliRunner()
        
        with patch('py_healthcheck.cli.run_health_checks_sync') as mock_run:
            mock_run.return_value = {
                "status": "ok",
                "checks": {"postgres_1": "ok"},
                "summary": {"total": 1, "passed": 1, "failed": 0, "duration": 0.1}
            }
            
            result = runner.invoke(main, [
                "--check", "postgres:postgresql://user:pass@host/db",
                "--timeout", "10"
            ])
            
            assert result.exit_code == 0
            # Verify timeout was passed to run_health_checks_sync
            mock_run.assert_called_once_with(timeout=10.0, include_details=True)
    
    def test_cli_invalid_check_spec(self):
        """Test CLI with invalid check specification."""
        runner = CliRunner()
        
        result = runner.invoke(main, ["--check", "invalid_spec"])
        
        assert result.exit_code == 1
        assert "Error parsing check" in result.output
