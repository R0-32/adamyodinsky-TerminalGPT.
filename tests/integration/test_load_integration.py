import unittest
import os
import json
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from terminalgpt.main import cli
import unittest
import shutil
import json


class TestLoadCommandIntegration(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.test_conversation_path = "test_conversations"
        os.makedirs(self.test_conversation_path, exist_ok=True)

    def tearDown(self):
        # Remove the test_conversations directory after the tests are done
        shutil.rmtree(self.test_conversation_path)

    def test_load_command_integration(self):
        file_name = "test_conversation"
        messages = [{"role": "user", "content": "Test message"}]

        with open(os.path.join(self.test_conversation_path, file_name), "w") as f:
            json.dump(messages, f)

        with unittest.mock.patch(
            "terminalgpt.conversations.get_conversations", return_value=[file_name]
        ):
            result = self.runner.invoke(cli, args="load")

        self.assertIn(
            "\x1b[1m\x1b[94m\nWelcome back to TerminalGPT!\nHere are your previous conversations:\n\x1b[0m\n\x1b[1m- test_conversation\nChoose a conversation:\n \n\nChoose a conversation:\n \n\nAborted!\n",
            result.output,
        )

    def test_load_conv_nothing_to_load_integration(self):
        patch("terminalgpt.conversations.get_conversations", MagicMock(return_value=[]))

        with unittest.mock.patch(
            "terminalgpt.conversations.get_conversations", return_value=[]
        ):
            result = self.runner.invoke(cli, args="load")

            self.assertIn(
                "\x1b[1m\x1b[31m\n** There are no conversations to load! **\x1b[0m\x1b[0m\n",
                result.output,
            )


if __name__ == "__main__":
    unittest.main()
