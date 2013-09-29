djagon = window.djagon || {};
djagon.game = djagon.game || {};

/**
 * The Game.
 * Contains players, transport (via Socket.IO), and all game mechanics.
 *
 * @param cfg Config
 * @constructor
 */
djagon.game.Game = function(cfg) {
    cfg && this.init(cfg);
};

djagon.game.Game.prototype = {
    container: null,
    url: '',
    gameId: '',
    socket: null,
    players: null,

    init: function(cfg) {
        $.extend(true, this, cfg);
        this.players = [];
        this.initSocket();
    },

    initSocket: function() {
        var self = this;
        var socket = this.socket = io.connect(this.url);

        socket.on('connect', function() {
            socket.emit('join_game', self.gameId);
        });
    }
};

/**
 * Abstract player class (for both: main player and other players).
 *
 * @param {Object=} cfg Config
 * @constructor
 */
djagon.game.Player = function(cfg) {
    cfg && this.init(cfg);
};

djagon.game.Player.prototype = {
    cards: 0,
    game: null,

    init: function(cfg) {
        $.extend(true, this, cfg);
        // TODO
    }
};

/**
 * Main player.
 * Game has only one main player with playable hand.
 *
 * @param {Object=} cfg Config
 * @constructor
 */
djagon.game.MainPlayer = function(cfg) {
    cfg && this.init(cfg);
};

djagon.game.MainPlayer.prototype = $.extend(true, new djagon.game.Player(), {
    init: function(cfg) {
        $.extend(true, this, cfg);
        // TODO
    }
});
