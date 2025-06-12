import unittest
from unittest.mock import patch
from adaptive_learning.integration.integration_manager import IntegrationManager


class TestIntegrationManager(unittest.TestCase):
    @patch("adaptive_learning.ui.ui_manager.UIManager.start_interaction")
    def test_run_starts_ui_interaction(self, mock_start_interaction):
        manager = IntegrationManager()
        manager.run()
        mock_start_interaction.assert_called_once()


if __name__ == "__main__":
    unittest.main()
