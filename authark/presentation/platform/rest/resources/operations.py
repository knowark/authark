
def operations():
    return {
        # Dominion
        'dominionsHeadId': {
            'actions':{
                'default':{
                    'handler': 'AutharkInformer.count',
                    'meta': {'model': 'dominion'}
                 }
             }
        },
        "dominionsGetId": {
            'actions':{
                'default':{
                    'handler': 'AutharkInformer.search',
                    'meta': {'model': 'dominion'}
                }
            }
        },

        # Policy
        'policiesHeadId': {
            'actions':{
                'default':{
                    'handler': 'AutharkInformer.count',
                    'meta': {'model': 'policy'}
                 }
             }
        },
        "policiesGetId": {
            'actions':{
                'default':{
                    'handler': 'AutharkInformer.search',
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
                    'handler': 'AutharkInformer.count',
                    'meta': {'model': 'ranking'}
                 }
             }
        },
        "rankingsGetId": {
            'actions':{
                'default':{
                    'handler': 'AutharkInformer.search',
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

        # Restriction
        'restrictionsHeadId': {
            'actions':{
                'default':{
                    'handler': 'AutharkInformer.count',
                    'meta': {'model': 'restriction'}
                 }
             }
        },
        "restrictionsGetId": {
            'actions':{
                'default':{
                    'handler': 'AutharkInformer.search',
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
                    'handler': 'AutharkInformer.count',
                    'meta': {'model': 'role'}
                 }
             }
        },
        "rolesGetId": {
            'actions':{
                'default':{
                    'handler': 'AutharkInformer.search',
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

        # User
        'usersHeadId': {
            'actions':{
                'default':{
                    'handler': 'AutharkInformer.count',
                    'meta': {'model': 'user'}
                 }
             }
        },
        "usersGetId": {
            'actions':{
                'default':{
                    'handler': 'AutharkInformer.search',
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



    }
