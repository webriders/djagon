from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic.base import RedirectView, TemplateView
from source.game.models import GameTable
from source.game.game import Game


class CreateGameView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        game = Game()
        game.save()
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
        try:
            game = GameTable.objects.get(game_id=game_id)
        except GameTable.DoesNotExist:
            messages.warning(request, "There is no such game. Create yours!")
            return HttpResponseRedirect(reverse('djagon:home'))
        if game.players_number >= Game.PLAYERS_LIMIT:
            messages.warning(request, "Players number is limited in this game. Please, create yours!")
            return HttpResponseRedirect(reverse('djagon:home'))
        if not game.status in [game.STATUS_OPEN, game.STATUS_IDLE]:
            messages.warning(request, "This game has already been started")
            return HttpResponseRedirect(reverse('djagon:home'))

        return super(PlayGameView, self).get(self, request, *args, **kwargs)

play_game = PlayGameView.as_view()


class JoinRandomGameView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        try:
            game = GameTable.objects.filter(status=GameTable.STATUS_OPEN, players_number__lt=Game.PLAYERS_LIMIT).order_by('?')[0]
            return reverse('djagon:game-play', args=(game.game_id,))
        except IndexError:
            messages.warning(self.request, "There are no open games. Create yours!")
            return reverse('djagon:home')

join_random = JoinRandomGameView.as_view()
