Ext.define('pilight.Application', {
    init:function(){
        var typemap = {
            'SubMaster' : 'pilight.submaster.Panel',
            'ShowManager' : 'pilight.showrunner.Panel',
            'ColorWheel' : 'pilight.show.colorwheel.Panel',
            'Messaging' : 'pilight.messaging.Panel'
        }

        var windows = {};
        var viewport = Ext.create('Ext.Viewport', {
            layout:'border',
            items:[
                {
                    region:'center'
                }
            ]
        });

        var generateWindow = function(controllable){
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

            windows[id] = win;
        };

        var destroyWindow = function(id){
            var win = windows[id];
            if (!win) return;
            win.close();
            delete(windows[id]);
        };

        var destroyAllWindows = function() {
            for (var id in windows) {
                destroyWindow(id);
            }
        };

        var socket,
            controlServerUI = false;
        var connectWin = Ext.create('pilight.ConnectWindow', {
            connectionHandler:function(host, port){
                connectWin.setLoading('Connecting');

                socket = Ext.create('pilight.socket.Socket', {
                    host:host,
                    port:port
                });

                socket.on('connect', function(){
                    connectWin.setLoading(false);
                    connectWin.hide();

                    var controlServerUI = Ext.create('pilight.controlserver.List', {
                        region:'west',
                        split:true,
                        resizable:true
                    });
                    viewport.add(controlServerUI);

                    socket.sendCommand({'command':'getControllables'}, function(data){
                        data.forEach(generateWindow);

                        socket.listen('controlserver', {
                            receiveEvent:function(data){
                                for (var key in data) {
                                    switch (key) {
                                        case 'add':
                                            generateWindow(data[key]);
                                            break;
                                        case 'remove':
                                            var id = data[key]['id'];
                                            destroyWindow(id);
                                            break;
                                    }
                                }
                            }
                        });
                    });
                });

                socket.on('close', function(){
                    destroyAllWindows();
                    if (controlServerUI) viewport.remove(controlServerUI);
                    connectWin.setLoading(false);
                    connectWin.show();
                });
            }
        });
        connectWin.show();        
    }
});
