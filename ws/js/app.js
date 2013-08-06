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

    var typemap = {
        'SubMaster' : 'pilight.submaster.Panel',
        'ShowManager' : 'pilight.showrunner.Panel'
    }

    socket.on('connect', function(){
        socket.sendCommand({'command':'getControllables'}, function(data){
            data.forEach(function(controllable){
                var type = controllable.type;
                if (typeof(typemap[type]) == 'undefined') return;
                var win = Ext.create('Ext.window.Window', {
                    layout:'fit',
                    title:type,
                    items:[
                        Ext.create(typemap[type], {
                            socket:socket
                        })
                    ]
                });
                win.show()
            });
        });
    });
});
