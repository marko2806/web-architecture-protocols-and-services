from rest_framework.test import APITestCase, APIRequestFactory, APIClient, force_authenticate
from .models import BoardGame, Publisher
from .views import BoardGameList, BoardGameDetail, PublisherList, PublisherDetail, PublisherGamesList
from django.contrib.auth.models import User
import json


class PostsListTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="marko", password="apuw2022")

        self.publisher1 = Publisher.objects.create(name="Hasbro")
        self.publisher2 = Publisher.objects.create(name="Gamewright")

    def test_publishers_get(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='marko')
        request = factory.get("/api/publishers/")
        force_authenticate(request, user=user)
        response = PublisherList.as_view()(request)
        self.assertEquals('Hasbro', response.data[0]['name'])
        self.assertEquals('Gamewright', response.data[1]['name'])
        self.assertEquals(2, len(response.data))

    def test_publishers_post(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='marko')
        request = factory.post("/api/publishers/", json.dumps({"name": "test"}), content_type='application/json')
        force_authenticate(request, user=user)
        response = PublisherList.as_view()(request)

        self.assertEquals(201, response.status_code)

        request = factory.get("/api/publishers/")
        force_authenticate(request, user=user)
        response = PublisherList.as_view()(request)

        self.assertEquals(200, response.status_code)
        self.assertEquals('test', response.data[2]['name'])
        self.assertEquals(3, len(response.data))

    def test_unauthorized_publishers_get(self):
        factory = APIRequestFactory()
        request = factory.get("/api/publishers/")
        response = PublisherList.as_view()(request)
        self.assertEquals(401, response.status_code)

    def test_unauthorized_publishers_post(self):
        factory = APIRequestFactory()
        request = factory.post("/api/publishers/", json.dumps({"name": "test"}), content_type='application/json')
        response = PublisherList.as_view()(request)
        self.assertEquals(401, response.status_code)


class PostsDetailsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="marko", password="apuw2022")

        self.publisher1 = Publisher.objects.create(name="Hasbro")
        self.publisher2 = Publisher.objects.create(name="Gamewright")

    def test_publishers_get(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='marko')
        request = factory.get("/api/publishers/{pk}")
        force_authenticate(request, user=user)
        response = PublisherDetail.as_view()(request, pk=2)

        self.assertEquals(200, response.status_code)
        self.assertEquals('Gamewright', response.data['name'])

    def test_publishers_delete(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='marko')

        request = factory.delete("/api/publishers/{pk}")
        force_authenticate(request, user=user)
        response = PublisherDetail.as_view()(request, pk=1)

        self.assertEquals(204, response.status_code)

        request = factory.get("/api/publishers/{pk}")
        force_authenticate(request, user=user)
        response = PublisherDetail.as_view()(request, pk=1)

        self.assertEquals(404, response.status_code)

    def test_publishers_put(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='marko')
        request = factory.put("/api/publishers/{pk}", json.dumps({"name": "test"}), content_type='application/json')
        force_authenticate(request, user=user)
        response = PublisherDetail.as_view()(request, pk=2)

        self.assertEquals(200, response.status_code)
        id = response.data["id"]

        request = factory.get("/api/publishers/{pk}")
        force_authenticate(request, user=user)
        response = PublisherDetail.as_view()(request, pk=id)

        self.assertEquals(200, response.status_code)
        self.assertEquals('test', response.data['name'])

    def test_unauthorized_publishers_get(self):
        factory = APIRequestFactory()
        request = factory.get("/api/publishers/{pk}")
        response = PublisherDetail.as_view()(request, pk=2)
        self.assertEquals(401, response.status_code)

    def test_unauthorized_publishers_delete(self):
        factory = APIRequestFactory()
        request = factory.delete("/api/publishers/{pk}")
        response = PublisherDetail.as_view()(request, pk=2)
        self.assertEquals(401, response.status_code)

    def test_unauthorized_publishers_put(self):
        factory = APIRequestFactory()
        request = factory.put("/api/publishers/{pk}", json.dumps({"name": "test"}), content_type='application/json')
        response = PublisherDetail.as_view()(request, pk=2)
        self.assertEquals(401, response.status_code)


class BoardGameListTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="marko", password="apuw2022")

        self.publisher1 = Publisher.objects.create(name="Hasbro")
        self.publisher2 = Publisher.objects.create(name="Gamewright")

        self.game1 = BoardGame.objects.create(name="Monopoly", min_players=2, max_players=8, publisher=self.publisher1)
        self.game2 = BoardGame.objects.create(name="Risk", min_players=2, max_players=6, publisher=self.publisher1)
        self.game3 = BoardGame.objects.create(name="Yahtzee", min_players=2, max_players=10, publisher=self.publisher1)
        self.game4 = BoardGame.objects.create(name="Outfoxed!", min_players=2, max_players=4, publisher=self.publisher2)
        self.game5 = BoardGame.objects.create(name="Sushi Roll", min_players=2, max_players=5, publisher=self.publisher2)
        self.game6 = BoardGame.objects.create(name="Qwixx", min_players=2, max_players=5, publisher=self.publisher2)

    def test_board_games_get(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='marko')
        request = factory.get("/api/board-games/")
        force_authenticate(request, user=user)
        response = BoardGameList.as_view()(request)
        self.assertEquals('Monopoly', response.data[0]['name'])
        self.assertEquals('Outfoxed!', response.data[3]['name'])
        self.assertEquals(6, len(response.data))

    def test_board_games_post(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='marko')
        request = factory.post("/api/board-games/", {"name": "test", "min_players": 2, "max_players": 10, "publisher": 1, "publisher_id": 1})
        force_authenticate(request, user=user)
        response = BoardGameList.as_view()(request)

        self.assertEquals(201, response.status_code)

        request = factory.get("/api/board-games/")
        force_authenticate(request, user=user)
        response = BoardGameList.as_view()(request)

        self.assertEquals(200, response.status_code)
        self.assertEquals('test', response.data[6]['name'])
        self.assertEquals(7, len(response.data))

    def test_unauthorized_board_games_get(self):
        factory = APIRequestFactory()
        request = factory.get("/api/board-games/")
        response = BoardGameList.as_view()(request)
        self.assertEquals(401, response.status_code)

    def test_unauthorized_board_games_post(self):
        factory = APIRequestFactory()
        request = factory.post("/api/board-games/", json.dumps({"name": "test", "min_players": 2, "max_players": 10, "publisher": 2}), content_type='application/json')
        response = BoardGameList.as_view()(request)
        self.assertEquals(401, response.status_code)


class BoardGamesDetailsTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="marko", password="apuw2022")

        self.publisher1 = Publisher.objects.create(name="Hasbro")
        self.publisher2 = Publisher.objects.create(name="Gamewright")

        self.game1 = BoardGame.objects.create(name="Monopoly", min_players=2, max_players=8, publisher=self.publisher1)
        self.game2 = BoardGame.objects.create(name="Risk", min_players=2, max_players=6, publisher=self.publisher1)
        self.game3 = BoardGame.objects.create(name="Yahtzee", min_players=2, max_players=10, publisher=self.publisher1)
        self.game4 = BoardGame.objects.create(name="Outfoxed!", min_players=2, max_players=4, publisher=self.publisher2)
        self.game5 = BoardGame.objects.create(name="Sushi Roll", min_players=2, max_players=5, publisher=self.publisher2)
        self.game6 = BoardGame.objects.create(name="Qwixx", min_players=2, max_players=5, publisher=self.publisher2)

    def test_board_games_get(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='marko')
        request = factory.get("/api/board-games/{pk}")
        force_authenticate(request, user=user)
        response = BoardGameDetail.as_view()(request, pk=2)

        self.assertEquals(200, response.status_code)
        self.assertEquals('Risk', response.data['name'])

    def test_board_games_delete(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='marko')

        request = factory.delete("/api/board-games/{pk}")
        force_authenticate(request, user=user)
        response = BoardGameDetail.as_view()(request, pk=1)

        self.assertEquals(204, response.status_code)

        request = factory.get("/api/board-games/{pk}")
        force_authenticate(request, user=user)
        response = BoardGameDetail.as_view()(request, pk=1)

        self.assertEquals(404, response.status_code)

    def test_publishers_put(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='marko')
        request = factory.put("/api/board-games/{pk}", json.dumps({"name": "test", "min_players": 2, "max_players": 10, "publisher": 1}), content_type='application/json')
        force_authenticate(request, user=user)
        response = BoardGameDetail.as_view()(request, pk=2)

        self.assertEquals(200, response.status_code)
        id = response.data["id"]

        request = factory.get("/api/board-games/{pk}")
        force_authenticate(request, user=user)
        response = BoardGameDetail.as_view()(request, pk=id)

        self.assertEquals(200, response.status_code)
        self.assertEquals('test', response.data['name'])

    def test_unauthorized_board_games_get(self):
        factory = APIRequestFactory()
        request = factory.get("/api/board-games/{pk}")
        response = BoardGameDetail.as_view()(request, pk=6)
        self.assertEquals(401, response.status_code)

    def test_unauthorized_board_games_delete(self):
        factory = APIRequestFactory()
        request = factory.delete("/api/board-games/{pk}")
        response = BoardGameDetail.as_view()(request, pk=6)
        self.assertEquals(401, response.status_code)

    def test_unauthorized_board_games_put(self):
        factory = APIRequestFactory()
        request = factory.put("/api/board-games/{pk}", json.dumps({"name": "test", "min_players": 2, "max_players": 10, "publisher": 1}), content_type='application/json')
        response = BoardGameDetail.as_view()(request, pk=6)
        self.assertEquals(401, response.status_code)


class PublisherGamesListTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="marko", password="apuw2022")

        self.publisher1 = Publisher.objects.create(name="Hasbro")
        self.publisher2 = Publisher.objects.create(name="Gamewright")

        self.game1 = BoardGame.objects.create(name="Monopoly", min_players=2, max_players=8, publisher=self.publisher1)
        self.game2 = BoardGame.objects.create(name="Risk", min_players=2, max_players=6, publisher=self.publisher1)
        self.game3 = BoardGame.objects.create(name="Yahtzee", min_players=2, max_players=10, publisher=self.publisher1)
        self.game4 = BoardGame.objects.create(name="Outfoxed!", min_players=2, max_players=4, publisher=self.publisher2)
        self.game5 = BoardGame.objects.create(name="Sushi Roll", min_players=2, max_players=5, publisher=self.publisher2)
        self.game6 = BoardGame.objects.create(name="Qwixx", min_players=2, max_players=5, publisher=self.publisher2)

    def test_publisher_games_get(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='marko')
        request = factory.get("/api/publishers/{pk}/board-games/")
        force_authenticate(request, user=user)
        response = PublisherGamesList.as_view()(request, pk=1)
        self.assertEquals('Monopoly', response.data[0]['name'])
        self.assertEquals('Risk', response.data[1]['name'])
        self.assertEquals('Yahtzee', response.data[2]['name'])
        self.assertEquals(3, len(response.data))


    def test_unauthorized_publisher_games_get(self):
        factory = APIRequestFactory()
        request = factory.get("/api/publishers/1/board-games")
        response = PublisherGamesList.as_view()(request)
        self.assertEquals(401, response.status_code)
