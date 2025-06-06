"""Add interests column to POI

Revision ID: 6f694ad6e172
Revises: 749c91f9f593
Create Date: 2025-06-05 13:27:47.805194
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6f694ad6e172'
down_revision = '749c91f9f593'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(
        'points_of_interest',
        sa.Column('interests', postgresql.ARRAY(sa.String()), nullable=True)
) 
def downgrade():
    op.drop_column('points_of_interest', 'interests')
