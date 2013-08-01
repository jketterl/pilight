Ext.onReady(function(){
	Ext.Loader.setConfig({
		paths:{
			'pilight':'js/pilight'
		}
	});

    var viewport = Ext.create('Ext.Viewport')

	var socket = Ext.create('pilight.socket.Socket', {
		host:window.location.host,
		port:9001
	});

    socket.on('connect', function(){
        var win = Ext.create('Ext.window.Window', {
            title:'Submaster',
            layout:'fit',
            border:false,
            items:[
                Ext.create('pilight.submaster.Panel', {
                    socket:socket
                })
            ]
        });

        win.show()

        var win = Ext.create('Ext.window.Window', {
            title:'Shows',
            layout:'fit',
            items:[
                Ext.create('pilight.showrunner.Panel', {
                    socket:socket
                })
            ]
        });

        win.show()
    });
});
