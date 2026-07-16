## Spec

- 모든 모델 import (User, Team, TeamMember, Project, Dataset, DatasetVersion, Experiment, ExperimentParam)
- from app.models import Base -> Base.metadata에 모든 모델 등록
- Alembic이 이 파일을 통해 target_metadata를 감지

## Completion

- [ ] from app.models import Base -> 모든 테이블 metadata에 포함 확인
- [ ] alembic revision --autogenerate -> 모든 테이블 migration 생성
