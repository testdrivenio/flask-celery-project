from project import create_app, ext_celery


app = create_app()
celery = ext_celery.celery


@app.cli.command("celery_worker")
def celery_worker():
    from watchgod import run_process
    import subprocess

    def run_worker():
        subprocess.call(
            ['celery', '-A', 'celery_app.celery', 'worker', '--loglevel=info', '-Q', 'high_priority,default']
        )

    run_process('./project', run_worker)
