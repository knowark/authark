
def operations():
    return {
        # Dominion
        'dominionsHeadId': {
            'actions':{
                'default':{
                    'handler': 'StandardInformer.count',
                    'meta': {'model': 'dominion'}
                 }
             }
        },
        "dominionsGetId": {
            'actions':{
                'default':{
                    'handler': 'StandardInformer.search',
                    'meta': {'model': 'dominion'}
                }
            }
        },

        # Policy
        'policiesHeadId': {
            'actions':{
                'default':{
                    'handler': 'StandardInformer.count',
                    'meta': {'model': 'policy'}
                 }
             }
        },
        "policiesGetId": {
            'actions':{
                'default':{
                    'handler': 'StandardInformer.search',
                    'meta': {'model': 'policy'}
                }
            }
        },
        'policiesPatchId': {
            'actions':{
                'default':{
                    'handler': 'SecurityManager.create_policy',
                    'meta': {'model': 'policy'}
                }
            }
        },
        'policiesDeleteId': {
            'actions':{
                'default':{
                    'handler': 'SecurityManager.remove_policy',
                    'meta': {'model': 'policy'}
                }
            }
        },

        # Ranking
        'rankingsHeadId': {
            'actions':{
                'default':{
                    'handler': 'StandardInformer.count',
                    'meta': {'model': 'ranking'}
                 }
             }
        },
        "rankingsGetId": {
            'actions':{
                'default':{
                    'handler': 'StandardInformer.search',
                    'meta': {'model': 'ranking'}
                }
            }
        },
        'rankingsPatchId': {
            'actions':{
                'default':{
                    'handler': 'ManagementManager.assign_role',
                    'meta': {'model': 'ranking'}
                }
            }
        },
        'rankingsDeleteId': {
            'actions':{
                'default':{
                    'handler': 'ManagementManager.deassign_role',
                    'meta': {'model': 'ranking'}
                }
            }
        },

        # Registration
        'registrationsPatchId': {
            'actions':{
                'default':{
                    'handler': 'ProcedureManager.register',
                    'meta': {'model': 'registration'}
                 }
             }
        },

        # Requisition
        'requisitionsPatchId': {
            'actions':{
                'default':{
                    'handler': 'ProcedureManager.fulfill',
                    'meta': {'model': 'requisitions'}
                 }
             }
        },

        # Restriction
        'restrictionsHeadId': {
            'actions':{
                'default':{
                    'handler': 'StandardInformer.count',
                    'meta': {'model': 'restriction'}
                 }
             }
        },
        "restrictionsGetId": {
            'actions':{
                'default':{
                    'handler': 'StandardInformer.search',
                    'meta': {'model': 'restriction'}
                }
            }
        },
        'restrictionsPatchId': {
            'actions':{
                'default':{
                    'handler': 'SecurityManager.create_restriction',
                    'meta': {'model': 'restriction'}
                }
            }
        },
        'restrictionsDeleteId': {
            'actions':{
                'default':{
                    'handler': 'SecurityManager.remove_restriction',
                    'meta': {'model': 'restriction'}
                }
            }
        },

        # Role
        'rolesHeadId': {
            'actions':{
                'default':{
                    'handler': 'StandardInformer.count',
                    'meta': {'model': 'role'}
                 }
             }
        },
        "rolesGetId": {
            'actions':{
                'default':{
                    'handler': 'StandardInformer.search',
                    'meta': {'model': 'role'}
                }
            }
        },
        'rolesPatchId': {
            'actions':{
                'default':{
                    'handler': 'ManagementManager.create_role',
                    'meta': {'model': 'role'}
                }
            }
        },
        'rolesDeleteId': {
            'actions':{
                'default':{
                    'handler': 'ManagementManager.remove_role',
                    'meta': {'model': 'role'}
                }
            }
        },
        # Tenant
        'tenantsGetId': {
            'actions':{
                'default':{
                    'handler': 'TenantInformer.search_tenants',
                    'meta': {'model': 'tenant'}
                 }
             }
        },
        # Token
        'tokensPatchId': {
            'actions':{
                'default':{
                    'handler': 'AuthManager.authenticate',
                    'meta': {'model': 'token'}
                 }
             }
        },
        # User
        'usersHeadId': {
            'actions':{
                'default':{
                    'handler': 'StandardInformer.count',
                    'meta': {'model': 'user'}
                 }
             }
        },
        "usersGetId": {
            'actions':{
                'default':{
                    'handler': 'StandardInformer.search',
                    'meta': {'model': 'user'}
                }
            }
        },
        'usersPatchId': {
            'actions':{
                'default':{
                    'handler': 'ProcedureManager.update',
                    'meta': {'model': 'user'}
                }
            }
        },
        'usersDeleteId': {
            'actions':{
                'default':{
                    'handler': 'ProcedureManager.deregister',
                    'meta': {'model': 'user'}
                }
            }
        },

        # Verification
        'verificationsPatchId': {
            'actions':{
                'default':{
                    'handler': 'ProcedureManager.verify',
                    'meta': {'model': 'verification'}
                 }
             }
        },


    }
