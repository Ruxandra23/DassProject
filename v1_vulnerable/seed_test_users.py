
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, _init_db
from models import User, UserRole, Ticket, TicketSeverity, TicketStatus, db

with app.app_context():
    _init_db()
    if User.query.filter_by(email="victim@test.com").first():
        print("Utilizatorii de test există deja în v1.")
    else:
        for email, password in [
            ("victim@test.com", "123"),
            ("admin@test.com", "parola"),
            ("user@test.com", "1"),
        ]:
            u = User(email=email, role=UserRole.USER)
            u.set_password(password)
            db.session.add(u)
        db.session.commit()
        print("v1: Am creat 3 utilizatori de test.")
        print("  victim@test.com / 123")
        print("  admin@test.com  / parola")
        print("  user@test.com   / 1")

    # adauga tickete de test daca nu exista
    victim = User.query.filter_by(email="victim@test.com").first()
    admin = User.query.filter_by(email="admin@test.com").first()

    if victim and admin and not Ticket.query.filter_by(owner_id=victim.id).first():
        tickete = [
            Ticket(title="Retea lenta birou 3", description="Viteza internet scazuta dupa ora 14:00.", severity=TicketSeverity.MED, status=TicketStatus.OPEN, owner_id=victim.id),
            Ticket(title="Acces refuzat folder shared", description="Nu pot deschide folderul Z:\\Shared\\Proiecte.", severity=TicketSeverity.HIGH, status=TicketStatus.OPEN, owner_id=victim.id),
            Ticket(title="Raport confidential proiect X", description="Date sensibile despre bugetul intern 2025.", severity=TicketSeverity.HIGH, status=TicketStatus.OPEN, owner_id=admin.id),
        ]
        for t in tickete:
            db.session.add(t)
        db.session.commit()
        print("v1: Am creat 3 tickete de test (2 ale victim, 1 al admin).")
