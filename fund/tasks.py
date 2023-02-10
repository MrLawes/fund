from fund.fund_celery import app


@app.task(bind=True)
def test(self, ):
    print(1111111)
