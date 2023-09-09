from unittest import TestCase
from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Test for views for Users"""

    def setUp(self):
        """Add a sample user"""

        User.query.delete()

        user = User(
            first_name="John",
            last_name="Doe",
            image_url="https://pinsandaces.com/cdn/shop/products/BF22_BallMarkers_MainImageFloatingArtboard5copy_1800x.jpg?v=1669140481",
        )

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction"""

        db.session.rollback()

    def test_redirect_users(self):
        """Test redirecting to the user listing home page"""
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)

    def test_list_user(self):
        """Test listing the users"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("John", html)

    def test_show_user(self):
        """Test showing detail of the user"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>John Doe</h1>", html)

    def test_add_user(self):
        """Test adding a new user"""
        with app.test_client() as client:
            d = {"first_name": "Gucci", "last_name": "Chanel", "image_url": ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Gucci Chanel</a>", html)
