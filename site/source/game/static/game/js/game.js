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

    cardsURL: '/static/game/img/cards/', // sorry for this, we have no time, DjangoDash 2013 time is running out

    init: function(cfg) {
        $.extend(true, this, cfg);
        this.initSocket();
        this.initResize();
    },

    initSocket: function() {
        var self = this;
        var socket = this.socket = io.connect(this.url);

        socket.on('connect', function() {
            socket.emit('join_game', self.gameId, self.getSessionId());
        });

        socket.on('initial_state', function(state) {
            console.log('initial_state', 'received');
            self.gameState = 'before';
            self.currentState = state;
            self.draw(state);
        });

        socket.on('game_start', function(state) {
            console.log('game_start', 'received');
            self.gameState = 'playing';
            self.currentState = state;
            self.draw(state);
        });
    },

    getSessionId: function() {
        if (!($.cookie('sessid'))) {
            $.cookie('sessid', this.gameId + '-' + Math.floor(Math.random() * 100000 ));
        }
        return $.cookie('sessid');
    },

    draw: function(state) {
        var playersData = this.generatePlayersData(state.players_list);
        var cardsData = this.generateCardsData(playersData);
        var yourCardsData = cardsData.your;
        var otherCardsData = cardsData.other;

        this.drawPlayers(playersData);
        this.drawYourCards(yourCardsData);
        this.drawOtherCards(otherCardsData);
    },

    drawPlayers: function(playersData) {
        var players = d3.select(this.container[0]).selectAll('.player-info')
            .data(playersData, function(d) {
                return d.id;
            });

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
            .style('background-color', function(d) {
                return d.color;
            })
            .attr('src', function(d) {
                return d.avatar;
            });

        // title
        el.append('div')
            .classed('player-name', true)
            .append('span')
            .text(function(d) {
                return d.name;
            });

        // "I'm ready" button
        el.filter(function(d) {
            return d.you == true;
        })
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
            .style('left', function(d) {
                return d.x + 'px';
            })
            .style('top', function(d) {
                return d.y + 'px';
            })
    },

    generatePlayersData: function(playersRawData) {
        var container = this.container,
            playersAmount = playersRawData.length;

        var yourPlayerIndex;
        $.each(playersRawData, function(index, player) {
            if (player.you)
                yourPlayerIndex = index;
        });

        if (typeof yourPlayerIndex == 'undefined')
            throw "There is no current player in game state!";

        var newData = [];

        $.each(playersRawData, function(i, o) {
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
                y: margin + yr * (Math.sin(angle) + 1),
                incline: i * alpha
            }
        }

        return newData;
    },

    generateCardsData: function(playersData) {
        var container = this.container,
            cardWidth = 141,
            cardHeight = 220;

        var yourCardsData = [],
            otherCardsData = [];

        $.each(playersData, function(index, player) {
            var cardsAmount = player.cards.length;

            $.each(player.cards, function(i, card) {
                var data;

                if (player.you) {
                    data = $.extend(true, {}, card);

                    var handWidth = 800,
                        cardMarginRight = 20,
                        cardMarginBottom = 20,
                        totalCardsWidth = cardWidth * cardsAmount + cardMarginRight * (cardsAmount - 1),
                        offset = Math.max(0, (handWidth - totalCardsWidth) / 2),
                        start = container.width() / 2 - handWidth / 2 + offset,
                        step = cardsAmount > 1
                            ? Math.min((handWidth - cardWidth) / (cardsAmount - 1), cardWidth + cardMarginRight)
                            : 0;

                    data.x = start + step * i;
                    data.y = container.height() - cardHeight - cardMarginBottom;
                    yourCardsData.push(data);
                } else {
                    data = {
                        id: card,
                        x: player.x - cardWidth / 2 + (16 / cardsAmount * i) - 16,
                        y: player.y - cardHeight / 2 + (16 / cardsAmount * i) - 16
                    };
                    otherCardsData.push(data);
                }
            })
        });

        return {
            your: yourCardsData,
            other: otherCardsData
        };
    },

    drawYourCards: function(cardsData) {
        var cards = d3.select(this.container[0]).selectAll('.card.your')
            .data(cardsData, function(d) {
                return d.id;
            });

        this.createYourNewCards(cards.enter());
        this.removeYourOldCards(cards.exit());
        this.updateYourCurrentCards(d3.select(this.container[0]).selectAll('.card.your'));
    },

    createYourNewCards: function(cards) {
        console.log('createYourNewCards', cards[0].length);

        var self = this;

        cards.append('div')
            .classed('card your', true)
            .on("dblclick", function(d) {
                self.makeTurn(d.id);
            })
            .append('img')
            .attr('src', function(d) {
                var color = d.color,
                    cardsURL = self.cardsURL;

                if (color == 'black' && d.value == 'wild')
                    return cardsURL + 'card-wild.png';
                else if (color == 'black' && d.value == 'draw-four')
                    return cardsURL + 'card-wild-draw-four.png';
                else
                    return cardsURL + 'card-' + d.value + '.png';
            })
            .style('background-color', function(d) {
                return {
                    black: '#000',
                    red: '#ed1c24',
                    green: '#00a650',
                    blue: '#0994dd',
                    yellow: '#fedd03'
                }[d.color];
            });
    },

    removeYourOldCards: function(cards) {
        console.log('removeYourOldCards', cards[0].length);

        cards.each(function() {
            $(this).fadeOut().promise().done(function() {
                $(this).remove();
            });
        });
    },

    updateYourCurrentCards: function(cards) {
        console.log('updateYourCurrentCards', cards[0].length);

        var maxWidth = this.container.width(),
            maxHeight = this.container.height(),
            cardWidth = 141,
            cardHeight = 220;

        cards.style('left', maxWidth / 2 - cardWidth / 2)
            .style('top', maxHeight / 2 - cardHeight / 2);

        cards.transition()
            .style('left', function(d) {
                return d.x + 'px';
            })
            .style('top', function(d) {
                return d.y + 'px';
            })
    },

    drawOtherCards: function(cardsData) {
        var cards = d3.select(this.container[0]).selectAll('.card.other')
            .data(cardsData, function(d) {
                return d.id;
            });

        this.createOtherNewCards(cards.enter());
        this.removeOtherOldCards(cards.exit());
        this.updateOtherCurrentCards(d3.select(this.container[0]).selectAll('.card.other'));
    },

    createOtherNewCards: function(cards) {
        console.log('createOtherNewCards', cards[0].length);

        var cardBackSide = this.cardsURL + 'card-back-side.png';

        cards.append('div')
            .classed('card other', true)
            .append('img')
            .attr('src', cardBackSide);
    },

    removeOtherOldCards: function(cards) {
        console.log('removeOtherOldCards', cards[0].length);

        cards.each(function() {
            $(this).fadeOut().promise().done(function() {
                $(this).remove();
            });
        });
    },

    updateOtherCurrentCards: function(cards) {
        console.log('updateOtherCurrentCards', cards[0].length);

        var maxWidth = this.container.width(),
            maxHeight = this.container.height(),
            cardWidth = 141,
            cardHeight = 220;

        cards.style('left', maxWidth / 2 - cardWidth / 2)
            .style('top', maxHeight / 2 - cardHeight / 2);

        cards.transition()
            .style('left', function(d) {
                return d.x + 'px';
            })
            .style('top', function(d) {
                return d.y + 'px';
            });
    },

    initResize: function() {
        var self = this;

        $(window).on('resize', function() {
            if (self.currentState)
                self.draw(self.currentState);
        });
    },

    sendReadyState: function() {
        if (this.gameState != 'before') {
            alert("You can't do this now, sorry...");
        } else {
            this.socket.emit("start_confirm", this.gameId);
            console.log('start_confirm', 'sent');
        }
    },

    makeTurn: function(card_id) {
         this.socket.emit("make_turn", this.gameId, card_id);
    }
};
