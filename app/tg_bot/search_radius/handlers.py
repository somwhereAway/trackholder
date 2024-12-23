from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
)

import constants
import callbacks


search_radius_conv_handler = ConversationHandler(
    entry_points=[CommandHandler(
        "search_radius", callbacks.start_search_radius)],
    states={
        constants.WAITING_INPUT: [
            MessageHandler(filters.text & ~filters.command,
                           callbacks.process_radius_input)
        ],
    },
    fallbacks=[CommandHandler("cancel", callbacks.cancel)]
)
