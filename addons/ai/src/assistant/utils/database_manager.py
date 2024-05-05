from datetime import datetime
from typing import TYPE_CHECKING, List, Dict, Tuple, Any, Optional, Sequence

from sqlalchemy import create_engine, MetaData, Table, select, Row
from sqlalchemy.orm import sessionmaker

from addons.ai.src.assistant.utils.abstract_assistant_child import AbstractAssistantChild
from addons.ai.src.assistant.utils.history_item import HistoryItem
from src.helper.user import get_user_or_sudo_user

if TYPE_CHECKING:
    from addons.ai.src.assistant.assistant import Assistant


class DatabaseManager(AbstractAssistantChild):
    def __init__(self, assistant: 'Assistant'):
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
            self.tables[table] = Table(
                table,
                self.metadata,
                autoload_with=self.engine
            )

        self.assistant.log("Database ready")

    def get_or_create_user(self) -> Row[Tuple[Any, ...]]:
        username = get_user_or_sudo_user()
        table = self.tables["user"]

        # Query for the user
        query = select(table).where(table.columns.name == username)
        result = self.session.execute(query).fetchone()

        if result is None:
            self.assistant.log(f"User {username} not found in database. Creating now.")
            ins = table.insert().values(name=username)
            self.session.execute(ins)
            self.session.commit()
            self.assistant.log(f"User {username} created.")

            return self.session.execute(query).fetchone()
        else:
            self.assistant.log(f"User {username} found in database.")
            return result

    def get_conversations_dict(self) -> {}:
        conversations = self.get_conversations()
        conversations_dict = {}

        for conversation in conversations:
            conversations_dict[conversation.id] = (
                conversation.date_created.strftime("%Y-%m-%d %H:%M:%S")
                + '|' + (conversation.title or "(No title)"))

        return conversations_dict

    def get_conversations(self) -> Row[Tuple[Any, ...]]:
        user = self.get_or_create_user()
        table = self.tables["assistant_conversation"]
        query = (select(table)
                 .where(table.columns.user_id == user.id))

        return self.session.execute(query).fetchall()

    def get_last_conversation(self) -> Row[Tuple[Any, ...]]:
        user = self.get_or_create_user()
        table = self.tables["assistant_conversation"]

        # Query for the user
        query = (select(table)
                 .where(table.columns.user_id == user.id)
                 .limit(1))

        return self.session.execute(query).fetchone()

    def get_or_create_conversation(self, conversation_id: Optional[int] = None) -> Row[Tuple[Any, ...]]:
        user = self.get_or_create_user()
        table = self.tables["assistant_conversation"]
        result: Optional[Row[Tuple[Any, ...]]] = None

        if conversation_id:
            query = select(table).where(table.columns.id == conversation_id)
            result = self.session.execute(query).fetchone()

        if result is None:
            self.assistant.log(f"No conversation found for {user.name} not found in database. Creating now.")
            ins = table.insert().values(
                user_id=user.id,
                date_created=datetime.now(),
            )
            result = self.session.execute(ins)
            self.session.commit()

            return self.get_or_create_conversation(result.inserted_primary_key[0])
        else:
            self.assistant.log(f"Using conversation: {result.title or '(No title)'}")
            return result

    def save_assistant_conversation_item(self, assistant_conversation_item: HistoryItem) -> None:
        self.session.add(assistant_conversation_item)
        self.session.commit()

    def get_conversation_items(self, conversation_id: int) -> Sequence[Row[tuple[Any, ...] | Any]]:
        query = self.session.query(HistoryItem).filter(
            HistoryItem.conversation_id == conversation_id
        ).order_by(HistoryItem.date_created)

        return query.all()
