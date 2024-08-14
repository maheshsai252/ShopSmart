from snowflake.snowflake_wrapper import retrieve_last_5_user_searches

def test_user_searches():
    searches = retrieve_last_5_user_searches(user_id=1)
    assert len(searches) == 5