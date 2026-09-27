# Контракт Tool (воркшоп 1)
# Имя: get_ticket_status
# Назначение: получить текущее состояние талона электронной очереди и место клиента в очереди.
# Вход: ticket_id: str — обязателен, формат QM-<число>, например QM-101.
# Выход при успехе: JSON-строка с полями status, ticket_id, state, position.
# Выход при ошибке: JSON-строка с полями status="error" и message.
# Допустимые состояния талона: waiting, called, served, cancelled.
# Краевые случаи:
# - пустой ticket_id — ошибка;
# - неправильный формат ticket_id — ошибка;
# - талон не найден — ошибка;
# - отменённый или обслуженный талон — корректное состояние, а не ошибка.

import json
import re

from crewai.tools import tool


TICKETS = {
    "QM-101": {"state": "waiting", "position": 3},
    "QM-102": {"state": "called", "position": 1},
    "QM-103": {"state": "served", "position": None},
    "QM-104": {"state": "cancelled", "position": None},
}


def _fail(message: str) -> str:
    """Возвращает ошибку в едином JSON-формате."""
    return json.dumps(
        {"status": "error", "message": message},
        ensure_ascii=False,
    )


@tool("get_ticket_status")
def get_ticket_status(ticket_id: str) -> str:
    """Возвращает состояние конкретного талона электронной очереди и его место в очереди.

Используй этот инструмент всегда, когда пользователь спрашивает о состоянии,
статусе или месте в очереди конкретного талона вида QM-<число>.
Не придумывай статус талона самостоятельно — получай его только через этот инструмент."""
    if not ticket_id or not ticket_id.strip():
        return _fail("ticket_id не должен быть пустым")

    ticket_id = ticket_id.strip()

    if not re.fullmatch(r"QM-\d+", ticket_id):
        return _fail(
            f"ticket_id должен иметь формат QM-<число>, получено '{ticket_id}'"
        )

    try:
        ticket = TICKETS.get(ticket_id)

        if ticket is None:
            return _fail(f"талон '{ticket_id}' не найден")

        return json.dumps(
            {
                "status": "ok",
                "ticket_id": ticket_id,
                "state": ticket["state"],
                "position": ticket["position"],
            },
            ensure_ascii=False,
        )
    except Exception as exc:
        return _fail(f"не удалось получить состояние талона: {exc}")
