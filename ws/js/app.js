Ext.onReady(function(){
	Ext.Loader.setConfig({
		paths:{
			'pilight':'js/pilight'
		}
	});

    var viewport = Ext.create('Ext.Viewport')

    Ext.state.Manager.setProvider(new Ext.state.CookieProvider());

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
                var id = controllable.id;
                if (typeof(typemap[type]) == 'undefined') return;
                var win = Ext.create('Ext.window.Window', {
                    layout:'fit',
                    title:type,
                    stateful:true,
                    stateId:id,
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
