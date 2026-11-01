import json
from typing import Dict, Any

from cropsflow import action, Action, TaskContext, option

from cropsflow_json.contexts import JSONContext


@action(selector="json-parse")
@option(key="source", meta_type=str)
class JSONParse(Action):
    async def run(self, context: TaskContext, options: Dict[str, Any] = {}) -> TaskContext:
        return JSONContext(data=json.dumps(options.get("source")))
