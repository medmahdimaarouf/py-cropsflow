"""
constants.py

This module defines all internal constant keys used across decorators, metadata annotations,
and configuration options for the Proxtractor framework. It centralizes the naming of
watermarks, annotation keys, and option tags used for dependency injection, module
declarations, task templates, and playbook execution behavior.

Sections included:
- Decorator watermark keys for marking injectable types, actions, modules, and pipes
- Annotation keys for declarations and providers
- Action and Pipe configuration constants
- Task and template metadata keys
- Playbook-specific syntax keywords and runtime flags
- Resource and injection-related constants

These constants ensure consistency and reduce the risk of typos in metadata usage across the system.
"""

# DECORATOR Type Key
DECORATOR_WATERMARKS = "_watermarks_"

# Watermarks
INJECTABLE_WATERMARK = "__injectable__"
PIPE_WATERMARK = "__pipe__"
ACTION_WATERMARK = "__action__"
TASK_WATERMARK = "__task__"
MODULE_WATERMARK = "__module__"
GROUP_WATERMARK = '__group__'
DECLARATIONS_WATERMARK = '__declaration__'
# Declaration annotation keys
DECLARATIONS_ANNOTATION_KEY = '_declarations_'
# Injectable DECORATOR Providers
INJECTABLE_DECORATOR_INJECTION_SCOPE_KEY = "_injectable_decorator_scope_"

# Injectable DECORATOR Scope
INJECTABLE_DECORATOR_SCOPE_KEY = "_injectable_DECORATOR_scope_"

# Module DECORATOR Keys
MODULE_DECORATOR_PROVIDERS_KEY = "_module_DECORATOR_providers_"
MODULE_DECORATOR_DECLARATIONS_KEY = "_module_DECORATOR_declarations_"
MODULE_DECORATOR_IMPORTS_KEY = "_module_DECORATOR_imports_"
MODULE_DECORATOR_EXPORTS_KEY = "_module_DECORATOR_exports_"

GROUP_DECORATOR_NAME_KEY = "_GROUP_DECORATOR_NAME_"
GROUP_DECORATOR_ROUTE_KEY = "_GROUP_DECORATOR_ROUTE_"

# Action DECORATOR Keys
ACTION_DECORATOR_SELECTOR_KEY = "_action_selector_"
ACTION_DECORATOR_PROVIDERS_KEY = "_action_providers_"
ACTION_DECORATOR_AUTO_NEXT_KEY = '_action_auto_next_'

# DataPipe DECORATOR Keys
DATAPIPE_DECORATOR_SELECTOR_KEY = "_datapipe_selector_"
DATAPIPE_DECORATOR_ACCESSOR_KEY = "_datapipe_accessor_"
DATAPIPE_DECORATOR_ACCUMULATORS_KEY = "_datapipe_accumulators_"

# Option DECORATOR KEYS
OPTION_DECORATOR_KEY = "_option_key_"

# Task DECORATOR Keys
TASK_DECORATOR_TEMPLATE_URI_KEY = "_task_template_url_"
TASK_DECORATOR_TEMPLATE_KEY = "_task_template_"

# Inject DECORATOR Keys
INJECT_FN_DEPENDENCY_KEY = "__inject_method_dependencies__"

# Resource Paths
RESOURCES_PATH_PROVIDER_TOKEN = "_resources_path_provider_token_"
DEFAULT_RESOURCES_PATH = "_/default/resources/path_"

# Playbook syntax keys
PLAYBOOK_TRANSFORMER_PIPE_ID_OPTION_KEY = 'pipe-id'
PLAYBOOK_ACCUMULATOR_ACCESSOR_OPTION_KEY = 'pipe-accessor'
PLAYBOOK_IS_ASYNC_OPTION_KEY = 'async'
PLAYBOOK_IS_SKIPPABLE_OPTION_KEY = 'skippable'
PLAYBOOK_NODE_ID_OPTION_KEY = 'id'
