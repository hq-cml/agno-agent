agent = Agent(
    model=openAIResponses(id="gpt-5.2"),
    skills=Skills(
        loaders=[LocalSkills("/path/to/skills")]
    )
)