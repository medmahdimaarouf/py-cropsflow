from cropsflow.common.decorators import task


@task(template_path='./test.task.xml')
class TestTask:
    pass
