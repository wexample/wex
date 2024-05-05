from typing import TYPE_CHECKING, List, Dict

from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

from addons.ai.src.assistant.utils.abstract_assistant_child import AbstractAssistantChild
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

    def get_or_create_user(self):
        username = get_user_or_sudo_user()

        # Query for the user
        query = select(self.tables["user"]).where(self.tables["user"].columns.name == username)
        result = self.session.execute(query).fetchone()

        if result is None:
            self.assistant.log(f"User {username} not found in database. Creating now.")
            ins = self.tables["user"].insert().values(name=username)
            self.session.execute(ins)
            self.session.commit()
            self.assistant.log(f"User {username} created.")
        else:
            self.assistant.log(f"User {username} found in database.")

        return self.session.execute(query).fetchone()
