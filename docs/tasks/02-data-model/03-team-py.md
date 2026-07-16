## Story

팀을 생성하고 멤버를 초대한다. 팀 단위로 프로젝트/데이터셋/실험 공유.

## Spec

**teams**: id(UUID PK), name(VARCHAR 100), description(TEXT), owner_id(FK users)

**team_members**: UNIQUE(team_id, user_id), id(UUID PK), team_id(FK), user_id(FK), role(VARCHAR 20) CHECK('owner','admin','member')

## Completion

- [ ] CREATE TABLE teams + team_members
- [ ] UNIQUE(team_id, user_id) 포함
- [ ] role CHECK 제약 포함
