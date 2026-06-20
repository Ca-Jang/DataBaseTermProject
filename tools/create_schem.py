import duckdb
import pandas as pd

db_path = "data/hero_stats.db"
con = duckdb.connect(db_path)

print("1. 데이터베이스 연결 완료")

# ==========================================
# 2. DDL: SEQUENCE 생성 및 테이블 적용
# ==========================================
ddl_query = """
-- auto increment 를 위한 SEQUENCE 생성
CREATE SEQUENCE IF NOT EXISTS seq_hero_id START 1;
CREATE SEQUENCE IF NOT EXISTS seq_map_id START 1;
CREATE SEQUENCE IF NOT EXISTS seq_tier_id START 1;

-- hero 테이블
-- 영웅의 기본 정보 저장
CREATE TABLE IF NOT EXISTS hero (
    hero_id INT DEFAULT nextval('seq_hero_id') NOT NULL,
    name VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    subrole VARCHAR NOT NULL,
    health INT NULL,
    armor INT NULL,
    shields INT NULL,
    portrait_url VARCHAR NULL,
    PRIMARY KEY (hero_id)
);

-- map 테이블
-- 맵의 기본 정보 저장
CREATE TABLE IF NOT EXISTS map (
    map_id INT DEFAULT nextval('seq_map_id') NOT NULL,
    map_name VARCHAR NOT NULL,
    mod VARCHAR NOT NULL,
    screenshot_url VARCHAR NULL,
    PRIMARY KEY (map_id)
);

-- tier 테이블
-- 티어 정보 저장
CREATE TABLE IF NOT EXISTS tier (
    tier_id INT DEFAULT nextval('seq_tier_id') NOT NULL,
    tier_name VARCHAR NOT NULL,
    tier_order INT NOT NULL,
    icon_url VARCHAR NULL,
    PRIMARY KEY (tier_id)
);

-- hero_abilities 테이블
-- 영웅의 상세 정보 저장
CREATE TABLE IF NOT EXISTS hero_abilities (
    skill_id INT NOT NULL,
    hero_id INT NOT NULL,
    skill_name VARCHAR NULL,
    description VARCHAR NULL,
    icon_url VARCHAR NULL,
    PRIMARY KEY (skill_id, hero_id),
    CONSTRAINT FK_hero_TO_hero_abilities FOREIGN KEY (hero_id) REFERENCES hero (hero_id)
);

-- perk 테이블
-- 각 영웅의 특전 저장
CREATE TABLE IF NOT EXISTS perk (
    perk_id INT NOT NULL,
    hero_id INT NOT NULL,
    perk_name VARCHAR NOT NULL,
    perk_type VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    icon_url VARCHAR NULL,
    PRIMARY KEY (perk_id, hero_id),
    CONSTRAINT FK_hero_TO_perk FOREIGN KEY (hero_id) REFERENCES hero (hero_id)
);

-- hero_stat 테이블
-- 각 영웅의 맵, 티어별 승률, 픽률, 밴률 저장
CREATE TABLE IF NOT EXISTS hero_stat (
    hero_id INT NOT NULL,
    map_id INT NOT NULL,
    tier_id INT NOT NULL,
    winrate DOUBLE NOT NULL DEFAULT 0.0,
    pickrate DOUBLE NOT NULL DEFAULT 0.0,
    banrate DOUBLE NOT NULL DEFAULT 0.0,
    PRIMARY KEY (hero_id, map_id, tier_id),
    CONSTRAINT FK_hero_TO_hero_stat FOREIGN KEY (hero_id) REFERENCES hero (hero_id),
    CONSTRAINT FK_map_TO_hero_stat FOREIGN KEY (map_id) REFERENCES map (map_id),
    CONSTRAINT FK_tier_TO_hero_stat FOREIGN KEY (tier_id) REFERENCES tier (tier_id)
);

-- favorite_hero 테이블
-- 선호 영웅 저장
CREATE TABLE IF NOT EXISTS favorite_hero (
    hero_id INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (hero_id),
    CONSTRAINT FK_hero_TO_favorite FOREIGN KEY (hero_id) REFERENCES hero (hero_id)
);
"""

con.execute(ddl_query)
print("스키마 및 시퀀스 생성 완료")