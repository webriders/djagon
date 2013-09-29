from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
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

play_game = PlayGameView.as_view()


class JoinRandomGameView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        try:
            game = GameTable.objects.filter(status=GameTable.STATUS_OPEN).order_by('?')[0]
            return reverse('djagon:game-play', args=(game.game_id,))
        except IndexError:
            messages.warning(self.request, "There are no open games. Create yours!")
            return reverse('djagon:home')

join_random = JoinRandomGameView.as_view()
