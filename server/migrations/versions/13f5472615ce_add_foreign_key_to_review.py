"""add foreign key to Review

Revision ID: 13f5472615ce
Revises: 48c4b5ca040e
Create Date: 2025-06-20 10:47:36.298202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13f5472615ce'
down_revision = '48c4b5ca040e'
branch_labels = None
depends_on = None


def upgrade():
    # Check if the column exists before adding it
    inspector = sa.inspect(op.get_bind())
    columns = [col['name'] for col in inspector.get_columns('reviews')]
    if 'employee_id' not in columns:
        op.add_column('reviews', sa.Column('employee_id', sa.Integer(), nullable=True))
    
    # Ensure the foreign key constraint is created
    op.create_foreign_key(
        'fk_reviews_employee_id_employees',  # Constraint name
        'reviews', 'employees', 
        ['employee_id'], ['id']
    )

def downgrade():
    # Drop the foreign key constraint
    op.drop_constraint('fk_reviews_employee_id_employees', 'reviews', type_='foreignkey')
    # Optionally drop the column if it was added
    inspector = sa.inspect(op.get_bind())
    columns = [col['name'] for col in inspector.get_columns('reviews')]
    if 'employee_id' in columns:
        op.drop_column('reviews', 'employee_id')