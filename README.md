
<p align="center">
  <a href="http://proxtractor.com/" target="blank"><img src="https://res.cloudinary.com/medmahdimaarouf/image/upload/v1690126172/Proxtractor/prx-logo-dark.svg" width="120" alt="Proxtractor Logo" /></a>
</p>

  <p align="center">A progressive <a href="https://python.org" target="blank">Python</a> RPA framework for building efficient and scalable web services automation applications.</p>

## Description

Proxtractor cloud for running automated web services

The CLI works with [schematics](https://github.com/angular/angular-cli/tree/master/packages/angular_devkit/schematics), and provides built in support from the schematics collection at [@proxtractor/proxtractor-schematics](https://github.com/proxtractor/proxtractor-schematics).

Read more [here](https://docs.proxtractor.com/cli/overview).

## Installation

```
$ npm install -g @proxtractor/cli

```

## Pipe example should be

```
@PrxPipe({
    // required for task xml selector 
    selector:"my-pipe",
})
export class MyPipe extends BaseDataPipe<IDataSchemaNode>{

    accumulate(value:IDataSchemaNode):void{

    }

    @Accumulator({name:"email",required:boolean})
    accumulateEmail(value:TextSchemaNode):void{
        //accumulate your nodeValue data fields/items.
        this.value = value;
    }
}
```

## Action example should be

```
@PrxAction({
    // required for task xml template 
    selector:"my-action",
})
export class MyAction /* implement Action lifecycle like OnInit , OnDestroy , OnSuccess , OnDataRecived .... */{
    @Option({name:string,required:boolean})

    constructor(){private driver:MyDriver /* other dependecies*/}

    start(context:ActionContext):ActionObservable<ActionContext>{
        return new ActionObservable((async subscriber=>{
            // this.driver.agent. ...
            await subscriber.next(context);
            subscriber.complete()
        }))
    }
}
```
NB : - Action can have pipe class as a injected dependency
- Action should have driver agent type generic type.

```
@PrxInjectable({
    // Injectable params coming soon
})
export class ChromiumAgent{
    // configuration values injected from PrxConfigService for environment variables
    @Config({name:string,required:boolean})

    constructor(){}

}
```


## Task example should be
```
@PrxTask({
    template:"robot.xml"
})
/*
 ** Task lifecylces **
OnInit          : Task initialized lifecycle
OnSuccess       : Task finished with success
OnDataRecived   : Data recived and beeing to pass to pipe .
OnError         : Task finish with error
*/
export MyTask implements OnInit , OnSuccess , OnDataRecived , OnError{

}
```
## Task template should be

```
<?xml version="1.0" encoding="UTF-8" ?>
<task>
    <title>Task title here</title>
    <description>
        <!-- Task description here -->
    </description>
    <version>1.0</version>
    <input>
        <schema>
        </schema>
    </input>
    <script>
        <pipe-selector>
            <!--
                The engine will affect each action return data to each pipe accumulator in key order.
                If you do not give a pipe accumulator key , the engine will use default pipe accumulator.
                If the key is not found , it will use argumented pipe accumulator.
                -->
            <action-selector pipe-option-key="value" for="parent-pipe-accumulator">
            </action-selector>
            <action-selector>
            </action-selector>
        </pipe-selector>
    </script>
</task>

```
## Project schemantics ( to be updated in order of starter projects )

```
src
    pipes
        main.pipe.ts
    tasks
        main.task.ts
        main.task.xml
    modules
        app.module.ts
main.ts
.gitingore
.env    
package.json  
tsconig.json  
readme.md
```
#Proxtarctor modules design

```
@PrxModule({
    // deprecated option
    declarations:[],
    imports:[],
    exports:[],
    // providers in this module
    providers:[]
})
export class MyModule {
    
}
```
# Features

Task Option Multi-selection value options ( example : button type in click puppeteer action .)


