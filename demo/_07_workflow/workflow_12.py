# Human in the Loop，关键步骤要求人工介入确认

workflow = Workflow(
    db=SqliteDb(db_file='tmp/hitl.db'),
    steps=[
        Step(name='fetch_data', agent=fetch_agent),
        Step(
            name='process_data',
            agent=process_agent,
            requires_confirmation=True,
            confirmation_message='即将处理敏感数据，确认?’',
            on_reject=0nReject.skip,
        ),
    ],
)