Ext.define('pilight.socket.Socket', {
	mixins:{
		observable:'Ext.util.Observable'
	},
	constructor:function(config){
		var me = this;
		me.mixins.observable.constructor.call(me, config);

        me.sequence = 0;
        me.callbacks = [];

        me.addEvents(['open']);

		me.socket = new WebSocket('ws://' + me.host + ':' + me.port + '/control');
		me.socket.onopen = function(){
            me.fireEvent('connect', me)
		};

		me.socket.onerror = function(err){
			console.info('websocket error: ');
			console.info(err);
		};

        me.socket.onmessage = function(e){
            var message = Ext.JSON.decode(e.data);
            if (typeof(message.sequence) != 'undefined' && me.callbacks[message.sequence]) {
                me.callbacks[message.sequence](message.data || {});
                return;
            }
            if (typeof(message.source) != 'undefined') {
                if (me.listeners[message.source]) me.listeners[message.source].forEach(function(l){
                    l.receiveEvent(message.data || {})
                });
                return;
            }
        };

        me.socket.onclose = function(){
            me.fireEvent('close', me);
        };

        me.listeners = {};
	},
    sendCommand:function(command, callback) {
        var me = this;
        if (callback) me.callbacks[me.sequence] = callback;
        Ext.apply(command, {sequence:me.sequence++});
        me.socket.send(Ext.JSON.encode(command));
    },
    listen:function(module, listener) {
        var me = this;
        if (!me.listeners[module]) {
            me.listeners[module] = [];
            me.sendCommand({module:module, command:'listen'});
        }
        me.listeners[module].push(listener);
    }
});
