Implement Database
======================

:estimark:
    state=opened

The storage of the microservice records is in JSON,
looking for a similar architecture, the migration to Postgresql is performed.

Validation Criteria
-------------------

- [ ] Postgresql installed in the dependencies in the make deploy.
- [ ] Postgresql user created in the make deploy.
- [ ] Shemas Public Postgresql creado en el make deploy.
- [ ] Postgresql shemas of models created in migration.
- [ ] Repository changed to SQL type in the code.
- [ ] SQLConnector added to integration and application
