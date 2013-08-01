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
            if (typeof(message.sequence) != 'undefined' && me.callbacks[message.sequence]) me.callbacks[message.sequence](message.data || {});
        };
	},
    sendCommand:function(command, callback) {
        var me = this;
        if (callback) me.callbacks[me.sequence] = callback;
        Ext.apply(command, {sequence:me.sequence++});
        me.socket.send(Ext.JSON.encode(command));
    }
});
