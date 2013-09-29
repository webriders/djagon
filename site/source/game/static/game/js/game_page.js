djagon = window.djagon || {};

djagon.gamePage = {
    game: null,

    init: function() {
        var cnt = $('#game-table');
        this.game = new djagon.Game({
            container: cnt,
            gameId: cnt.data('game-id'),
            url: cnt.data('game-url')
        });
    }
};

$(function() {
    djagon.gamePage.init();
});