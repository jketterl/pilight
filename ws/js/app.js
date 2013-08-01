Ext.onReady(function(){
	Ext.Loader.setConfig({
		paths:{
			'pilight':'js/pilight'
		}
	});

	var socket = Ext.create('pilight.socket.Socket', {
		host:window.location.host,
		port:9001
	});
});
