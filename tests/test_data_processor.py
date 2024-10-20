import pandas as pd
import pytest

from market_calendar_tool.scraper.data_processor import (
    DataProcessingError,
    DataProcessor,
)

SAMPLE_RAW_BASE_DATA = {
    "days": [
        {
            "events": [
                {"id": 139497, "name": "Bank Holiday"},
                {"id": 141896, "name": "MPC Member Speaks"},
            ]
        }
    ]
}

SAMPLE_RAW_EXT_DATA = {
    "data": {
        "event_id": 141895,
        "specs": [
            {
                "order": -20,
                "title": "Description",
                "html": "Due to speak about improving Maori access to capital, in Taupo;",
            }
        ],
        "history": {
            "events": [
                {
                    "event_id": 140427,
                    "impact": "medium",
                    "impact_class": "icon--ff-impact-ora",
                    "date": "Aug 16, 2024",
                    "url": "/calendar?day=aug16.2024#detail=140427",
                    "description": "Due to speak about monetary policy at an event hosted by the Wellington Chamber of Commerce.",
                }
            ]
        },
        "linked_threads": {"news": [{"id": 1308739, "html": "\t<div></div>\n\t"}]},
    }
}


@pytest.fixture
def mock_processor():
    return DataProcessor(SAMPLE_RAW_BASE_DATA)


@pytest.fixture
def mock_ext_processor():
    return DataProcessor(SAMPLE_RAW_EXT_DATA)


def test_to_base_df(mock_processor):
    df = mock_processor.to_base_df()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["id", "name"]
    assert len(df) == 2
    assert df["id"].tolist() == [139497, 141896]
    assert df["name"].tolist() == ["Bank Holiday", "MPC Member Speaks"]


def test_to_specs_df(mock_ext_processor):
    df = mock_ext_processor.to_specs_df()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["order", "title", "html", "id"]
    assert len(df) == 1
    assert df["order"].tolist() == [-20]


def test_to_news_df(mock_ext_processor):
    df = mock_ext_processor.to_news_df()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["news_id", "html", "id"]
    assert len(df) == 1
    assert df["id"].tolist() == [141895]


def test_to_history_df(mock_ext_processor):
    df = mock_ext_processor.to_history_df()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == 1
    assert df["event_id"].tolist() == [140427]
    assert df["id"].tolist() == [141895]


def test_invalid_record_path():
    processor = DataProcessor(SAMPLE_RAW_BASE_DATA)
    with pytest.raises(DataProcessingError) as exc_info:
        processor._to_df(record_path=["invalid", "path"])
    assert "Failed to convert data to DataFrame" in str(exc_info.value)
