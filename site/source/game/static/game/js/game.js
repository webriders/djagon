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

    // last state of the table (all players and cards) returned from server
    currentState: null,

    // state of the game: 'before', 'playing', 'after'
    gameState: 'before',

    currentPlayerId: null,

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
            console.log('initial_state', 'received');
            self.gameState = 'before';
            self.currentState = state;
            self.drawPlayers(state.players_list);
        });

        socket.on('initial_state', function(state) {});
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
        var self = this;

        var el = players.append('div')
            .classed('player-info', true);

        // avatar
        el.append('img')
            .classed('avatar', true)
            .style('background-color', function(d) { return d.color; })
            .attr('src', function(d) {
                return d.avatar;
            });

        // title
        el.append('div')
            .classed('player-name', true)
            .append('span')
            .text(function(d) { return d.name; });

        // "I'm ready" button
        el.filter(function(d) { return d.you == true; })
            .append('button')
            .classed('ready-button', true)
            .text('I am ready!')
            .on('click', function() {
                self.sendReadyState();

            });

        // "I'm ready" mark
        el.append('div')
            .classed('ready-mark', true);
    },

    removeOldPlayers: function(players) {
        players.each(function() {
            $(this).fadeOut().promise().done(function() {
                $(this).remove();
            });
        });
    },

    updateCurrentPlayers: function(players) {
        var self = this;

        players
            .each(function(d) {
                var readyButton = $(this).find('.ready-button'),
                    readyMark = $(this).find('.ready-mark');

                readyButton[self.gameState == 'before' && d.you == true && d.lamp == false ? 'addClass' : 'removeClass']('active');
                readyMark[self.gameState == 'before' && d.lamp == true ? 'addClass' : 'removeClass']('active');
            })
            .transition()
            .style('left', function(d) { return d.x + 'px'; })
            .style('top', function(d) { return d.y + 'px'; })

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

            // random color
            var colors = ['#df0012', '#009a54', '#0188cc', '#ffdd00', '#fff', '#aaa', '#f1b12b'];
            data.color = colors[i % colors.length];

            data.you = !!data.you;

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

    initResize: function() {
        var self = this;

        $(window).on('resize', function() {
            if (self.currentState)
                self.drawPlayers(self.currentState.players_list);
        });
    },

    sendReadyState: function() {
        if (this.gameState != 'before') {
            alert("You can't do this now, sorry...");
        } else {
            console.log('start_confirm', 'sent');
            this.socket.emit("start_confirm", this.gameId);
        }
    },

    drawCards: function() {

    }
};
