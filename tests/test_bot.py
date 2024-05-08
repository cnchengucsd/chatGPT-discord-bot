import unittest
from unittest.mock import AsyncMock, patch
import discord
from discord.ext import commands
from src.aclient import discordClient

class TestDiscordBot(unittest.TestCase):
    def setUp(self):
        self.interaction = AsyncMock(spec=discord.Interaction)
        self.interaction.user = discord.Object(id=1234)
        self.interaction.channel = discord.Object(id=5678)
        self.interaction.channel_id = 5678

    @patch('src.aclient.discordClient.tree.sync')
    @patch('src.aclient.discordClient.send_start_prompt')
    async def test_on_ready(self, mock_send_start_prompt, mock_sync):
        with patch('src.aclient.asyncio.get_event_loop') as mock_loop:
            mock_loop.create_task = AsyncMock()
            await discordClient.on_ready()
            mock_send_start_prompt.assert_awaited_once()
            mock_sync.assert_awaited_once()
            mock_loop.create_task.assert_called_once()

    @patch('src.aclient.discordClient.enqueue_message')
    async def test_chat_command(self, mock_enqueue_message):
        self.interaction.user = discord.Object(id=123)  # Different from the bot's ID
        message = "Hello, bot!"
        await discordClient.chat(self.interaction, message=message)
        mock_enqueue_message.assert_awaited_once_with(self.interaction, message)

    @patch('src.aclient.discordClient.reset_conversation_history')
    async def test_reset_command(self, mock_reset_conversation_history):
        await discordClient.reset(self.interaction)
        mock_reset_conversation_history.assert_called_once()
        self.interaction.followup.send.assert_awaited_once_with("> **INFO: I have forgotten everything.**")

if __name__ == '__main__':
    unittest.main()
