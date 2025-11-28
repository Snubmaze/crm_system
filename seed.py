import asyncio

from sqlalchemy import select

from src.core.db import async_session_factory, init_db
from src.models.operator import Operator
from src.models.source import Source
from src.models.source_operator_weight import SourceOperatorWeight
from src.models.lead import Lead
from src.models.ticket import Ticket, TicketStatus


async def seed():
    print("Initializing DB...")
    await init_db()

    async with async_session_factory() as session:
        operators_data = [
            {"name": "Павел", "max_active_tickets": 2, "is_active": True},
            {"name": "Александр", "max_active_tickets": 3, "is_active": True},
            {"name": "Олег", "max_active_tickets": 1, "is_active": False},
        ]

        operators = []
        for op_data in operators_data:
            stmt = select(Operator).where(Operator.name == op_data["name"])
            result = await session.execute(stmt)
            op = result.scalar_one_or_none()

            if op is None:
                op = Operator(**op_data)
                session.add(op)
                await session.flush()
                print(f"Created operator: {op.name}")

            operators.append(op)


        sources_data = [
            {"name": "telegram"},
            {"name": "instagram"},
        ]

        sources = []
        for src_data in sources_data:
            stmt = select(Source).where(Source.name == src_data["name"])
            result = await session.execute(stmt)
            src = result.scalar_one_or_none()

            if src is None:
                src = Source(**src_data)
                session.add(src)
                await session.flush()
                print(f"Created source: {src.name}")

            sources.append(src)

        weights_data = {
            "telegram": [
                (operators[0].id, 70),
                (operators[1].id, 30),
            ],
            "instagram": [
                (operators[0].id, 50),
                (operators[1].id, 50),
            ],
        }

        for src in sources:
            await session.execute(
                select(SourceOperatorWeight)
                .where(SourceOperatorWeight.source_id == src.id)
                .execution_options(synchronize_session="fetch")
            )
            for operator_id, weight in weights_data[src.name]:
                sow = SourceOperatorWeight(
                    source_id=src.id,
                    operator_id=operator_id,
                    weight=weight,
                )
                session.add(sow)

            print(f"Configured operator weights for source: {src.name}")


        leads_data = [
            "melly@example.com",
            "user2@example.com",
            "user3@example.com",
        ]

        leads = []
        for email in leads_data:
            stmt = select(Lead).where(Lead.email == email)
            result = await session.execute(stmt)
            lead = result.scalar_one_or_none()

            if lead is None:
                lead = Lead(email=email)
                session.add(lead)
                await session.flush()
                print(f"Created lead: {lead.email}")

            leads.append(lead)


        tickets_data = [
            (leads[0].id, sources[0].id, operators[0].id, "Пишу из тг бота!"),
            (leads[1].id, sources[1].id, operators[1].id, "Пишу из инсты!"),
            (leads[2].id, sources[0].id, operators[1].id, "Need help, please!"),
        ]

        for lead_id, src_id, op_id, msg in tickets_data:
            stmt = select(Ticket).where(Ticket.lead_id == lead_id)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing is None:
                ticket = Ticket(
                    lead_id=lead_id,
                    source_id=src_id,
                    operator_id=op_id,
                    message=msg,
                    status=TicketStatus.ACTIVE,
                )
                session.add(ticket)
                print(f"Created ticket: lead={lead_id}, operator={op_id}")

        await session.commit()
        print("Seeding completed.")


if __name__ == "__main__":
    asyncio.run(seed())
