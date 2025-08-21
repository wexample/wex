from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from sqlalchemy import MetaData, Table, create_engine, select
from sqlalchemy.engine import CursorResult, Row
from sqlalchemy.orm import sessionmaker

from addons.ai.src.assistant.utils.abstract_assistant_child import \
    AbstractAssistantChild
from addons.ai.src.assistant.utils.history_item import HistoryItem
from src.helper.user import get_user_or_sudo_user

if TYPE_CHECKING:
    from addons.ai.src.assistant.assistant import Assistant


class DatabaseManager(AbstractAssistantChild):
    def __init__(self, assistant: "Assistant") -> None:
        super().__init__(assistant)

        manager = assistant.assistant_app_manager
        self.config = manager.get_config("service.postgres").get_dict()

        self.engine = create_engine(
            f"postgresql://{self.config['user']}"
            f":{self.config['password']}@localhost"
            f":5{manager.get_config('port.public', 444).get_int()}/{self.config['name']}"
        )

        self.assistant.log("Database connected")

        self.session = sessionmaker(bind=self.engine)()
        self.metadata = MetaData()

        tables: List[str] = [
            "user",
            "assistant_conversation",
            "assistant_conversation_item",
        ]

        self.tables: Dict[str, Table] = {}
        for table in tables:
            self.tables[table] = Table(table, self.metadata, autoload_with=self.engine)

        self.kernel.io.success("Database ready")

    def get_or_create_user(self) -> Row[Tuple[Any, ...]]:
        username = get_user_or_sudo_user()
        table = self.tables["user"]

        # Query for the user
        query = select(table).where(table.columns.name == username)
        result: Optional[Row[Tuple[Any, ...]]] = self.session.execute(query).fetchone()

        if result is None:
            self.assistant.log(f"User {username} not found in database. Creating now.")
            ins = table.insert().values(name=username)
            self.session.execute(ins)
            self.session.commit()
            self.assistant.log(f"User {username} created.")

            result = self.session.execute(query).fetchone()
            assert result is not None
            return result
        else:
            self.assistant.log(f"User {username} found in database.")
            return result

    def get_conversations_dict(self) -> Dict[int, str]:
        conversations = self.get_conversations()
        conversations_dict: Dict[int, str] = {}

        for conversation in conversations:
            conversations_dict[conversation.id] = (
                conversation.date_created.strftime("%Y-%m-%d %H:%M:%S")
                + "|"
                + (conversation.title or "(No title)")
            )

        return conversations_dict

    def get_conversations(self) -> List[Row[Tuple[Any, ...]]]:
        user = self.get_or_create_user()
        table = self.tables["assistant_conversation"]
        query = select(table).where(table.columns.user_id == user.id)

        rows = self.session.execute(query).fetchall()
        return list(rows)

    def get_last_conversation(self) -> Optional[Row[Tuple[Any, ...]]]:
        user = self.get_or_create_user()
        table = self.tables["assistant_conversation"]

        # Query for the user
        query = select(table).where(table.columns.user_id == user.id).limit(1)

        return self.session.execute(query).fetchone()

    def get_or_create_conversation(
        self, conversation_id: Optional[int] = None
    ) -> Row[Tuple[Any, ...]]:
        user = self.get_or_create_user()
        table = self.tables["assistant_conversation"]
        result: Optional[Row[Tuple[Any, ...]]] = None

        if conversation_id:
            query = select(table).where(table.columns.id == conversation_id)
            result = self.session.execute(query).fetchone()

        if result is None:
            self.assistant.log(
                f"No conversation found for {user.name} not found in database. Creating now."
            )
            ins = table.insert().values(
                user_id=user.id,
                date_created=datetime.now(),
            )
            insert_result: CursorResult[Any] = self.session.execute(ins)
            self.session.commit()

            return self.get_or_create_conversation(
                insert_result.inserted_primary_key[0]
            )
        else:
            self.assistant.log(f"Using conversation: {result.title or '(No title)'}")
            return result

    def save_assistant_conversation_item(
        self, assistant_conversation_item: HistoryItem
    ) -> None:
        self.session.add(assistant_conversation_item)
        self.session.commit()

    def get_conversation_items(self, conversation_id: int) -> List[HistoryItem]:
        query = (
            self.session.query(HistoryItem)
            .filter(HistoryItem.conversation_id == conversation_id)
            .order_by(HistoryItem.date_created)
        )

        return query.all()
