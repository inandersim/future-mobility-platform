from uuid import uuid4
import pytest
from app.sovereignty import SovereigntyViolation, assert_country_scope, assert_organization_scope


def test_same_country_is_allowed() -> None:
    country = uuid4()
    assert_country_scope(country, country)


def test_cross_country_is_denied() -> None:
    with pytest.raises(SovereigntyViolation):
        assert_country_scope(uuid4(), uuid4())


def test_same_country_different_organization_is_denied() -> None:
    country = uuid4()
    with pytest.raises(SovereigntyViolation):
        assert_organization_scope(country, country, uuid4(), uuid4())


def test_country_scope_blocks_cross_country_before_org_check() -> None:
    with pytest.raises(SovereigntyViolation, match="Cross-country"):
        assert_organization_scope(uuid4(), uuid4(), uuid4(), uuid4())
