import os
import pytest
from bot.db import init_db, add_task, get_db

def setup_module(module):
    # Используем отдельную тестовую БД
    global TEST_DB
    TEST_DB = 'test_tasks.db'
    from bot import db
    db.DB_NAME = TEST_DB
    init_db()

def teardown_module(module):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_add_task():
    user_id = 'test_user'
    text = 'test task'
    add_task(user_id, text)
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT user_id, text FROM tasks WHERE user_id=?', (user_id,))
        row = c.fetchone()
        assert row == (user_id, text) 