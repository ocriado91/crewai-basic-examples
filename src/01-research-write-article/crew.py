"""A Multi-Agent system for Research and Write an article about a topic."""

from crewai import Agent, Task, Crew, LLM
from textwrap import dedent

import os


class ResearchAndWriterCrew:
    def __init__(self, verbose=False):
        """Implementation of Multi Agent System using crewAI."""

        self.verbose = verbose
        # LLM using Groq (Check the environment file)
        self.llm = LLM(
            model=os.getenv("MODEL_NAME"),
            temperature=float(os.getenv("MODEL_TEMPERATURE")),
        )

        # Create AI agents
        # 1. First agent is the Content Planner agent, in charge of research
        # about current topic.
        planner = Agent(
            llm=self.llm,  # To use LLM through Groq Platform (OpenAI API by default).
            role="Content Planner",
            goal="Plan engaging and factually accurate content on {topic}",
            backstory=dedent(
                "You're working on planning a blog article "
                "about the topic: {topic}."
                "You collect information that helps the "
                "audience learn something "
                "and make informed decisions. "
                "Your work is the basis for "
                "the Content Writer to write an article on this topic."
            ),
            allow_delegation=False,  # Not allowed to delegate work to another agent.
            verbose=self.verbose,
        )

        # 2. Second agent is Content Writer agent, in charge of write the article.
        writer = Agent(
            llm=self.llm,  # To use LLM through Groq Platform (OpenAI API by default).
            role="Content Writer",
            goal=dedent(
                "Write insightful and factually accurate "
                "opinion piece about the topic: {topic}"
            ),
            backstory=dedent(
                "You're working on a writing "
                "a new opinion piece about the topic: {topic}. "
                "You base your writing on the work of "
                "the Content Planner, who provides an outline "
                "and relevant context about the topic. "
                "You follow the main objectives and "
                "direction of the outline, "
                "as provide by the Content Planner. "
                "You also provide objective and impartial insights "
                "and back them up with information "
                "provide by the Content Planner. "
                "You acknowledge in your opinion piece "
                "when your statements are opinions "
                "as opposed to objective statements."
            ),
            allow_delegation=False,  # Not allowed to delegate work to another agent.
            verbose=self.verbose,
        )

        # 3. Editor Agent in charge of review the text written by Content Writer
        # agent.
        editor = Agent(
            llm=self.llm,  # To use LLM through Groq Platform (OpenAI API by default).
            role="Editor",
            goal=dedent(
                "Edit a given blog post to align with "
                "the writing style of the organization. "
            ),
            backstory=dedent(
                "You are an editor who receives a blog post "
                "from the Content Writer. "
                "Your goal is to review the blog post "
                "to ensure that it follows journalistic best practices,"
                "provides balanced viewpoints "
                "when providing opinions or assertions, "
                "and also avoids major controversial topics "
                "or opinions when possible."
            ),
            allow_delegation=False,  # Not allowed to delegate work to another agent.
            verbose=self.verbose,
        )

        # Creating Tasks -> Specific assignment completed by an Agent
        plan = Task(
            description=dedent(
                "1. Prioritize the latest trends, key players, "
                "and noteworthy news on {topic}.\n"
                "2. Identify the target audience, considering "
                "their interests and pain points.\n"
                "3. Develop a detailed content outline including "
                "an introduction, key points, and a call to action.\n"
                "4. Include SEO keywords and relevant data or sources."
            ),
            expected_output=dedent(
                "A comprehensive content plan document "
                "with an outline, audience analysis, "
                "SEO keywords, and resources."
            ),
            agent=planner,
        )

        write = Task(
            description=dedent(
                "1. Use the content plan to craft a compelling "
                "blog post on {topic}.\n"
                "2. Incorporate SEO keywords naturally.\n"
                "3. Sections/Subtitles are properly named "
                "in an engaging manner.\n"
                "4. Ensure the post is structured with an "
                "engaging introduction, insightful body, "
                "and a summarizing conclusion.\n"
                "5. Proofread for grammatical errors and "
                "alignment with the brand's voice.\n"
            ),
            expected_output=dedent(
                "A well-written blog post "
                "in markdown format, ready for publication, "
                "each section should have 2 or 3 paragraphs.",
            ),
            agent=writer,
        )

        edit = Task(
            description=dedent(
                "Proofread the given blog post for "
                "grammatical errors and "
                "alignment with the brand's voice."
            ),
            expected_output=dedent(
                "A well-written blog post in markdown format, "
                "ready for publication, "
                "each section should have 2 or 3 paragraphs."
            ),
            agent=editor,
        )

        # Create Crew
        self.crew = Crew(
            agents=[planner, writer, editor],
            tasks=[plan, write, edit],
            verbose=self.verbose,
        )

    def run(self, topic: str = None):
        # Running the Crew
        return self.crew.kickoff(inputs={"topic": topic})
