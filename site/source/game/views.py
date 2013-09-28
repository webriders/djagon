from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView, TemplateView
from source.game.uno_game import UnoGame


class CreateGameView(RedirectView):
    def get_redirect_url(self, **kwargs):
        game = UnoGame()
        game.save()
        return reverse('djagon:game-play', args=(game.game_id,))

create_game = CreateGameView.as_view()


class PlayGameView(TemplateView):
    template_name = 'game/game_play.html'

    def get_context_data(self, **kwargs):
        data = super(PlayGameView, self).get_context_data(**kwargs)
        data['game_id'] = self.kwargs.get('game_id')
        return data

play_game = PlayGameView.as_view()
