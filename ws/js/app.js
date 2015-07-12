Ext.onReady(function(){
	Ext.Loader.setConfig({
		paths:{
			'pilight':'js/pilight'
		}
	});

    var viewport = Ext.create('Ext.Viewport')

    Ext.state.Manager.setProvider(new Ext.state.CookieProvider());

    var app = Ext.create('pilight.Application');
    app.init();

});
