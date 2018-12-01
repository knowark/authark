from inspect import signature
from .types import (
    ProviderDict, ProvidersDict, ProvidersList,
    Config, Registry, Factories)


class Resolver:
    def __init__(self, config: Config, factories: Factories) -> None:
        self.config = config
        self.factories = factories
        self.default_factory = self.config['factory']

    def resolve(self, providers: ProvidersDict) -> Registry:
        providers_list = self._resolve_dependencies(providers)

        registry = {}  # type: Registry
        for provider in providers_list:
            if provider['name'] in registry:
                continue
            self._resolve_instance(provider, registry)

        return registry

    def _resolve_dependencies(self, providers: ProvidersDict
                              ) -> ProvidersList:

        for key, value in providers.items():
            factory = value.get('factory', self.default_factory)
            method = value.get('method')

            annotations = signature(getattr(
                self.factories[factory], method)).parameters

            dedicated_providers = value.get('providers', {})

            providers[key]['name'] = key
            providers[key]['dependencies'] = [
                providers[value.annotation.__name__] for key, value in
                annotations.items() if key != 'return'
            ]

        return list(providers.values())

    def _resolve_instance(self, provider: ProviderDict,
                          registry: Registry) -> object:

        arguments = []
        dedicated_dependencies = provider.get('providers', {})
        for dependency in provider['dependencies']:
            name = dependency['name']
            if name in dedicated_dependencies:
                dependency['method'] = dedicated_dependencies[name]
                del dependency['name']
                dependency_instance = self._resolve_instance(
                    dependency, registry)
            elif dependency['name'] in registry:
                dependency_instance = registry[dependency['name']]
            else:
                dependency_instance = self._resolve_instance(
                    dependency, registry)
            arguments.append(dependency_instance)

        factory = provider.get('factory', self.default_factory)
        method = provider['method']

        instance = getattr(self.factories[factory], method)(*arguments)

        if provider.get('name'):
            registry[provider['name']] = instance

        return instance
