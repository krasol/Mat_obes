from crewai import Agent, Crew, Task

from ai.llm_factory import get_llm
from ai.tools.get_ticket_status import get_ticket_status


agent = Agent(
    role="Оператор электронной очереди QueueManager",
    goal="Помогать пользователю получать достоверную информацию о талонах электронной очереди.",
    backstory=(
        "Ты оператор системы QueueManager. "
        "Когда пользователь спрашивает состояние конкретного талона, "
        "ты всегда проверяешь его через инструмент get_ticket_status "
        "и не придумываешь состояние или место в очереди самостоятельно."
    ),
    tools=[get_ticket_status],
    llm=get_llm(),
    verbose=True,
    max_iter=5,
)


task = Task(
    description=(
        "Узнай текущее состояние талона QM-101 и его место в электронной очереди. "
        "Обязательно используй get_ticket_status и основывай ответ только на данных инструмента."
    ),
    expected_output=(
        "Краткий ответ на русском языке: номер талона, его текущее состояние "
        "и место в очереди."
    ),
    agent=agent,
)


crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
)


if __name__ == "__main__":
    print(crew.kickoff())
