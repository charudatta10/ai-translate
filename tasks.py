from invoke import task

@task(dfault=True)
def run(ctx):
    ctx.run("python -m src.main")