from fabric import task
import cloudlab_init

@task
def hello(ctx):
    print("Hello world!")

@task
def init(ctx):
    cloudlab_init.batch_init()
    
@task
def cluster(ctx):
    cloudlab_init.cluster_init()
