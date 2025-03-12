from datetime import datetime

from .base import Base, db


class InvitationCode(Base):
    __table_args__ = {'schema': 'public'}

    __tablename__ = 'invitation_codes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_disabled = db.Column(db.Boolean, default=False)
    usage_count = db.Column(db.Integer, default=0)
    last_used_at = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('public.users.id'), nullable=False)

    def is_valid(self):
        return not self.is_disabled and datetime.now() < self.expires_at

    def record_usage(self):
        self.usage_count += 1
        self.last_used_at = datetime.now()
        db.session.commit()
        return self

    def disable(self):
        self.is_disabled = True
        db.session.commit()
        return self

    def enable(self):
        self.is_disabled = False
        db.session.commit()
        return self

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    def __repr__(self):
        return f'<ID: {self.id}, Code: {self.code}, Expires: {self.expires_at}, Disabled: {self.is_disabled}>'
