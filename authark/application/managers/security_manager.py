from typing import List
from ..domain.models import Rule, Policy, Dominion
from ..domain.repositories import (
    RuleRepository, PolicyRepository)
from ..domain.common import RecordList


class SecurityManager:

    def __init__(self, rule_repository: RuleRepository,
                 policy_repository: PolicyRepository,
                ) -> None:
        self.rule_repository:RuleRepository = rule_repository
        self.policy_repository:PolicyRepository = policy_repository

    async def create_rule(self, rule_dicts: RecordList) -> None:
        rules:List[Rule] = ([Rule(**rule_dict)
                      for rule_dict in rule_dicts])
        await self.rule_repository.add(rules)
    
    async def create_policy(self, policy_dicts: RecordList) -> None:
        policies:List[Policy] = ([Policy(**policy_dict)
                      for policy_dict in policy_dicts])
        await self.policy_repository.add(policies)

    async def remove_rule(self, rule_ids: List[str]) -> bool:
        rules = await self.rule_repository.search(
            [('id', 'in', rule_ids)])
        return await self.rule_repository.remove(rules)

    async def remove_policy(self, policy_ids: List[str]) -> bool:
        policies = await self.policy_repository.search(
            [('id', 'in', policy_ids)])
        return await self.policy_repository.remove(policies)

    # async def update_rule(self, rule: Rule):
    #     existing_rule = await self.rule_repository.search(
    #         [('id', '=', rule.id)])
    #     if existing_rule:
    #         rule.id = existing_rule[0].id
    #         await self.rule_repository.add(rule)
    #     else:
    #         await self.rule_repository.add(rule)

    # async def update_policy(self, policy: Policy):
    #     existing_policy = await self.policy_repository.search(
    #         [('id', '=', policy.id)])
    #     if existing_policy:
    #         policy.id = existing_policy[0].id
    #         await self.policy_repository.add(policy)
    #     else:
    #         await self.policy_repository.add(policy)
