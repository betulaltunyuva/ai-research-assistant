import utils.conversation_memory as memory


def test_sqlite_memory(tmp_path):
    memory.DB_PATH = str(
        tmp_path / "test_memory.db"
    )

    memory.init_memory()

    memory.save_message(
        "user",
        "Test sorusu",
        session_id="pytest-session"
    )

    memory.save_message(
        "assistant",
        "Test cevabı",
        session_id="pytest-session"
    )

    messages = memory.get_recent_messages(
        session_id="pytest-session",
        limit=10
    )

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Test sorusu"
    assert messages[1]["role"] == "assistant"

    memory.save_research(
        query="Test araştırması",
        final_answer="Test sonuç",
        sources=[
            {
                "title": "Test Kaynak",
                "url": "https://example.com"
            }
        ],
        document_path="",
        session_id="pytest-session"
    )

    research = memory.get_last_research(
        session_id="pytest-session"
    )

    assert research is not None
    assert research["query"] == "Test araştırması"
    assert research["final_answer"] == "Test sonuç"
    assert len(research["sources"]) == 1