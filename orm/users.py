# Stdlib Imports
from typing import List

# SQLAlchemy Imports
from sqlalchemy.orm import joinedload

# Own Imports
from models.user import User
from schemas.user import UserCreate
from orm.base import ORMSessionMixin
from config.database import SessionLocal


class BaseUsersORM(ORMSessionMixin):
    def partial_list(self):
        """This method partially retrieves a list of users."""

        return self.orm.query(User)


class UsersORM(BaseUsersORM):
    """CRUD Operations for the users to interact with the database."""

    async def get(self, user_id: int) -> User:
        """This method gets a user from the database."""

        user = (
            self.partial_list()
            .options(joinedload(User.wallets))
            .filter(User.id == user_id)
            .first()
        )
        return user

    async def get_email(self, user_email: str) -> User:
        """This method gets a user based on their email from the database."""

        user = (
            self.partial_list()
            .options(joinedload(User.wallets))
            .filter(User.email == user_email)
            .first()
        )
        return user

    async def list(self, skip: int, limit: int) -> List[User]:
        """This method gets all the users from the database."""

        return (
            self.partial_list()
            .options(joinedload(User.wallets))
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def create(self, user: UserCreate) -> User:
        """This method creates a new user."""

        user = User(**user.dict())

        self.orm.add(user)
        self.orm.commit()
        self.orm.refresh(user)

        return user


users_orm = UsersORM(SessionLocal())
