from nba_fantasy.raw_capture import save_raw_json, load_raw_json


def test_save_and_load_raw_json(tmp_path):
    response = {
        "success": True,
        "data": {
            "leagueName": "Lou Williams Memorial League",
            "players": [
                {
                    "name": "Ayo Dosunmu",
                    "team": "MIN",
                }
            ],
        },
    }

    output_path = tmp_path / "flaim_roster_raw_test.json"

    saved_path = save_raw_json(response, output_path)

    assert saved_path.exists()

    loaded = load_raw_json(saved_path)

    assert loaded["success"] is True
    assert loaded["data"]["leagueName"] == "Lou Williams Memorial League"
    assert loaded["data"]["players"][0]["name"] == "Ayo Dosunmu"