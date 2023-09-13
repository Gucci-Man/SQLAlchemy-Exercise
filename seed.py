"""Seed file to make sample data for db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Create user data
superman = User(first_name="Clark", last_name="Kent", image_url=None)
batman = User(
    first_name="Bruce",
    last_name="Wayne",
    image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMUJ2eluUMsAft7EjoRqUegTo-TxTe4I1gRg&usqp=CAU",
)
ironman = User(
    first_name="Tony",
    last_name="Stark",
    image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_cAlWyfiAdWCS1DAfrC7r3hf08sfRF6ygew&usqp=CAU",
)

db.session.add_all([superman, batman, ironman])
db.session.commit()

# create post data
p1 = Post(title="Metropolis!", content="Metropolis is in Danger", user_code=1)
p2 = Post(title="Daily News", content="Metropolis is at peace", user_code=1)
p3 = Post(title="Gotham News", content="Gotham is taken over by joker", user_code=2)
p4 = Post(title="Arkham Series", content="Arkham Knight attacks again", user_code=2)
p5 = Post(title="Avengers Daily", content="Avengers save the world again", user_code=3)

db.session.add_all([p1, p2, p3, p4, p5])
db.session.commit()
