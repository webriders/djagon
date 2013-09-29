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
    /** @type {jQuery} */
    container: null,

    /** @type {String} */
    url: '',

    /** @type {String} */
    gameId: '',

    /** @type {io.Socket} */
    socket: null,

    // last state returned from server
    currentState: null,

    init: function(cfg) {
        $.extend(true, this, cfg);
        this.initSocket();
        this.initResize();
    },

    initSocket: function() {
        var self = this;
        var socket = this.socket = io.connect(this.url);

        socket.on('connect', function() {
            socket.emit('join_game', self.gameId);
        });

        socket.on('initial_state', function(state) {
            self.currentState = state;
            self.drawPlayers(state.players_list);
        });
    },

    initResize: function() {
        var self = this;
        $(window).on('resize', function() {
            if (self.currentState)
                self.drawPlayers(self.currentState.players_list);
        });
    },

    drawPlayers: function(playersRawData) {
        var playersData = this.generatePlayersData(playersRawData);

        var players = d3.select(this.container[0]).selectAll('.player-info')
            .data(playersData, function(d) { return d.id; });

        this.createNewPlayers(players.enter());
        this.removeOldPlayers(players.exit());
        this.updateCurrentPlayers(d3.select(this.container[0]).selectAll('.player-info'));
    },

    createNewPlayers: function(players) {
        var el = players.append('div')
            .classed('player-info', true);

        el.append('img')
            .classed('avatar', true)
            .style('background-color', function(d) { return d.color; })
            .attr('src', function(d) {
                return d.avatar;
            });

        el.append('div')
            .classed('player-name', true)
            .append('span')
            .text(function(d) { return d.name; });
    },

    removeOldPlayers: function(players) {
        players.each(function() {
            $(this).fadeOut().promise().done(function() {
                $(this).remove();
            });
        });
    },

    updateCurrentPlayers: function(players) {
        players.transition()
            .style('left', function(d) { return d.x + 'px'; })
            .style('top', function(d) { return d.y + 'px'; });
    },

    generatePlayersData: function(players) {
        var container = this.container,
            playersAmount = players.length;

        var yourPlayerIndex;
        $.each(players, function(index, player) {
            if (player.you)
                yourPlayerIndex = index;
        });

        if (typeof yourPlayerIndex == 'undefined')
            throw "There is no current player in game state!";

        var newData = [];

        $.each(players, function(i, o) {
            var data = $.extend(true, {}, o);

            // set position
            $.extend(data, _position(i - yourPlayerIndex));

            // update avatar
            if (!data.avatar)
                data.avatar = 'http://robohash.org/' + encodeURI(data.name);

            // random color
            var colors = ['#df0012', '#009a54', '#0188cc', '#ffdd00', '#fff', '#000', '#f1b12b'];
            data.color = colors[i % colors.length];

            newData.push(data);
        });

        function _position(i) {
            var margin = 60,
                maxWidth = container.width(),
                maxHeight = container.height(),
                xr = maxWidth / 2 - margin,
                yr = maxHeight / 2 - margin,
                alpha = 2 * Math.PI / playersAmount,
                startAngle = Math.PI / 2,
                angle = startAngle + i * alpha;

            return {
                x: margin + xr * (Math.cos(angle) + 1),
                y: margin + yr * (Math.sin(angle) + 1)
            }
        }

        return newData;
    },

    drawCards: function() {

    }
};
