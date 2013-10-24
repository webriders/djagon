djagon = window.djagon || {};
djagon.game = djagon.game || {};

djagon.game.page = {
    game: null,

    init: function () {
        var cnt = $('#game-table');
        this.game = new djagon.game.Game({
            container: cnt,
            gameId: cnt.data('game-id'),
            url: cnt.data('game-url')
        });
    }
};

$(function () {
    djagon.game.page.init();
});
