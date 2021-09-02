import inspect
from injectark import Injectark
from authark.integration.core.common import config
from authark.integration.factories import factory_builder


test_tuples = [
    ('BaseFactory', [
        ('QueryParser', 'QueryParser'),
        ('AuthProvider', 'StandardAuthProvider'),
        ('UserRepository', 'MemoryUserRepository'),
        ('CredentialRepository', 'MemoryCredentialRepository'),
        ('DominionRepository', 'MemoryDominionRepository'),
        ('RoleRepository', 'MemoryRoleRepository'),
        ('RestrictionRepository', 'MemoryRestrictionRepository'),
        ('PolicyRepository', 'MemoryPolicyRepository'),
        ('RankingRepository', 'MemoryRankingRepository'),
        ('HashService', 'MemoryHashService'),
        ('AccessTokenService', 'MemoryAccessTokenService'),
        ('RefreshTokenService', 'MemoryRefreshTokenService'),
        ('VerificationTokenService', 'MemoryVerificationTokenService'),
        ('ImportService', 'MemoryImportService'),
        ('AccessService', 'AccessService'),
        ('IdentityService', 'MemoryIdentityService'),
        ('EnrollmentService', 'EnrollmentService'),
        ('PlanSupplier', 'MemoryPlanSupplier'),
        ('AuthManager', 'AuthManager'),
        ('ManagementManager', 'ManagementManager'),
        ('ImportManager', 'ImportManager'),
        ('SessionManager', 'SessionManager'),
        ('SecurityManager', 'SecurityManager'),
        ('ProcedureManager', 'ProcedureManager'),
        ('AutharkInformer', 'StandardAutharkInformer'),
        ('ComposingInformer', 'StandardComposingInformer'),
        ('TenantInformer', 'TenantInformer'),
        ('TenantSupplier', 'MemoryTenantSupplier'),
        ('SetupSupplier', 'MemorySetupSupplier'),
        ('TemplateSupplier', 'MemoryTemplateSupplier'),
    ]),
    ('CheckFactory', [
        ('AuthProvider', 'StandardAuthProvider'),
        ('TenantSupplier', 'MemoryTenantSupplier'),
        ('HashService', 'MemoryHashService'),
        ('UserRepository', 'MemoryUserRepository'),
        ('CredentialRepository', 'MemoryCredentialRepository'),
        ('RoleRepository', 'MemoryRoleRepository'),
        ('RankingRepository', 'MemoryRankingRepository'),
        ('RestrictionRepository', 'MemoryRestrictionRepository'),
        ('PolicyRepository', 'MemoryPolicyRepository'),
        ('DominionRepository', 'MemoryDominionRepository'),
        ('AccessTokenService', 'PyJWTAccessTokenService'),
        ('AccessService', 'AccessService'),
    ]),
    ('CryptoFactory', [
        ('HashService', 'PasslibHashService'),
        ('TokenService', 'PyJWTTokenService'),
        ('AccessTokenService', 'PyJWTAccessTokenService'),
        ('RefreshTokenService', 'PyJWTRefreshTokenService'),
        ('VerificationTokenService', 'PyJWTVerificationTokenService'),
    ]),
    ('JsonFactory', [
        ('UserRepository', 'JsonUserRepository'),
        ('CredentialRepository', 'JsonCredentialRepository'),
        ('DominionRepository', 'JsonDominionRepository'),
        ('RoleRepository', 'JsonRoleRepository'),
        ('RestrictionRepository', 'JsonRestrictionRepository'),
        ('PolicyRepository', 'JsonPolicyRepository'),
        ('RankingRepository', 'JsonRankingRepository'),
        ('ImportService', 'JsonImportService'),
        ('TenantSupplier', 'JsonTenantSupplier'),
        ('PlanSupplier', 'JsonPlanSupplier'),
        ('SetupSupplier', 'JsonSetupSupplier'),
    ]),
    ('WebFactory', [
        ('TemplateSupplier', 'JinjaTemplateSupplier'),
    ]),
    ('OauthFactory', [
        ('IdentityService', 'OauthIdentityService'),
    ]),
]


def test_factories():
    for factory_name, dependencies in test_tuples:
        factory = factory_builder.build(config, name=factory_name)

        injector = Injectark(factory=factory)

        for abstract, concrete in dependencies:
            result = injector.resolve(abstract)
            assert type(result).__name__ == concrete
