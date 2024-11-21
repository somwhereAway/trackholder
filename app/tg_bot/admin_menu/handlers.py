import logging

from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)
from tg_bot.admin_menu.callbacks import (
    admin_panel,
    rep_button,
    users_panel,
    exit_conversation,
    represent_user,
    make_super,
)
from tg_bot.start_handler import start
from tg_bot.admin_menu import constants as cs

admin_handler = ConversationHandler(
    entry_points=[CommandHandler("admin", admin_panel)],
    states={
        cs.USER_MENU: [
            CallbackQueryHandler(
                users_panel, pattern='^' + cs.SHOW_USER + '$'),
            CallbackQueryHandler(
                rep_button, pattern='^(page)'),
            CallbackQueryHandler(
                exit_conversation, pattern='^' + cs.EXIT + '$'),
            CallbackQueryHandler(
                represent_user, pattern='^' + cs.CURR_USER),
            CallbackQueryHandler(
                make_super,
                pattern='^(' + cs.MAKE_SUPER + '|' + cs.MAKE_COMMON + ')'
            ),
        ]
    },
    fallbacks=[
        CommandHandler("start", start)],
)
