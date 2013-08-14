Ext.define('pilight.submaster.Channel', {
    mixins:{
        observable:'Ext.util.Observable'
    },
    constructor:function(config){
        this.mixins.observable.constructor.call(this, config);

        this.addEvents('valueChanged');
    },
    setValue:function(value, callback){
        this.submaster.setValue(this, value, callback);
    },
    getValue:function(value){
        return this.value;
    },
    updateValue:function(value){
        this.value = value;
        this.fireEvent('valueChanged', value);
    }
});
