from ai.tools.get_ticket_status import get_ticket_status

print("name:", get_ticket_status.name)
print("ok  :", get_ticket_status.run(ticket_id="QM-101"))
print("err :", get_ticket_status.run(ticket_id="BAD-101"))
