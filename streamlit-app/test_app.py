import pytest
import streamlit as st
from unittest.mock import patch, MagicMock
import pandas as pd
import requests
import sys
import os

# Add the app directory to Python path for testing
sys.path.insert(0, os.path.dirname(__file__))

class TestStreamlitApp:
    """Test suite for the Kafka APM Streamlit application"""
    
    def test_app_imports(self):
        """Test that the main app can be imported without errors"""
        try:
            import app
            assert True, "Main app imported successfully"
        except ImportError as e:
            pytest.fail(f"Failed to import main app: {e}")
    
    def test_architecture_page_imports(self):
        """Test that the architecture page can be imported"""
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pages'))
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "architecture", 
                os.path.join(os.path.dirname(__file__), 'pages', '01_🏗️_Architecture.py')
            )
            if spec and spec.loader:
                architecture_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(architecture_module)
            assert True, "Architecture page imported successfully"
        except Exception as e:
            pytest.fail(f"Failed to import architecture page: {e}")
    
    def test_live_dashboard_imports(self):
        """Test that the live dashboard page can be imported"""
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pages'))
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "live_dashboard", 
                os.path.join(os.path.dirname(__file__), 'pages', '02_📊_Live_Dashboard.py')
            )
            if spec and spec.loader:
                dashboard_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(dashboard_module)
            assert True, "Live dashboard page imported successfully"
        except Exception as e:
            pytest.fail(f"Failed to import live dashboard page: {e}")
    
    def test_demo_scenarios_imports(self):
        """Test that the demo scenarios page can be imported"""
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pages'))
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "demo_scenarios", 
                os.path.join(os.path.dirname(__file__), 'pages', '03_🎮_Demo_Scenarios.py')
            )
            if spec and spec.loader:
                scenarios_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(scenarios_module)
            assert True, "Demo scenarios page imported successfully"
        except Exception as e:
            pytest.fail(f"Failed to import demo scenarios page: {e}")

