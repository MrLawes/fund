from fund.fund_celery import app


@app.task(bind=True)
def refresh_fund(self, ):
    from fund.management.commands.fund_value import Command
    Command().handle()
