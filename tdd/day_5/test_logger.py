from unittest.mock import patch
import logger

@patch('logger.log_warning', wraps=logger.log_warning)
def test_input_validator_logs_warning_for_empty_input(mock_log):
    validator = logger.InputValidator()
    result = validator.validate("")
    assert result == False
    mock_log.assert_called_with("Empty input received!")