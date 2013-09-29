djagon = window.djagon || {};

/**
 * The Game.
 * Contains players, transport (via Socket.IO), and all game mechanics.
 *
 * @param cfg Config
 * @constructor
 */
djagon.Game = function(cfg) {
    cfg && this.init(cfg);
};

djagon.Game.prototype = {
    container: null,
    url: '',
    gameId: '',
    socket: null,

    init: function(cfg) {
        $.extend(true, this, cfg);
        this.initSocket();
    },

    initSocket: function() {
        var self = this;
        var socket = this.socket = io.connect(this.url);

        socket.on('connect', function() {
            socket.emit('join_game', self.gameId);
        });

//        socket.on('update_state', function(data) {
//            var area = self.area.empty();
//            $.each(data.players, function(i, playerData) {
//                area.append(new Player(playerData).render());
//            })
//        });
    }
};

/**
 * Player.
 * Game has only one active player with playable hand.
 *
 * @param cfg Config
 * @constructor
 */
djagon.Player = function(cfg) {
    cfg && this.init(cfg);
};

djagon.Player.prototype = {
    init: function(cfg) {
        $.extend(true, this, cfg);


    }
};