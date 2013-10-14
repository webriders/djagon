from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic.base import RedirectView, TemplateView
from source.storage.exceptions import GameDoesNotExist, NoOpenedGames
from source.storage.models import StoredGame
from source.storage import utils
from source.uno.game import Game


class CreateGameView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        game = utils.create_new_game("new_game")
        return reverse('djagon:game-play', args=(game.game_id,))


create_game = CreateGameView.as_view()


class PlayGameView(TemplateView):
    template_name = 'game/game_page.html'

    def get_context_data(self, **kwargs):
        data = super(PlayGameView, self).get_context_data(**kwargs)
        data['game_id'] = self.kwargs.get('game_id')
        data['game_url'] = settings.GAME_SOCKET_URL
        return data

    def get(self, request, *args, **kwargs):
        game_id = self.kwargs.get('game_id')
        sessid = request.COOKIES.get('sessid')

        try:
            game, game_state = utils.fetch_game(game_id=game_id)
        except GameDoesNotExist:
            messages.warning(request, "There is no such game. Create yours!")
            return HttpResponseRedirect(reverse('djagon:home'))

        if len(game.players) == Game.PLAYERS_LIMIT:
            messages.warning(request, "Players number is limited in this game. Please, create yours!")
            return HttpResponseRedirect(reverse('djagon:home'))

        if game_state == StoredGame.STATE_ACTIVE:
            if not sessid or not game.resolve().user_is_member(sessid):
                messages.warning(request, "This game has already been started")
                return HttpResponseRedirect(reverse('djagon:home'))
        elif not game_state in [StoredGame.STATE_OPEN, StoredGame.STATE_IDLE]:
            messages.warning(request, "This game has already been started")
            return HttpResponseRedirect(reverse('djagon:home'))

        return super(PlayGameView, self).get(self, request, *args, **kwargs)


play_game = PlayGameView.as_view()


class JoinRandomGameView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        try:
            game = utils.fetch_any_game()
            return reverse('djagon:game-play', args=(game.game_id,))
        except NoOpenedGames:
            messages.warning(self.request, "There are no open games. Create yours!")
            return reverse('djagon:home')


join_random = JoinRandomGameView.as_view()
