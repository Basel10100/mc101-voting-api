# Making db models
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, func, Boolean, LargeBinary, Table
from db.DbConfig import Base, get_engine
from utils.constants import TableNames, ColumnNames


class UserDBModel(Base):
    __tablename__ = TableNames.USERS  # Name of the table in the database

    id = Column(ColumnNames.ID, Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(ColumnNames.EMAIL, String, unique=True, index=True, nullable=False)
    hashed_password = Column(ColumnNames.HASHED_PASSWORD, String, nullable=False)
    name = Column(ColumnNames.Name, String, nullable=True)  # Full name can be optional
    is_active = Column(ColumnNames.IS_ACTIVE, Boolean, default=True)  # 1 for active, 0 for inactive
    created_at = Column(ColumnNames.CREATED_AT, 
                        TIMESTAMP(True), 
                        default=func.now(), 
                        nullable=False)

class CandidateDBModel(Base):
    __tablename__ = TableNames.CANDIDATES

    id = Column(ColumnNames.ID, Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(ColumnNames.Name, String, nullable=False, unique=True)
    party = Column(ColumnNames.PARTY, String, nullable=True)  # Party can be optional
    created_at = Column(ColumnNames.CREATED_AT, 
                        TIMESTAMP(True), 
                        default=func.now(), 
                        nullable=False)    


class VoteDBModel(Base):
    # This is a table to hold the votes cast by users for candidates
    __tablename__ = TableNames.VOTES

    # Pay attention to the ondelete behavior of foreign keys
    # We have two parameters in ForeignKey: the table.column and ondelete behavior
    # The table.column is neccessary to establish the foreign key relationship
    # The ondelete behavior defines what happens to the foreign key when the referenced record is deleted
    # By default, it is RESTRICT, which means the deletion will be blocked if there are dependent records
    id = Column(ColumnNames.ID, Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ColumnNames.USER_ID, Integer,  
                     ForeignKey(f"{TableNames.USERS}.{ColumnNames.ID}", ondelete="SET NULL"),
                     nullable=False,
                     )  # Foreign key to UserDBModel.id
    ## Users are not important for us in the voting system, so we let them to be deleted from USERS table,
    # but we set the user_id to NULL in VOTES table to keep the vote record.
    ## Other ondelete options: CASCADE, RESTRICT, NO ACTION (similar to restrict), SET DEFAULT
    candidate_id = Column(
        ColumnNames.CANDIDATE_ID, Integer,
        ForeignKey(f"{TableNames.CANDIDATES}.{ColumnNames.ID}", ondelete="RESTRICT"),
        nullable=False, 
        )  # Foreign key to CandidateDBModel.id
    ## Candidates are important for us, if a candidate is deleted from CANDIDATES table, 
    # we should not delete the votes, thus, it will not allow the deletion of votes
    created_at = Column(ColumnNames.CREATED_AT,
                        TIMESTAMP(True),
                        default=func.now(),
                        nullable=False)


class NoteDBModel(Base):
    __tablename__ = TableNames.NOTES

    id = Column(ColumnNames.ID, Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ColumnNames.USER_ID, Integer, ForeignKey(f"{TableNames.USERS}.{ColumnNames.ID}", ondelete="CASCADE"), nullable=False)
    title = Column(ColumnNames.TITLE, String, nullable=False)
    content_encrypted = Column(ColumnNames.CONTENT_ENCRYPTED, LargeBinary, nullable=False)
    personal_encryption = Column(ColumnNames.PERSONAL_ENCRYPTION, Boolean, default=False)
    kdf_salt = Column(ColumnNames.KDF_SALT, LargeBinary, nullable=False)
    nonce = Column(ColumnNames.NONCE, LargeBinary, nullable=False)
    created_at = Column(ColumnNames.CREATED_AT, TIMESTAMP(True), default=func.now(), nullable=False)
    updated_at = Column(ColumnNames.UPDATED_AT, TIMESTAMP(True), default=func.now(), onupdate=func.now(), nullable=False)


TokenBlacklistTable = Table(
    "token_blacklist",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("jti", String, unique=True, nullable=False, index=True),
    Column("expires_at", TIMESTAMP(True), nullable=False),
    extend_existing=True,
)


class TokenBlacklist(Base):
    __table__ = TokenBlacklistTable


Base.metadata.create_all(bind=get_engine())