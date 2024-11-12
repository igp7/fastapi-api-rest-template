from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.database.base import Base


class BlacklistToken(Base):
    __tablename__ = 'blacklist_token'

    token_id = Column(Integer, primary_key=True)
    jti = Column(String(36), nullable=False)
    token_type = Column(String(10), nullable=False)
    user_identity = Column(String(50), ForeignKey('user.public_id'))
    expires = Column(DateTime, nullable=False)

    # Relaciones
    #users = relationship("User", back_populates="tokens")
