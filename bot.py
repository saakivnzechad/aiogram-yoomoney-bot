"""
 * Copyright (c) 2025 Danil Klimov.
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import asyncio
import logging
import os
import random
import string
import sqlite3
import config
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from yoomoney import Quickpay, Client
from aiogram.enums import ParseMode

# Load environment variables and configuration
API_TOKEN = config.API_TOKEN
TELEGRAM_CHANNEL_LINK = config.TELEGRAM_CHANNEL_LINK
FREE_GUIDE_LINK = config.FREE_GUIDE_LINK
CONTACT_LINK = config.CONTACT_LINK
PAYMENT_TOKEN = config.PAYMENT_TOKEN
PAYMENT_SUM = config.PAYMENT_SUM
PAYMENT_RECEIVER = config.PAYMENT_RECEIVER
PAYMENT_TARGETS = config.PAYMENT_TARGETS

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and YooMoney client
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
client = Client(PAYMENT_TOKEN)

# Function to create database and users table
def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, payment_id TEXT, payment_status BOOLEAN)''')
    conn.commit()
    conn.close()

# Function to generate a unique payment_id
def generate_payment_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Function to save user data to DB
def save_user_data(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("SELECT payment_id FROM users WHERE user_id = ?", (user_id,))
    existing_record = c.fetchone()

    if existing_record is None:
        payment_id = generate_payment_id()
        c.execute("INSERT INTO users (user_id, payment_id, payment_status) VALUES (?, ?, ?)",
                  (user_id, payment_id, False))
    conn.commit()
    conn.close()

# Function to check user's payment status
def check_payment_status(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT payment_status FROM users WHERE user_id = ?", (user_id,))
    payment_status = c.fetchone()
    conn.close()
    return payment_status[0] if payment_status else False

# Function to get user's payment_id
def get_payment_id(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT payment_id FROM users WHERE user_id = ?", (user_id,))
    payment_id = c.fetchone()
    conn.close()
    return payment_id[0] if payment_id else None

# State classes for the finite state machine
class PurchaseProcess(StatesGroup):
    waiting_for_payment = State()

# Handler for the /start command
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    save_user_data(message.from_user.id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Join Channel", url=TELEGRAM_CHANNEL_LINK)],
        [InlineKeyboardButton(text="📄 Download Free Content", callback_data="download_free_content"),
         InlineKeyboardButton(text="🌐 Open Content Online", url=FREE_GUIDE_LINK)],
        [InlineKeyboardButton(text="💬 Contact for Consultation", url=CONTACT_LINK)],
        [InlineKeyboardButton(text="📚 Buy Digital Product", callback_data="buy_product")]
    ])

    photo = FSInputFile('start_image.png')
    await message.answer_photo(
        photo=photo,
        caption="👋 Welcome!\n\nChoose one of the available options:",
        reply_markup=keyboard
    )

# Handler for "Download Free Content" button
@dp.callback_query(lambda call: call.data == "download_free_content")
async def send_free_content(callback: types.CallbackQuery):
    file_path = "free_content.docx"

    if not os.path.exists(file_path):
        await callback.message.answer("❌ Error: file not found.")
        logger.error(f"File not found at path: {file_path}")
        return

    try:
        document = FSInputFile(file_path)
        await callback.message.answer_document(document, caption="📄 Your free content:")
        logger.info(f"Content sent to user: {callback.from_user.id}")
    except PermissionError:
        await callback.message.answer("❌ File access error.")
        logger.error(f"File access error: {file_path}")
    except Exception as e:
        logger.error(f"Error sending document: {e}")
        await callback.message.answer("❌ An error occurred while sending the file.")

# Handler for digital product purchase
@dp.callback_query(lambda call: call.data == "buy_product")
async def buy_product(callback: types.CallbackQuery, state: FSMContext):
    try:
        user_id = callback.from_user.id
        payment_status = check_payment_status(user_id)

        if payment_status:
            await callback.message.answer("✅ Payment already made. Thank you!")
            await send_paid_content(callback.message)
        else:
            payment_id = get_payment_id(user_id)
            quickpay = Quickpay(
                receiver=PAYMENT_RECEIVER,
                quickpay_form="shop",
                targets=PAYMENT_TARGETS,
                paymentType="SB",
                sum=PAYMENT_SUM,
                label=payment_id
            )
            payment_url = quickpay.base_url

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Pay", url=payment_url)],
                [InlineKeyboardButton(text="Complete Payment", callback_data="confirm_payment")]
            ])
            await callback.message.answer(
                f"📚 To get the product, please pay <b>{PAYMENT_SUM}</b> rubles. \nAfter payment, click the <b>Complete Payment</b> button.",
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML
            )

            await state.set_state(PurchaseProcess.waiting_for_payment)
            await callback.answer()

    except Exception as e:
        logger.error(f"Error processing product purchase request: {e}")
        await callback.message.answer("❌ An error occurred while processing your request.")

# Handler for payment confirmation
@dp.callback_query(lambda call: call.data == "confirm_payment")
async def confirm_payment(callback: types.CallbackQuery, state: FSMContext):
    try:
        user_id = callback.from_user.id
        payment_id = get_payment_id(user_id)

        history = client.operation_history(label=payment_id)
        payment_confirmed = any(operation.status == "success" for operation in history.operations)

        if payment_confirmed:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("UPDATE users SET payment_status = ? WHERE user_id = ?", (True, user_id))
            conn.commit()
            conn.close()

            await callback.message.answer("✅ Payment successfully confirmed. Thank you!")
            await send_paid_content(callback.message)
            logger.info(f"Payment confirmed for user {user_id} with payment_id {payment_id}")
        else:
            await callback.message.answer("❌ Payment not found or not yet completed.")
            logger.warning(f"Payment not confirmed for user {user_id} with payment_id {payment_id}")

        await state.clear()
        await callback.answer()

    except Exception as e:
        logger.error(f"Error confirming payment: {e}")
        await callback.message.answer("❌ An error occurred while checking the payment. Please try again.")

# Function to send paid content
async def send_paid_content(message: types.Message):
    pdf_file_path = "paid_content.pdf"

    if not os.path.exists(pdf_file_path):
        await message.answer("❌ File not found.")
        logger.error(f"File not found at path: {pdf_file_path}")
        return

    try:
        loading_message = await message.answer("🔄 Please wait, file is loading...")
        document = FSInputFile(pdf_file_path)
        await message.answer_document(document, caption="📄 Your file:")
        await loading_message.delete()
        logger.info(f"Paid content sent to user: {message.from_user.id}")

    except PermissionError:
        await message.answer("❌ File access error.")
        logger.error(f"File access error: {pdf_file_path}")
    except Exception as e:
        logger.error(f"Error sending document: {e}")
        await message.answer("❌ An error occurred while sending the file.")

# Bot startup
async def main():
    try:
        create_db()
        logger.info("Bot started...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error starting the bot: {e}")

if __name__ == '__main__':
    asyncio.run(main())