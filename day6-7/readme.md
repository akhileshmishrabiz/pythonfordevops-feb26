# RDS instance

**RDS Connection Details**

- **User:** `postgres`
- **Password:** `Admin1234`
- **Database:** `rds_migration`
- **Port:** `5432`
- **Host:** `rds-migration.cvik8accw2tk.ap-south-1.rds.amazonaws.com`

**SQLAlchemy Connection String:**

```python
db_link = 'postgresql://postgres:Admin1234@rds-migration.cvik8accw2tk.ap-south-1.rds.amazonaws.com:5432/rds_migration'
```