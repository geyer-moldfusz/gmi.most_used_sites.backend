from gmi.most_used_sites.backend.models import User

def test_user_model(session):
    user = User(unique_id='foo')

    session.add(user)
    session.commit()

    assert(user.id > 0)
