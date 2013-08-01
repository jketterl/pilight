Ext.define('pilight.socket.Socket', {
	mixins:{
		observable:'Ext.util.Observable'
	},
	constructor:function(config){
		var me = this;
		me.mixins.observable.constructor.call(me, config);

		me.socket = new WebSocket('ws://' + me.host + ':' + me.port + '/control');
		me.socket.onopen = function(){
			console.info('websocket open');
		}

		me.socket.onerror = function(err){
			console.info('websocket error: ');
			console.info(err);
		}
	}
});
