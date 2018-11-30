

def test_resolver_instantiation(resolver):
    assert resolver is not None


def test_resolver_resolve_dependencies(resolver, providers_dict):
    result = resolver._resolve_dependencies(providers_dict)

    assert isinstance(result, list)
    assert len(result) == 3
    for provider in result:
        assert 'dependencies' in provider
        dependencies = provider['dependencies']
        if provider['name'] == 'BazService':
            assert len(dependencies) == 2
        else:
            assert len(dependencies) == 0


def test_resolver_resolve_instance(resolver):
    registry = {}
    provider_dict = {
        'method': 'standard_baz_service',
        'name': 'BazService',
        'dependencies': [
            {'method': 'memory_foo_repository',
             'name': 'FooRepository',
             'dependencies': []},
            {'method': 'memory_bar_repository',
             'name': 'BarRepository',
             'dependencies': []}
        ]
    }

    result = resolver._resolve_instance(provider_dict, registry)

    assert result.__class__.__name__ == 'StandardBazService'


def test_resolver_resolve(resolver, providers_dict):
    registry = resolver.resolve(providers_dict)

    assert isinstance(registry, dict)
    assert 'FooRepository' in registry
    assert 'BarRepository' in registry
    assert 'BazService' in registry


def test_resolver_dedicated_providers(resolver, dedicated_providers_dict):
    registry = resolver.resolve(dedicated_providers_dict)

    common_foo_repository = registry['FooRepository']

    dedicated_foo_repository = registry['BazService'].foo_repository

    assert id(common_foo_repository) != id(dedicated_foo_repository)