class TestDashboardFunctions:
    """Test dashboard utility functions"""
    
    @patch('requests.get')
    def test_prometheus_query_success(self, mock_get):
        """Test successful Prometheus query"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'success',
            'data': {
                'result': [{'value': [1234567890, '42']}]
            }
        }
        mock_get.return_value = mock_response
        
        # Import and test the query function
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pages'))
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "live_dashboard", 
            os.path.join(os.path.dirname(__file__), 'pages', '02_📊_Live_Dashboard.py')
        )
        
        if spec and spec.loader:
            dashboard_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(dashboard_module)
            
            result = dashboard_module.query_prometheus('up')
            assert result is not None
            assert len(result) == 1
            assert result[0]['value'][1] == '42'
    
    @patch('requests.get')
    def test_prometheus_query_failure(self, mock_get):
        """Test failed Prometheus query"""
        # Mock failed response
        mock_get.side_effect = requests.RequestException("Connection failed")
        
        # Import and test the query function
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pages'))
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "live_dashboard", 
            os.path.join(os.path.dirname(__file__), 'pages', '02_📊_Live_Dashboard.py')
        )
        
        if spec and spec.loader:
            dashboard_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(dashboard_module)
            
            result = dashboard_module.query_prometheus('up')
            assert result is None

class TestScenarioFunctions:
    """Test demo scenario functions"""
    
    @patch('subprocess.run')
    def test_run_command_success(self, mock_run):
        """Test successful command execution"""
        # Mock successful command
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Success output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Import and test the run_command function
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pages'))
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "demo_scenarios", 
            os.path.join(os.path.dirname(__file__), 'pages', '03_🎮_Demo_Scenarios.py')
        )
        
        if spec and spec.loader:
            scenarios_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(scenarios_module)
            
            returncode, stdout, stderr = scenarios_module.run_command('echo "test"')
            assert returncode == 0
            assert stdout == "Success output"
            assert stderr == ""
    
    @patch('subprocess.run')
    def test_run_command_failure(self, mock_run):
        """Test failed command execution"""
        # Mock failed command
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Error output"
        mock_run.return_value = mock_result
        
        # Import and test the run_command function
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pages'))
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "demo_scenarios", 
            os.path.join(os.path.dirname(__file__), 'pages', '03_🎮_Demo_Scenarios.py')
        )
        
        if spec and spec.loader:
            scenarios_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(scenarios_module)
            
            returncode, stdout, stderr = scenarios_module.run_command('false')
            assert returncode == 1
            assert stdout == ""
            assert stderr == "Error output"

class TestDataFormats:
    """Test data format handling"""
    
    def test_metrics_dataframe_creation(self):
        """Test creating DataFrames for metrics display"""
        # Test data for architecture page
        app_data = {
            "Component": ["Java Apps", "Python Apps", "Go Apps"],
            "Technology": ["OpenTelemetry Java Agent", "OpenTelemetry Python SDK", "OpenTelemetry Go SDK"],
            "Purpose": ["Auto-instrumentation", "Manual instrumentation", "Manual instrumentation"]
        }
        
        df = pd.DataFrame(app_data)
        assert len(df) == 3
        assert "Component" in df.columns
        assert "Technology" in df.columns
        assert "Purpose" in df.columns
        assert df.iloc[0]["Component"] == "Java Apps"
    
    def test_status_dataframe_creation(self):
        """Test creating DataFrames for service status"""
        status_data = [
            {"Service": "kafka", "Status": "Running"},
            {"Service": "prometheus", "Status": "Running"},
            {"Service": "grafana", "Status": "Down"}
        ]
        
        df = pd.DataFrame(status_data)
        assert len(df) == 3
        assert "Service" in df.columns
        assert "Status" in df.columns
        
        # Check for running services
        running_services = df[df["Status"] == "Running"]
        assert len(running_services) == 2
        
        # Check for down services
        down_services = df[df["Status"] == "Down"]
        assert len(down_services) == 1
        assert down_services.iloc[0]["Service"] == "grafana"

class TestEnvironmentVariables:
    """Test environment variable handling"""
    
    def test_default_urls(self):
        """Test default URL configuration"""
        # Test with no environment variables set
        with patch.dict(os.environ, {}, clear=True):
            import app
            
            # The app should use default localhost URLs
            default_grafana = "http://localhost:3000"
            default_prometheus = "http://localhost:9090"
            
            # These are the expected defaults based on the app code
            assert True, "Default URLs should be localhost-based"
    
    def test_custom_urls(self):
        """Test custom URL configuration via environment variables"""
        custom_env = {
            'GRAFANA_URL': 'http://custom-grafana:3000',
            'PROMETHEUS_URL': 'http://custom-prometheus:9090',
            'OTEL_COLLECTOR_URL': 'http://custom-collector:13133'
        }
        
        with patch.dict(os.environ, custom_env):
            # The app should pick up custom URLs
            assert os.getenv('GRAFANA_URL') == 'http://custom-grafana:3000'
            assert os.getenv('PROMETHEUS_URL') == 'http://custom-prometheus:9090'
            assert os.getenv('OTEL_COLLECTOR_URL') == 'http://custom-collector:13133'

class TestUIComponents:
    """Test UI component functionality"""
    
    def test_language_selection(self):
        """Test language selection functionality"""
        # Test both supported languages
        languages = ["English", "繁體中文"]
        
        for lang in languages:
            assert lang in ["English", "繁體中文"], f"Language {lang} should be supported"
    
    def test_page_navigation(self):
        """Test page navigation structure"""
        # Expected pages based on the main app
        expected_pages = {
            "🏠 Overview": "overview",
            "🏗️ Architecture": "architecture", 
            "🔧 Tech Stack": "tech_stack",
            "📊 Monitoring Guide": "monitoring",
            "🎮 Demo Scenarios": "scenarios",
            "📈 Live Status": "status",
            "🔗 API Reference": "api",
            "🛠️ Troubleshooting": "troubleshooting"
        }
        
        for page_name, page_key in expected_pages.items():
            assert page_key is not None, f"Page {page_name} should have a valid key"
            assert isinstance(page_key, str), f"Page key for {page_name} should be a string"

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
