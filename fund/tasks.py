from fund.fund_celery import app


@app.task(bind=True)
def test(self, ):
    with open('a', 'a+') as f:
        f.write('fffffff\n')
