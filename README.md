<p align="center">
  <a href="http://proxtractor.com/" target="blank"><img src="https://res.cloudinary.com/medmahdimaarouf/image/upload/v1690126172/Proxtractor/prx-logo-dark.svg" width="120" alt="Proxtractor Logo" /></a>
</p>

  <p align="center">A progressive <a href="https://python.org" target="blank">Python</a> RPA framework for building efficient and scalable web services automation applications.</p>

## Description

CropsFlow cloud for running automated web services

The CLI provides built in support from the schematics collection
at [@cropsflow/schematics](https://github.com/cropsflow/schematics).

Read more [here](https://docs.cropsflow.com/cli/overview).

## Installation

```
$ pip install cropsflow

```

## Action example should be

```
@action(selector='my-pipe')
@option(key='my-option',meta_type:str})
class MyAction(Action):

    # Dependency injection
    @inject(arg_name='driver',token=Driver)
    def __init__(self,driver:Driver):
        self.driver = driver

    def start(self,context:ActionContext,options:Dic[str,any] = {}):
        pass
```

## Pipe example should be

```
@pipe(selector='my-pipe')
class MyPipe(Pipe):

    accumulate(self,value:DataModel,accessor:str =  None):
        # accumulate your nodeValue data fields/items.
        this.value = value;
```

## Service example should be

```
@service(scope=InjectionScope.DEFAULT)
class Driver:
    
    def __init__(self):
        pass

```

## Task example should be

```
@task(template='robot.xml')
'''
 ** Task lifecylces **
OnInit          : Task initialized lifecycle
OnSuccess       : Task finished with success
OnDataRecived   : Data recived and beeing to pass to pipe .
OnError         : Task finish with error
'''
class MyTask(Init):
    
    def __init__(self):
        pass
```

## Task template should be

```
<?xml version="1.0" encoding="UTF-8"?>
<task dataset="brand-items">
    <meta>
        <title>Example task</title>
        <version>1.0</version>
        <description>
            Example task for running multi actions 
        </description>
        <tags>
            task,automation,robots
        </tags>
        <readme src="./readme.md"/>
    </meta>
    <playbook>
        <sleep seconds="2">
            <sleep seconds="1"/>
            <sleep seconds="2"/>
            <sleep seconds="3"/>
        </sleep>
    </playbook>
</task>
```

# CropsFlow modules design

```
@module(
    declarations=[],
    imports=[CommonModule],
    exports=[],
    providers=[]
)
# this a Initialized Module example
class MyModule(Init):

    def __init__(self):
        pass
        
    # This method will be called in application initallization         
    def init(self):
        pass
```
